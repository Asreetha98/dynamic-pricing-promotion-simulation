# Decision persistence is performed by pricing_engine.calculate_price.
# This module is reserved for later policy orchestration and decision explanations.
def explain_decision(decision: dict) -> str:
    return f"{decision['decision']}: {decision['reason']}"
