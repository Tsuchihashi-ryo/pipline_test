from kfp.dsl import component

@component(
    base_image='python:3.9',
)
def add(
    num1: float,
    num2: float,
) -> float:
    """Adds two numbers."""
    return num1 + num2
