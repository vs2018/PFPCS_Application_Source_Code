from abc import ABC, abstractmethod

# Adapted from https://www.python-course.eu/python3_abstract_classes.php
class Model(ABC):
    @abstractmethod
    def evaluate(self):
        pass

    @abstractmethod
    def fit(self):
        pass

    @abstractmethod
    def predict(self):
        pass
