from abc import ABC, abstractmethod


class TextLoader(ABC):
    @abstractmethod
    def get_raw_text(self, url: str) -> str:
        raise NotImplementedError
