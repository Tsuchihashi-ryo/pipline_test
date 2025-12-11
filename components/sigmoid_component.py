from kfp.dsl import component, Input, Output, Artifact
from config import BASE_IMAGE

@component(base_image=BASE_IMAGE)
def sigmoid(
    input_artifact: Input[Artifact],
    output_artifact: Output[Artifact],
):
    """
    Applies the sigmoid function to a number from an artifact.
    This component runs in a custom Docker container with scipy pre-installed.
    """
    from scipy.special import expit

    with open(input_artifact.path, 'r') as f:
        value = float(f.read())

    sigmoid_value = expit(value)

    with open(output_artifact.path, 'w') as f:
        f.write(str(sigmoid_value))
