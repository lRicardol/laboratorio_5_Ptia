# value.py
from enum import Enum


class Value(Enum):
    """
    Definición semántica de los valores de las proposiciones:
    T: verdadero, F: falso, U: desconocido
    """
    T = "true"
    F = "false"
    U = "unknown"

    def __str__(self) -> str:
        return self.value
