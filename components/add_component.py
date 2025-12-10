from kfp.dsl import component, Input, Output, Artifact

@component(
    base_image='python:3.9',
)
def add(
    num1: float,
    num2: float,
    sum_result: Output[Artifact],
):
    """Adds two numbers."""
    sum_value = num1 + num2
    with open(sum_result.path, 'w') as f:
        f.write(str(sum_value))
