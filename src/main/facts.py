# facts.py
from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Optional

from value import Value


@dataclass
class Fact:
    """
    Definición de un hecho bajo el lenguaje establecido.
    Una proposición tiene un nombre, un valor (T, F, U) y una fuente.
    La fuente indica de dónde salió (usuario, regla X, etc.).
    """
    proposition: str
    value: Value
    source: str

    @classmethod
    def Fact(cls, proposition: str, value: Value, source: str) -> "Fact":
        """
        Crea un nuevo hecho.

        :param proposition: nombre de la proposición
        :param value: valor semántico de la proposición
        :param source: fuente del valor (usuario o regla)
        :return: instancia de Fact
        """
        return cls(proposition=proposition, value=value, source=source)

    def toString(self) -> str:
        """
        Devuelve el hecho en lenguaje natural.
        """
        return f"{self.proposition} = {self.value.value} (fuente: {self.source})"

    def __str__(self) -> str:
        return self.toString()


class FactBase:
    """
    Base de hechos del sistema.
    Maneja un conjunto de proposiciones con sus valores y fuentes.
    """

    def __init__(self) -> None:
        self._facts: Dict[str, Fact] = {}

    @classmethod
    def FactBase(cls) -> "FactBase":
        """
        Crea una base de hechos vacía.
        """
        return cls()

    # ---------- operaciones básicas ----------

    def addFact(self, proposition: str, value: Value, source: str) -> None:
        """
        Añade o actualiza un hecho en la base.

        :param proposition: nombre de la proposición
        :param value: valor de la proposición
        :param source: fuente del valor (usuario o regla)
        """
        self._facts[proposition] = Fact.Fact(proposition, value, source)

    def getValue(self, proposition: str) -> Value:
        """
        Obtiene el valor de una proposición.
        Si no existe, se considera desconocido (U).
        """
        fact: Optional[Fact] = self._facts.get(proposition)
        return fact.value if fact is not None else Value.U

    def askValue(self, proposition: str) -> Value:
        """
        Pregunta al usuario por el valor de una proposición
        cuando no se conoce. Se aceptan: 't', 'f', 'u'.
        """
        while True:
            raw = input(
                f"¿Cuál es el valor de '{proposition}'? "
                f"(t=true, f=false, u=unknown): "
            ).strip().lower()
            if raw == "t":
                return Value.T
            if raw == "f":
                return Value.F
            if raw == "u":
                return Value.U
            print("Valor inválido. Responda t / f / u.")

    def numFacts(self) -> int:
        """
        Número de hechos en la base.
        """
        return len(self._facts)

    def getFact(self, idx: int) -> Fact:
        """
        Devuelve el hecho en la posición idx (orden arbitrario).
        Sirve para recorrer la base.

        :param idx: índice entero
        """
        if idx < 0 or idx >= len(self._facts):
            raise IndexError("Índice de hecho fuera de rango")
        return list(self._facts.values())[idx]

    def toString(self) -> str:
        """
        Devuelve representación textual de toda la base de hechos.
        """
        if not self._facts:
            return "<Base de hechos vacía>"
        lines = [f.toString() for f in self._facts.values()]
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.toString()
