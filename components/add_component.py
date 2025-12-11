from kfp.dsl import component, Output, Artifact
from config import BASE_IMAGE

@component(base_image=BASE_IMAGE)
def add(
    num1: float,
    num2: float,
    sum_artifact: Output[Artifact],
):
    """Adds two numbers and saves the result to an artifact."""
    total = num1 + num2
    with open(sum_artifact.path, 'w') as f:
        f.write(str(total))
