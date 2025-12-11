from kfp.dsl import component

@component(
    base_image='python:3.9',
    packages_to_install=['scipy']
)
def hypotenuse(
    side1: float,
    side2: float,
) -> float:
    """
    Calculates the hypotenuse of a right triangle given its two sides.
    This component demonstrates installing a third-party library (scipy).
    """
    import numpy as np
    # Using scipy.linalg.norm is equivalent to math.sqrt(side1**2 + side2**2)
    # We use it here to demonstrate a scipy dependency.
    hypotenuse_length = np.hypot(side1, side2)
    return float(hypotenuse_length)
