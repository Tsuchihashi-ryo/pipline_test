from kfp.dsl import component

@component(
    base_image='python:3.9',
)
def subtract(
    num1: float,
    num2: float,
) -> float:
    """Subtracts two numbers."""
    return num1 - num2
