from django.utils.module_loading import import_string


def object_from_config(reporter):
    if isinstance(reporter, str):
        return import_string(reporter)()

    module_path, params = reporter
    return import_string(module_path)(**params)
