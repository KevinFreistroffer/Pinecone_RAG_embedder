from abc import ABC, abstractmethod

class _BaseProcessor(ABC):
    @abstractmethod
    def __init__(self, file_name):
        pass

    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def set_text_content(self):
        pass

    @abstractmethod
    def get_text_content(self):
        pass

    @abstractmethod
    def embeded_text_content(self):
        pass
