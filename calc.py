import re


class Calc:
    def __init__(self):
        self.operators = {'+': 0, '-': 0, '*': 1, '/': 1}

    def operation(self, a, b, operator):
        if operator == '+':
            return a + b
        elif operator == '-':
            return a - b
        elif operator == '*':
            return a * b
        elif operator == '/':
            if b == 0:
                raise ZeroDivisionError("Ты правда хочешь поделить на ноль?")
            return a / b

    def string_check(self, input_exp):
        shablon = r'^[+\-\*\/\(\)\0-9\.\s]+$'  # шаблон: какие символы допустимы в выражении

        skobki = 0
        for el in input_exp:
            if el == '(':
                skobki += 1
            elif el == ')':
                skobki -= 1

        if skobki != 0:  # проверка на работу со скобками
            return None

        return re.match(shablon, input_exp)  # проверка соответствия шаблону

    def symb_priority(self, s1, s2):  # приоритет операций
        return self.operators[s1] >= self.operators[s2]

    def evaluation(self, input_exp):  # реализация вычисления через работу со стэками
        if not self.string_check(input_exp):  # проверяем валидность введенного выражение
            raise TypeError("Недопустимые символы или проблема со скобками")
        num_stack = []
        operators_stack = []
        i = 0

        while i < len(input_exp):
            if input_exp[i].isdigit() or input_exp[i] == '.':  # заполняем стэк значений
                num = ''
                while i < len(input_exp) and (input_exp[i].isdigit() or input_exp[i] == '.'):
                    num += input_exp[i]
                    i += 1
                num_stack.append(float(num))
                i -= 1
            elif input_exp[i] in self.operators:  # пополняем стэк операций
                while operators_stack and operators_stack[-1] != '(' and self.symb_priority(operators_stack[-1],
                                                                                            input_exp[i]):
                    operator = operators_stack.pop()
                    b = num_stack.pop()
                    a = num_stack.pop()
                    num_stack.append(self.operation(a, b, operator))
                operators_stack.append(input_exp[i])
            elif input_exp[i] == '(':
                operators_stack.append(input_exp[i])
            elif input_exp[i] == ')':
                while operators_stack and operators_stack[-1] != '(':  # при закрытии скобок выражение внутри вычисляется
                    operator = operators_stack.pop()
                    b = num_stack.pop()
                    a = num_stack.pop()
                    num_stack.append(self.operation(a, b, operator))
                operators_stack.pop()
            i += 1

        while operators_stack:  # по порядку вычисляем результаты выражений
            operator = operators_stack.pop()
            b = num_stack.pop()
            a = num_stack.pop()
            num_stack.append(self.operation(a, b, operator))

        return num_stack[0]

