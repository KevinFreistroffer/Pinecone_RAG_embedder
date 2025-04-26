from abc import ABC, abstractmethod
from utils.decorators.decorators import log_function


class _BaseProcessor(ABC):

    @abstractmethod
    def __init__(self, file_name):
        pass

    @log_function
    @abstractmethod
    def read(self):
        pass

    @log_function
    @abstractmethod
    def set_text_content(self):
        pass

    @log_function
    @abstractmethod
    def get_text_content(self):
        pass

    @log_function
    @abstractmethod
    def embeded_text_content(self):
        pass
