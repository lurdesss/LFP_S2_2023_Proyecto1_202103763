from abc import ABC, abstractmethod

class Expresion(ABC):
    @abstractmethod
    def interpretar(self, contexto):
        pass
