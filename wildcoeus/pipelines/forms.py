from django import forms


class PipelineStartForm(forms.Form):
    def __init__(self, *args, **kwargs):
        pipeline_cls = kwargs.pop("pipeline_cls")
        super().__init__(*args, **kwargs)

        # create form fields for each InputType on a task
        tasks = pipeline_cls.tasks.values() if pipeline_cls.tasks else []

        for task in tasks:
            if task.InputType:
                for f in task.InputType.__fields__.values():
                    self.fields[f"{f.name}"] = forms.CharField(required=f.required)
