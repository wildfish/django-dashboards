from django.core.files.storage import FileSystemStorage


def get_log_path(run_id: str):
    """path to store the pipeline logs"""
    return f"logs/{run_id}.log"


class LogFileSystemStorage(FileSystemStorage):
    def get_available_name(self, name, max_length=None):
        """delete file if already exists so we can keep the same name"""
        if self.exists(name):
            self.delete(name)

        return name
