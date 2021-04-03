"""This file contains the calculater class as well as auxilliary function and operator classes"""

import re
import numbers
import numpy
import container


class Function:
    """This is the function class, that will be used to implement the calculator"""
    func = None

    def __init__(self, func):
        self.func = func

    def execute(self, element, debug=False):
        """execute the given function"""
        if not isinstance(element, numbers.Number):
            raise TypeError("the element must be a number")

        result = self.func(element)

        if debug is True:
            print(
                "Function: " +
                self.func.name +
                "({:f}) ={:f}".format(
                    element,
                    result))

        return result


class Operator:
    """This is the operator class, that we will use to implement the calculator"""
    operation = None
    strength = None

    def __init__(self, operation, strength):
        self.operation = operation
        self.strength = strength

    def execute(self, element_one, element_two):
        """Execute the given operator"""
        if not (isinstance(element_one, numbers.Number)
                and isinstance(element_two, numbers.Number)):
            raise TypeError("Both elements must be numbers")
        result = self.operation(element_one, element_two)
        return result

    def get_strength(self):
        return self.strength


class Calculator:
    """This is the main calculator class"""
    functions = None
    operators = None
    output_queue = None

    def __init__(self):
        self.functions = {"EXP": Function(numpy.exp),
                          "LOG": Function(numpy.log),
                          "SIN": Function(numpy.sin),
                          "COS": Function(numpy.cos),
                          "SQRT": Function(numpy.sqrt)}
        self.operators = {"ADD": Operator(numpy.add, 0),
                          "MULTIPLY": Operator(numpy.multiply, 1),
                          "DIVIDE": Operator(numpy.divide, 1),
                          "SUBTRACT": Operator(numpy.subtract, 0)}
        self.output_queue = container.Queue()

    def rpn_calculation(self, queue=[]):
        """Calculate input based on RPN syntax"""
        stack = container.Stack()
        for item in queue:
            self.output_queue.push(item)
        for i in range(self.output_queue.size()):
            if isinstance(self.output_queue.peek(), numbers.Number):
                num = self.output_queue.pop()
                stack.push(num)
            elif self.output_queue.peek() in self.functions.keys():
                element = stack.pop()
                func = self.output_queue.pop()
                num = self.functions[func].execute(element)
                stack.push(num)
            elif self.output_queue.peek() in self.operators.keys():
                element2 = stack.pop()
                element1 = stack.pop()
                operator = self.output_queue.pop()
                num = self.operators[operator].execute(element1, element2)
                stack.push(num)
            else:
                print("input not recognised")
        if stack.size() == 1:
            return stack.pop()
        print("input did not result in a final answer")
        return None

    def shunting_yard(self, parsed_input):
        """
        Implementation of the shunting-yarn algorithm,
        to parse normal input to RPN friendly input
        """
        operator_stack = container.Stack()
        for element in parsed_input:
            if isinstance(element, numbers.Number):
                self.output_queue.push(element)
            elif (element in self.functions.keys()) or (element == "("):
                operator_stack.push(element)
            elif element == ")":
                while not operator_stack.peek() == "(":
                    self.output_queue.push(operator_stack.pop())
                if operator_stack.peek() == "(":
                    operator_stack.pop()
                if operator_stack.peek() in self.functions.keys():
                    self.output_queue.push(operator_stack.pop())
            elif element in self.operators.keys():
                stronger = True
                if operator_stack.peek() in self.operators.keys():
                    stronger = self.operators[operator_stack.peek()].get_strength() \
                               < self.operators[element].get_strength()
                while not ((operator_stack.is_empty())
                           or stronger
                           or (operator_stack.peek() == "(")):
                    self.output_queue.push(operator_stack.pop())
                    if operator_stack.peek() in self.operators.keys():
                        stronger = self.operators[operator_stack.peek()].get_strength() \
                                   < self.operators[element].get_strength()
                operator_stack.push(element)
        while not operator_stack.is_empty():
            self.output_queue.push(operator_stack.pop())

    def parse_text(self, text):
        """Parses normal text input, into a list of strings and numbers that
        the shunting_yard algorithm can parse into RPN friendly input"""
        text = text.replace(" ", "").upper()
        patterns = re.compile(r'EXP|LOG|SIN|COS|SQRT|ADD|MULTIPLY|DIVIDE'
                              r'|SUBTRACT|[(]|[)]|[+-]?\d+(?:\.\d+)?')
        parsed_input = re.findall(patterns, text)
        for index in range(len(parsed_input)):
            if parsed_input[index].isnumeric():
                parsed_input[index] = float(parsed_input[index])
        return parsed_input

    def calculate_expression(self, text):
        """Combines the other methods of the calculator"""
        self.shunting_yard(self.parse_text(text))
        return self.rpn_calculation()


class Test:
    """This is a testclass for the classes in this file"""

    def __main__(self):
        exponentialfunc = Function(numpy.exp)
        sinfunc = Function(numpy.sin)
        print(exponentialfunc.execute(sinfunc.execute(0)))
        addop = Operator(numpy.add, 0)
        multiplyop = Operator(numpy.multiply, 1)
        print(addop.execute(1, multiplyop.execute(2, 3)))
        calc = Calculator()
        print(calc.functions["EXP"]
              .execute(calc.operators["ADD"]
                       .execute(1, calc.operators["MULTIPLY"]
                                .execute(2, 3))))
        # print(calc.rpn_calculation([1, 2, 3, "MULTIPLY", "ADD", "EXP"]))
        # calc.shunting_yard(["EXP", "(", 1, "ADD", 2, "MULTIPLY", 3, ")"])
        # print(calc.rpn_calculation())
        # print(calc.parse_text("exp( 1 add 2 multiply 3)"))
        # print(calc.parse_text("((15 DIVIDE (7 SUBTRACT (1 ADD 1))) MULTIPLY 3)SUBTRACT (2 ADD (1 ADD 1))"))
        print(calc.calculate_expression("exp( 1 add 2 multiply 3)"))
        print(calc.calculate_expression("((15 DIVIDE (7 SUBTRACT (1 ADD 1))) MULTIPLY 3)SUBTRACT (2 ADD (1 ADD 1))"))


if __name__ == '__main__':
    Test().__main__()
