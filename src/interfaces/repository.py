from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional

# Объявляем дженерик-тип для сущности (Entity)
T = TypeVar("T")


class Repository(ABC, Generic[T]):
    @abstractmethod
    def add(self, entity: T) -> T:
        """Создаёт новую сущность и возвращает её (возможно, с присвоенным ID)."""
        raise NotImplementedError

    @abstractmethod
    def get_by_id(self, entity_id) -> Optional[T]:
        """Возвращает сущность по её идентификатору или None, если не найдена."""
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: T) -> T:
        """Обновляет существующую сущность."""
        raise NotImplementedError

    @abstractmethod
    def delete(self, entity_id) -> bool:
        """Удаляет сущность по ID. Возвращает True, если удаление прошло успешно."""
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[T]:
        """Возвращает список всех сущностей."""
        raise NotImplementedError
