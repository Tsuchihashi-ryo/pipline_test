from kfp.dsl import component, Input, Output, Artifact

@component(
    base_image='python:3.9',
)
def subtract(
    num1: float,
    num2: float,
    difference: Output[Artifact],
):
    """Subtracts two numbers."""
    difference_value = num1 - num2
    with open(difference.path, 'w') as f:
        f.write(str(difference_value))
