from kfp.dsl import component, Input, Output, Artifact

@component(
    base_image='python:3.9',
)
def multiply(
    num1: float,
    num2: float,
    product: Output[Artifact],
):
    """Multiplies two numbers."""
    product_value = num1 * num2
    with open(product.path, 'w') as f:
        f.write(str(product_value))
