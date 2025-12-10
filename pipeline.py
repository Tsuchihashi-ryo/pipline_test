from kfp.dsl import pipeline
from kfp import compiler
from components.multiply_component import multiply
from components.add_component import add
from components.subtract_component import subtract

@pipeline(
    name='calculation-pipeline',
    description='A pipeline that multiplies and adds two numbers, then subtracts the results.'
)
def calculation_pipeline(
    num1: float = 10,
    num2: float = 5,
):
    """
    Defines the calculation pipeline.
    """
    multiply_task = multiply(num1=num1, num2=num2)
    add_task = add(num1=num1, num2=num2)

    subtract_task = subtract(
        num1=multiply_task.output,
        num2=add_task.output
    )

if __name__ == '__main__':
    compiler.Compiler().compile(
        pipeline_func=calculation_pipeline,
        package_path='calculation_pipeline.json'
    )
