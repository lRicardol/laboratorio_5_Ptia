# test_kb.py
"""
Pruebas sencillas del motor de inferencia.
Se pueden ejecutar con:
python -m test.test_kb
desde la raíz (lab_4_ptia).
"""

from src.main import *


def test_forward_minimal():
    kb = build_zookeeper_kb()
    fb = FactBase.FactBase()

    fb.addFact("tiene_pelo", Value.T, "usuario")
    fb.addFact("come_carne", Value.T, "usuario")
    fb.addFact("tiene_rayas", Value.T, "usuario")

    InferenceEngine.forward(kb, fb)

    assert fb.getValue("es_mamifero") == Value.T
    assert fb.getValue("es_carnivoro") == Value.T
    assert fb.getValue("es_tigre") == Value.T


def test_rule_evaluation():
    kb = KnowledgeBase.KnowledgeBase()
    kb.addRule(["a", "b"], "c")

    fb = FactBase.FactBase()
    fb.addFact("a", Value.T, "usuario")
    fb.addFact("b", Value.T, "usuario")

    rule = kb.getRule(0)
    assert rule.canApply(fb) == Value.T


if __name__ == "__main__":
    print("Ejecutando pruebas rápidas...")
    test_forward_minimal()
    test_rule_evaluation()
    print("OK")
