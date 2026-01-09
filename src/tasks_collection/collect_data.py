from interfaces import TaskRepository
from tasks_collection.page_to_tasks import get_data_from_page
from tasks_collection.data_to_tasks import convert_data_to_tasks
from interfaces import TaskGenerator


class TaskCollector:
    def __init__(
        self,
        domain_urls: list[str],
        task_repository: TaskRepository,
        task_generator: TaskGenerator,
    ) -> None:
        self._domain_urls: list[str] = domain_urls
        self._task_repository: TaskRepository = task_repository
        self._task_generator: TaskGenerator = task_generator

    def collect(self) -> None:
        """
        Собирает новые данные с интернет-ресурсов и кладёт их в репозиторий
        """
        tasks = []

        for domain_url in self._domain_urls:
            new_pages_urls = self._observe_new_pages(domain_url)
            if new_pages_urls:
                for page_url in new_pages_urls:
                    page_data = get_data_from_page(page_url, domain_url)
                    tasks_from_page = convert_data_to_tasks(
                        page_data,
                        domain_url,
                        self._task_generator,
                    )
                    tasks.extend(tasks_from_page)

        for task in tasks:
            self._task_repository.save(task)

    def _observe_new_pages(self, domain_url: str) -> list[str]:
        """
        Проверяет наличие новых данных на интернет-ресурсе

        Returns:
            new_pages_urls: Список урлов на новые данные (новые посты)
        """
        raise NotImplementedError
