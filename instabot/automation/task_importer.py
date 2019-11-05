import inspect
import pkgutil
from pathlib import Path
from importlib import import_module

from instabot.automation.task import Task


class TaskImporter:

    @staticmethod
    def import_tasks(package_path):
        tasks = {}
        for (_, name, _) in pkgutil.iter_modules([Path(package_path)]):
            imported_module = import_module('.' + name, package='.'.join(package_path.split('/')))

            for i in dir(imported_module):
                attribute = getattr(imported_module, i)

                if inspect.isclass(attribute) and issubclass(attribute, Task) and not inspect.isabstract(attribute):
                    tasks[attribute.task_id] = attribute

        return tasks
