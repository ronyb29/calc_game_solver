from behave import *
from the import the, expect

from solver import *

use_step_matcher("re")


@step("I have (?P<steps>.+) steps available")
def step_impl(context, steps):
    """
    :type steps: str
    """
    context.steps = int(steps)


@step("The starting number is (?P<start>.+)")
def step_impl(context, start):
    """
    :type start: str
    """
    context.start = Decimal(start)


@step("the valid operations are (?P<operations>.+)")
def step_impl(context, operations):
    """
    :type operations: str
    """
    context.operations = parse_operations(operations)


@step("the goal is (?P<goal>.+)")
def step_impl(context, goal):
    """
    :type goal: str
    """
    context.goal = Decimal(goal)


@step("I solve the puzzle")
def step_impl(context):
    """
    """
    mgs = MGS(context.start, context.goal, context.steps, context.operations)
    context.solution = mgs.solve()


@step("The solution steps must be (?P<solution>.+)")
def step_impl(context, solution):
    """
    :type solution: str
    """
    parsed_ops = parse_operations(solution)
    print(context.solution)
    print(parsed_ops)
    the(parsed_ops).should.have.length(len(context.solution))
    for i in range(len(context.solution)):
        the(context.solution[i]).should.equal(parsed_ops[i])


@when("I try to parse the step (?P<step>.+)")
def step_impl(context, step):
    """
    :type context: behave.runner.Context
    :type step: str
    """
    context.operation = parse_operation(step)


@then("I should have the parsed operation (?P<literal>.+)")
def step_impl(context, literal):
    """
    :type context: behave.runner.Context
    :type literal: str
    """
    expect(context.operation).should.equal(eval(literal, globals(), locals()))
