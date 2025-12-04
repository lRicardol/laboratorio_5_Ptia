from __future__ import annotations

from typing import List
from value import Value
from facts import FactBase
from rules import KnowledgeBase, Rule


class InferenceEngine:
    """
    Motor de inferencia para un sistema basado en reglas.
    Implementa:
    - Razonamiento hacia adelante (forward chaining)
    - Razonamiento hacia atrás (backward chaining)
    - Explicación del valor de una proposición (how)
    """

    @classmethod
    def forward(cls, kB: KnowledgeBase, fB: FactBase) -> FactBase:
        """
        Razonamiento hacia adelante:
        aplica reglas cuyas condiciones son verdaderas y
        añade las conclusiones como nuevos hechos (si no existían).
        Se repite hasta alcanzar punto fijo.
        """
        changed = True
        while changed:
            changed = False
            for rule in [kB.getRule(i) for i in range(kB.numRules())]:
                can = rule.canApply(fB)
                if can == Value.T:
                    concl = rule.getConclusion()
                    if fB.getValue(concl) == Value.U:
                        fB.addFact(concl, Value.T, f"regla: {rule.toString()}")
                        changed = True
        return fB

    @classmethod
    def backward(cls, kB: KnowledgeBase, fB: FactBase, proposition: str) -> FactBase:
        """
        Razonamiento hacia atrás:
        Intenta demostrar la proposición dada usando las reglas.
        Si no se puede, pregunta al usuario.
        """

        if fB.getValue(proposition) != Value.U:
            return fB

        candidate_rules: List[Rule] = kB.couldDeduce(proposition)
        for rule in candidate_rules:
            all_true = True
            for cond in rule.condition:
                v = fB.getValue(cond)

                if v == Value.U:
                    cls.backward(kB, fB, cond)
                    v = fB.getValue(cond)

                if v == Value.U:
                    user_value = fB.askValue(cond)
                    fB.addFact(cond, user_value, "usuario")
                    v = user_value

                if v != Value.T:
                    all_true = False
                    break

            if all_true:
                fB.addFact(proposition, Value.T, f"regla: {rule.toString()}")
                return fB

        if fB.getValue(proposition) == Value.U:
            v = fB.askValue(proposition)
            fB.addFact(proposition, v, "usuario")
        return fB

    @classmethod
    def how(cls, fB: FactBase, proposition: str) -> str:
        """
        Explica cómo se conoce el valor de una proposición.

        :return: texto con valor y fuente, o mensaje de desconocido.
        """
        for i in range(fB.numFacts()):
            fact = fB.getFact(i)
            if fact.proposition == proposition:
                return fact.toString()
        return f"{proposition} es desconocida en la base de hechos."
