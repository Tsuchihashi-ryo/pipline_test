from kfp.dsl import pipeline
from kfp import compiler

# Import component functions directly from their Python files
from components.multiply_component import multiply
from components.add_component import add
from components.difference_component import difference
from components.sigmoid_component import sigmoid

@pipeline(
    name='calculation-difference-sigmoid-pipeline',
    description='A pipeline that multiplies and adds two numbers, calculates the difference, and then applies the sigmoid function.'
)
def calculation_pipeline(
    num1: float = 10,
    num2: float = 5,
):
    """
    Defines the calculation pipeline using custom Docker components.
    """
    # Create tasks from the imported component functions
    multiply_task = multiply(num1=num1, num2=num2)
    add_task = add(num1=num1, num2=num2)

    difference_task = difference(
        num1_artifact=multiply_task.outputs['product_artifact'],
        num2_artifact=add_task.outputs['sum_artifact']
    )

    sigmoid_task = sigmoid(
        input_artifact=difference_task.outputs['difference_artifact']
    )

if __name__ == '__main__':
    compiler.Compiler().compile(
        pipeline_func=calculation_pipeline,
        package_path='calculation_pipeline.json'
    )
