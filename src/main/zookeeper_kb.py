# zookeeper_kb.py
"""
Caso de uso: ZOOKEEPER (simplificado)

Dominio:
  - Clasificamos un animal según algunos rasgos:
    * mamífero, ave, carnívoro, ungulado, etc.
"""

from value import Value
from facts import FactBase
from rules import KnowledgeBase
from inference_engine import InferenceEngine


def build_zookeeper_kb() -> KnowledgeBase:
    """
    Construye una KB de ejemplo estilo ZOOKEEPER (versión reducida).
    """
    kb = KnowledgeBase.KnowledgeBase()

    # --- Reglas de tipos generales ---
    # R1: SI tiene_pelo ENTONCES es_mamifero
    kb.addRule(["tiene_pelo"], "es_mamifero")

    # R2: SI da_leche ENTONCES es_mamifero
    kb.addRule(["da_leche"], "es_mamifero")

    # R3: SI tiene_plumas ENTONCES es_ave
    kb.addRule(["tiene_plumas"], "es_ave")

    # R4: SI vuela ∧ pone_huevos ENTONCES es_ave
    kb.addRule(["vuela", "pone_huevos"], "es_ave")

    # R5: SI es_mamifero ∧ come_carne ENTONCES es_carnivoro
    kb.addRule(["es_mamifero", "come_carne"], "es_carnivoro")

    # R6: SI es_mamifero ∧ tiene_pezuñas ENTONCES es_ungulado
    kb.addRule(["es_mamifero", "tiene_pezuñas"], "es_ungulado")

    # --- Reglas de animales concretos ---
    # R7: SI es_mamifero ∧ es_carnivoro ∧ tiene_manchas ENTONCES es_leopardo
    kb.addRule(["es_mamifero", "es_carnivoro", "tiene_manchas"], "es_leopardo")

    # R8: SI es_mamifero ∧ es_carnivoro ∧ tiene_rayas ENTONCES es_tigre
    kb.addRule(["es_mamifero", "es_carnivoro", "tiene_rayas"], "es_tigre")

    # R9: SI es_ungulado ∧ tiene_rayado_negro_blanco ENTONCES es_cebra
    kb.addRule(["es_ungulado", "tiene_rayado_negro_blanco"], "es_cebra")

    # R10: SI es_ungulado ∧ tiene_cuello_largo ENTONCES es_jirafa
    kb.addRule(["es_ungulado", "tiene_cuello_largo"], "es_jirafa")

    return kb

def forward_example():
    print("=== ZOOKEEPER - FORWARD CHAINING ===")
    kb = build_zookeeper_kb()
    fb = FactBase.FactBase()

    # Hechos de entrada (como si el usuario los hubiera descrito)
    fb.addFact("tiene_pelo", Value.T, "usuario")
    fb.addFact("come_carne", Value.T, "usuario")
    fb.addFact("tiene_manchas", Value.T, "usuario")

    print("\nBase de hechos inicial:")
    print(fb)

    # Ejecutar inferencia hacia adelante
    InferenceEngine.forward(kb, fb)

    print("\nBase de hechos después de FORWARD:")
    print(fb)

    # Explicar cómo se supo que es_leopardo
    print("\nExplicación de 'es_leopardo':")
    print(InferenceEngine.how(fb, "es_leopardo"))

def backward_example():
    print("\n=== ZOOKEEPER - BACKWARD CHAINING ===")
    kb = build_zookeeper_kb()
    fb = FactBase.FactBase()

    # En backward partimos de pocos hechos conocidos
    fb.addFact("tiene_pezuñas", Value.T, "usuario")
    fb.addFact("tiene_rayado_negro_blanco", Value.T, "usuario")

    goal = "es_cebra"
    print(f"\nObjetivo: demostrar '{goal}'")

    InferenceEngine.backward(kb, fb, goal)

    print("\nBase de hechos final:")
    print(fb)

    print("\nExplicación de 'es_cebra':")
    print(InferenceEngine.how(fb, goal))


if __name__ == "__main__":
    forward_example()
    backward_example()
