from kfp.dsl import component, Input, Output, Artifact
from config import BASE_IMAGE

@component(base_image=BASE_IMAGE)
def difference(
    num1_artifact: Input[Artifact],
    num2_artifact: Input[Artifact],
    difference_artifact: Output[Artifact],
):
    """Calculates the difference between two numbers passed as artifacts."""
    with open(num1_artifact.path, 'r') as f:
        num1 = float(f.read())
    with open(num2_artifact.path, 'r') as f:
        num2 = float(f.read())

    diff = num1 - num2

    with open(difference_artifact.path, 'w') as f:
        f.write(str(diff))
