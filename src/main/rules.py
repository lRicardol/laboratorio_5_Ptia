# rules.py
from __future__ import annotations

from dataclasses import dataclass
from typing import List

from value import Value
from facts import FactBase


@dataclass
class Rule:
    """
    Definición de una regla:
    - condition: lista de proposiciones (todas unidas por AND)
    - conclusion: proposición que la regla infiere si la condición es verdadera
    """
    condition: List[str]
    conclusion: str

    @classmethod
    def Rule(cls, condition: List[str], conclusion: str) -> "Rule":
        """
        Crea una nueva regla.
        """
        return cls(condition=list(condition), conclusion=conclusion)

    # ---------------- evaluación semántica ----------------

    def canApply(self, fB: FactBase) -> Value:
        """
        Evalúa la regla a partir de una base de hechos.

        - Si TODAS las condiciones son verdaderas (T) → T
        - Si alguna condición es falsa (F) → F
        - Si ninguna es F pero alguna es U → U
        """
        has_unknown = False
        for prop in self.condition:
            v = fB.getValue(prop)
            if v == Value.F:
                return Value.F
            if v == Value.U:
                has_unknown = True
        if has_unknown:
            return Value.U
        return Value.T

    def getConclusion(self) -> str:
        """
        Devuelve el consecuente de la regla.
        """
        return self.conclusion

    def toString(self) -> str:
        """
        Representación textual de la regla.
        """
        cond_str = " ∧ ".join(self.condition) if self.condition else "TRUE"
        return f"SI {cond_str} ENTONCES {self.conclusion}"

    def __str__(self) -> str:
        return self.toString()


class KnowledgeBase:
    """
    Base de conocimiento: conjunto de reglas.
    """

    def __init__(self) -> None:
        self._rules: List[Rule] = []

    @classmethod
    def KnowledgeBase(cls) -> "KnowledgeBase":
        """
        Crea una base de conocimiento vacía.
        """
        return cls()

    def addRule(self, condition: List[str], conclusion: str) -> None:
        """
        Añade una nueva regla.
        """
        self._rules.append(Rule.Rule(condition, conclusion))

    def couldDeduce(self, proposition: str) -> List[Rule]:
        """
        Devuelve las reglas cuyo consecuente es la proposición dada.
        """
        return [r for r in self._rules if r.conclusion == proposition]

    def numRules(self) -> int:
        """
        Número de reglas.
        """
        return len(self._rules)

    def getRule(self, r: int) -> Rule:
        """
        Devuelve la regla con índice r.
        """
        if r < 0 or r >= len(self._rules):
            raise IndexError("Índice de regla fuera de rango")
        return self._rules[r]

    def toString(self) -> str:
        """
        Representación textual completa de la base de reglas.
        """
        if not self._rules:
            return "<Base de conocimiento vacía>"
        lines = [f"R{i+1}: {rule.toString()}" for i, rule in enumerate(self._rules)]
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.toString()
