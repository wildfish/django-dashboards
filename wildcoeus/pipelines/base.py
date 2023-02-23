from typing import TYPE_CHECKING, Any, ClassVar, Dict, List, Optional

from django.core.exceptions import ImproperlyConfigured
from django.db.models import Model

from wildcoeus.meta import ClassWithAppConfigMeta
from wildcoeus.pipelines.registry import pipeline_registry
from wildcoeus.pipelines.results.base import PipelineExecution
from wildcoeus.pipelines.results.helpers import build_pipeline_execution
from wildcoeus.registry.registry import Registrable


if TYPE_CHECKING:  # pragma: nocover
    from wildcoeus.pipelines.runners import PipelineRunner
    from wildcoeus.pipelines.reporters.base import PipelineReporter

from wildcoeus.pipelines.status import PipelineTaskStatus
from wildcoeus.pipelines.tasks.base import Task


class Pipeline(Registrable, ClassWithAppConfigMeta):
    """
    The base pipeline class. All pipelines should be a subclass of this.
    """

    tasks: dict[str, Task] = {}
    """A dictionary of task property names mapped to the task objects"""

    ordering: Optional[dict[str, List[str]]] = None
    """
    The overridden ordering of tasks in the pipeline. If set, tasks will be ran 
    in the order they are defined in the pipeline class. If set to something other 
    than :code:`None`, it should be a dictionary of task property names mapped to
    lists of parent task property names. For example::
    
        ordering = {
            "b": ["a"],
            "c": ["b"],
        }
        
    would cause :code:`b` to be ran after :code:`a` and :code:`c` to be ran after :code:`b` 
    
    .. note::
       If defined, anything not present in the dictionary is assumes to have no
       dependencies and can be started at any point.
    """

    def __init__(self):
        self.id = self.get_id()
        self.cleaned_tasks: List[Optional[Task]] = []

    def __str__(self):
        return self._meta.verbose_name

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        if not cls._meta.abstract:
            pipeline_registry.register(cls)

    @classmethod
    def postprocess_meta(cls, current_class_meta, resolved_meta_class):
        """
        Collects all tasks and builds the :code:`tasks` dict and sets the :code:`pipeline_task`
        property on all tasks.

        :param current_class_meta: The meta class defined on this pipeline
        :param resolved_meta_class: The new meta class resolved from the current class and each
            base class
        """
        # collect all the tasks from all the base classes
        cls.tasks = {}
        for base in reversed(cls.__bases__):
            if not hasattr(base, "tasks") or not isinstance(base.tasks, dict):
                continue

            for k, v in ((k, v) for k, v in base.tasks.items() if isinstance(v, Task)):
                cls.tasks[k] = v

        # add all tasks from the current class
        for k, v in ((k, v) for k, v in cls.__dict__.items() if isinstance(v, Task)):
            cls.tasks[k] = v

        for key, task in list(cls.tasks.items()):
            task.pipeline_task = key

        return super().postprocess_meta(current_class_meta, resolved_meta_class)

    def clean_parents(
        self,
        task: Task,
        reporter: "PipelineReporter",
        runner: "PipelineRunner",
        run_id: str,
    ):
        """
        Checks that all tasks have valid parents if they are defined in the pipeline ordering

        :param task: The task to check
        :param reporter: The reporter to write any messages to
        :param runner: The runner to process the pipeline
        :param run_id: The id of the current pipeline run
        """
        # check against pipeline keys, as parent is relative to the Pipeline, not Task.id which will is
        # full task id.
        other_tasks = self.tasks.values() if self.tasks else []
        other_pipeline_tasks = [
            t.pipeline_task
            for t in other_tasks
            if t.pipeline_task != task.pipeline_task
        ]
        parent_keys = self.ordering.get(task.pipeline_task, [])

        if not all(p in other_pipeline_tasks for p in parent_keys):
            pipeline_execution = build_pipeline_execution(
                self,
                run_id,
                runner,
                reporter,
                {},
                build_all=None,
            )
            reporter.report_pipeline_execution(
                pipeline_execution,
                PipelineTaskStatus.CONFIG_ERROR,
                "One or more of the parent ids are not in the pipeline",
            )
            # TODO: make this a propper exception and make the message relate to the bad task
            raise Exception("One or more of the parent ids are not in the pipeline")

        return task

    def clean_tasks(
        self, reporter: "PipelineReporter", runner: "PipelineRunner", run_id: str
    ) -> List[Optional["Task"]]:
        """
        Checks that if ordering is set all tasks have their required parents in the pipeline

        :param reporter: The reporter to write any messages to
        :param runner: The runner to process the pipeline
        :param run_id: The id of the current pipeline run
        """
        if self.ordering:
            return list(
                map(
                    lambda t: self.clean_parents(t, reporter, runner, run_id) if t else t,
                    self.tasks.values() if self.tasks else {},
                )
            )
        else:
            return list(self.tasks.values())

    @classmethod
    def get_id(cls):
        """
        Generate id based on where the pipeline is created
        """
        return "{}.{}".format(cls._meta.app_label, cls.__name__)

    @classmethod
    def get_iterator(cls):
        """
        Returns a set of objects for multiple pipeline instances to be created for.
        If no iteration is required, :code:`None` should be returned.
        """
        return None

    @staticmethod
    def get_serializable_pipeline_object(obj):
        """
        Converts the object to a json serializable version to be stored
        in the db.

        :param obj: The object to store
        """
        if obj is None:
            return None

        return {
            "obj": obj,
        }

    def start(
        self,
        run_id: str,
        input_data: Dict[str, Any],
        runner: "PipelineRunner",
        reporter: "PipelineReporter",
    ) -> bool:
        """
        Starts the pipeline running.

        If the runner schedules the pipeline :code:`True` will be returned,
        otherwise :code:`False` will be returned. If this returns :code:`True`,
        The pipeline has been scheduled, this does not make any guarantee about
        whether the pipeline was successful.

        :param run_id: The id of the current pipeline run
        :param input_data: The data to pass to the pipeline
        :param reporter: The reporter to write any messages to
        :param runner: The runner to process the pipeline
        """
        self.cleaned_tasks = self.clean_tasks(reporter, runner, run_id)

        # create the execution object to store all pipeline results against
        execution = build_pipeline_execution(self, run_id, runner, reporter, input_data)

        if any(t is None for t in self.cleaned_tasks):
            # if any of the tasks have an invalid config cancel all others
            self.handle_config_error(execution, reporter)
            return False

        return runner.start(
            execution,
            reporter=reporter,
        )

    def handle_config_error(
        self,
        execution: PipelineExecution,
        reporter,
    ):
        """
        Handles recording a config error meaning a pipeline couldn't be started. All results
        objects will be updated to a :code:`CANCELLED` state.

        :param execution: The pipeline execution object representing the pipeline to run
        :param reporter: The reporter to write the error to
        """
        # update that pipeline has been cancelled
        execution.report_status_change(
            reporter,
            PipelineTaskStatus.CANCELLED,
            message="Pipeline cancelled due to an error in the pipeline config",
        )

        # cancel all pipeline results
        for pipeline_result in execution.get_pipeline_results():
            pipeline_result.report_status_change(
                reporter,
                PipelineTaskStatus.CANCELLED,
                message="Pipeline cancelled due to an error in the pipeline config",
                propagate=False,
            )

            # report all task executions have been cancelled
            for task_execution in pipeline_result.get_task_executions():
                task_execution.report_status_change(
                    reporter,
                    PipelineTaskStatus.CANCELLED,
                    message="Tasks cancelled due to an error in the pipeline config",
                    propagate=False,
                )

                # report all task results have been cancelled
                for task_result in task_execution.get_task_results():
                    task_result.report_status_change(
                        reporter,
                        PipelineTaskStatus.CANCELLED,
                        message="Tasks cancelled due to an error in the pipeline config",
                        propagate=False,
                    )


class ModelPipeline(Pipeline):
    """
    The base pipeline class to use when iterating over many model instances.
    """

    class Meta:
        abstract = True

        model: ClassVar[Model]
        """The model class to use when fetching objects from the database"""

    def get_queryset(self):
        """
        Returns a queryset containing all items for the model provided in the meta.
        If :code:`model` is not defined on the :code:`Meta` class this method must be
        overridden otherwise an :code:`ImproperlyConfigured` error will be raised.
        """
        if self._meta.model is not None:
            queryset = self._meta.model._default_manager.all()
        else:
            raise ImproperlyConfigured(
                "%(self)s is missing a QuerySet. Define "
                "%(self)s.Meta.model or override "
                "%(self)s.get_queryset()." % {"self": self.__class__.__name__}
            )

        return queryset

    def get_iterator(self):
        """
        Returns an iterator to run the pipeline over. By default this returns the result
        of :code:`get_queryset`.
        """
        return self.get_queryset()

    @staticmethod
    def get_serializable_pipeline_object(obj: Optional[Model]):
        """
        Serializes an django model object so that it can be stored on the pipeline result
        object.

        If :code:`obj` is not :code:`None` the object will be stored as a dictionary containing
        :code:`pk`, :code:`app_label` and :code:`model_name` so that the object can be retrieved
        from the database.

        :param obj: The object to serialize
        """
        if not obj:
            return None

        return {
            "pk": obj.pk,
            "app_label": obj._meta.app_label,
            "model_name": obj._meta.model_name,
        }
