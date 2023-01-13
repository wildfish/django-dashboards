from ..registry.registry import Registry


class PipeLineRegistry(Registry):
    def __init__(self):
        super().__init__(module_name="pipelines")


pipeline_registry = PipeLineRegistry()
