import math

OPERATORS = {
    "+": (1, lambda x, y: x + y),
    "-": (1, lambda x, y: x - y),
    "*": (2, lambda x, y: x * y),
    "/": (2, lambda x, y: x / y),
    "^": (3, lambda x, y: x**y),
    "~": (3, lambda x, y: math.sin(y) * x),
    "@": (3, lambda x, y: math.cos(y) * x),
    "$": (3, lambda x, y: math.tan(y) * x),
    "`": (1, lambda x, y: math.log(y, x)),
}


def eval_dlyadyrakov(formula):
    if formula.count("log") >= 1:
        formula = formula.replace("log", "`")
    if formula.count("cos") >= 1:
        formula = formula.replace("cos", "~")
    if formula.count("tg") >= 1:
        formula = formula.replace("cos", "$")
    if formula.count("cos") >= 1:
        formula = formula.replace("sin", "@")

    def parse(formula_string):
        number = ""
        for s in formula_string:
            if s in "1234567890.":
                number += s
            elif number:
                yield float(number)
                number = ""
            if s in OPERATORS or s in "()":
                yield s
        if number:
            yield float(number)

    def shunting_yard(parsed_formula):
        stack = []
        for token in parsed_formula:
            if token in OPERATORS:
                while stack and stack[-1] != "(" and OPERATORS[token][0] <= OPERATORS[stack[-1]][0]:
                    yield stack.pop()
                stack.append(token)
            elif token == ")":
                while stack:
                    x = stack.pop()
                    if x == "(":
                        break
                    yield x
            elif token == "(":
                stack.append(token)
            else:
                yield token
        while stack:
            yield stack.pop()

    def calc(polish):
        stack = []
        for token in polish:
            if token in OPERATORS:
                y, x = stack.pop(), stack.pop()
                stack.append(OPERATORS[token][1](x, y))
            else:
                stack.append(token)
        return stack[0]

    return calc(shunting_yard(parse(formula)))


while True:
    shodelati = input(
        "\nОператоры: [+, -, *, /, ^]\nФункции: [sin, cos, tg, log, log10, ln]"
        "\nПеревод системы исчисления: [СИ]"
        "\nСвободный ввод: [поставьте ()]"
        "\nВыйти из калькулятора: [ | ]"
        "\nЧто вы хотите сделать?:"
    )
    if shodelati == "+":
        try:
            x = int(input("введите первое значение"))
            y = int(input("введите второе значение"))
            if type(x) == int or type(y) == int:
                print(x + y)
            else:
                print("Ошибка")
        except ValueError:
            print("Обшибочка")
    elif shodelati == "-":
        try:
            x = int(input("введите первое значение"))
            y = int(input("введите второе значение"))

            if type(x) == int or type(y) == int:
                print(x - y)
            else:
                print("Ошибка")
        except ValueError:
            print("Обшибочка")

    elif shodelati == "*":
        try:
            x = int(input("введите первое значение"))
            y = int(input("введите второе значение"))

            if type(x) == int or type(y) == int:
                print(x * y)
            else:
                print("Ошибка")
        except ValueError:
            print("Обшибочка")
    elif shodelati == "/":
        try:
            x = int(input("введите первое значение"))
            y = int(input("введите второе значение"))

            if type(x) == int or type(y) == int:
                if y == 0:
                    print("Ошибка")
                else:
                    print(x / y)
            else:
                print("Ошибка")
        except ValueError:
            print("Обшибочка")
    elif shodelati == "^":
        try:
            x = int(input("введите первое значение"))
            y = int(input("введите второе значение"))

            if type(x) == int or type(y) == int:
                print(x**y)
            else:
                print("Ошибка")
        except ValueError:
            print("Обшибочка")
    elif shodelati == "cos":
        try:
            x = int(input("введите первое значение"))

            if type(x) == int:
                print(math.cos(x))
            else:
                print("Ошибка")
        except ValueError:
            print("Обшибочка")
    elif shodelati == "sin":
        try:
            x = int(input("введите первое значение"))

            if type(x) == int:
                print(math.sin(x))
            else:
                print("Ошибка")
        except ValueError:
            print("Обшибочка")
    elif shodelati == "tan":
        try:
            x = int(input("введите первое значение"))

            if type(x) == int:
                print(math.tan(x))
            else:
                print("Ошибка")
        except ValueError:
            print("Обшибочка")
    elif shodelati == "log":
        try:
            x = int(input("введите число"))
            y = int(input("введите основание"))

            if type(x) == int or type(y) == int:
                if x <= 0:
                    print("Ошибка")
                else:
                    print(math.log(x, y))
            else:
                print("Ошибка")
        except ValueError:
            print("Обшибочка")
    elif shodelati == "log10":
        try:
            x = int(input("введите число"))

            if type(x) == int:
                if x <= 0:
                    print("Ошибка")
                else:
                    print(math.log(x, 10))
            else:
                print("Ошибка")
        except ValueError:
            print("Обшибочка")
    elif shodelati == "ln":
        try:
            x = int(input("введите число"))

            if type(x) == int:
                if x <= 0:
                    print("Ошибка")
                else:
                    print(math.log(x))
            else:
                print("Ошибка")
        except ValueError:
            print("Обшибочка")
    elif shodelati == "()":
        try:
            print(eval_dlyadyrakov(input("введите пример:")))
        except ValueError:
            print("Обшибочка")
    elif shodelati == "СИ":
        try:
            num = int(input("введите число"))
            base = int(input("система исчисления (2-9): "))
            if not (2 <= base <= 9):
                print("Ошибка")
            nn = ""

            while num > 0:
                nn = str(num % base) + nn
                num //= base
            print(nn)
        except ValueError:
            print("Обшибочка")
    elif shodelati == "|":
        quit()
    else:
        print("Ошибка")
#  PUT YOUR CODE HERE
