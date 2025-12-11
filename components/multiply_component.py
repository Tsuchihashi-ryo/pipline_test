from kfp.dsl import component, Output, Artifact
from config import BASE_IMAGE

@component(base_image=BASE_IMAGE)
def multiply(
    num1: float,
    num2: float,
    product_artifact: Output[Artifact],
):
    """Multiplies two numbers and saves the result to an artifact."""
    product = num1 * num2
    with open(product_artifact.path, 'w') as f:
        f.write(str(product))
