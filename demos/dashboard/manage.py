#!/usr/bin/env python
import os
import sys
from pathlib import Path

ROOT_DIR = Path(__file__).absolute().parent.parent.parent
sys.path.append(os.path.join(ROOT_DIR))
if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "demo.settings")
    os.environ.setdefault("DJANGO_CONFIGURATION", "Dev")

    from configurations.management import execute_from_command_line

    execute_from_command_line(sys.argv)