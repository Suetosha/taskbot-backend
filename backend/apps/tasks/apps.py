from django.apps import AppConfig


class TasksConfig(AppConfig):
    name = 'apps.tasks'
    verbose_name = "Задачи"

    def ready(self) -> None:
        from . import signals
