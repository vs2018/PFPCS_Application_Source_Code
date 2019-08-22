from abc import ABC, abstractmethod

# Adapted from https://www.python-course.eu/python3_abstract_classes.php
class GPS(ABC):
    @abstractmethod
    def call_api(self):
        pass

    @abstractmethod
    def configure_api_data(self):
        pass

    @abstractmethod
    def reset(self):
        pass

    @abstractmethod
    def save(self):
        pass
