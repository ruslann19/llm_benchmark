from interfaces import TaskGenerator, TextLoader, TaskRepository


class TaskCollector:
    def __init__(
        self,
        text_loader: TextLoader,
        task_generator: TaskGenerator,
        task_repository: TaskRepository,
    ) -> None:
        self._text_loader = text_loader
        self._task_generator = task_generator
        self._task_repository = task_repository

    def collect_tasks(self, url: str) -> None:
        """
        Собирает новые данные с интернет-ресурсов и кладёт их в репозиторий
        """
        raw_text = self._text_loader.get_raw_text(url)
        tasks = self._task_generator.generate_from_text(raw_text)

        for task in tasks:
            task.source_url = url

        return self._task_repository.add_all(tasks)
