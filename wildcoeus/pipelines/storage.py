import os

from django.conf import settings
from django.core.files.storage import FileSystemStorage


def get_log_path(run_id: str):
    """path to store the pipeline logs"""
    return f"logs/{run_id}.log"


class LogFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        """override file if already available"""
        if self.exists(name):
            os.remove(os.path.join(settings.MEDIA_ROOT, name))

        return name
