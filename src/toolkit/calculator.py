from decimal import ROUND_FLOOR, ROUND_HALF_UP, Decimal, InvalidOperation

from toolkit.errors import CalculatorError

# Токенизация

def tokenize(expr: str) -> list[str]:
    """Разбивает выражение на отдельные токены"""
    tokens = []
    number = ""
    i = 0
    while i < len(expr):
        char = expr[i]
        if char.isdigit() or char == ".":
            number += char
            i += 1
        elif char in "*+-()%":
            if number:
                tokens.append(number)
                number = ""
            tokens.append(char)
            i += 1
        elif char == "/":
            if i + 1 < len(expr) and expr[i + 1] == "/":
                if number:
                    tokens.append(number)
                    number = ""
                tokens.append("//")
                i += 2
            else:
                if number:
                    tokens.append(number)
                    number = ""
                tokens.append(char)
                i += 1
        elif char.isspace():
            if number:
                tokens.append(number)
                number = ""
            i += 1
        else:
            raise CalculatorError(f"Недопустимый символ: {char}")
    if number:
        tokens.append(number)
    return tokens


# Валидация

def is_number(value: str) -> bool:
    """Проверяет, является ли строка числом"""
    try:
        Decimal(value)
        return True
    except InvalidOperation:
        return False


def validate(tokens: list[str]) -> None:
    """Проверяет корректность последовательности токенов"""
    if not tokens:
        raise CalculatorError("Пустое выражение")
    expect_number = True
    unary_used = False
    bracket_balance = 0
    for token in tokens:
        if expect_number:
            if is_number(token):
                expect_number = False
                unary_used = False
            elif token in "+-" and not unary_used:
                unary_used = True
                continue
            elif token in "+-" and unary_used:
                raise CalculatorError("Больше одного унарного знака подряд")
            elif token == "(":
                bracket_balance += 1
                unary_used = False
                continue
            else:
                raise CalculatorError("Ожидалось число")
        else:
            if token in ("+", "-", "*", "/", "//", "%"):
                expect_number = True
                unary_used = False

            elif token == ")":
                bracket_balance -= 1
                if bracket_balance < 0:
                    raise CalculatorError("Лишняя закрывающая скобка")
                continue
            else:
                raise CalculatorError("Ожидалась операция")
    if bracket_balance != 0:
        raise CalculatorError("Незакрытая скобка")
    if expect_number:
        raise CalculatorError("Оператор не может быть в конце")


# Вычисления

def to_postfix(tokens: list[str]) -> list[str]:
    """Преобразует токены в постфиксную запись"""
    output: list[str] = []
    operators: list[str] = []
    priors = {
        "u-": 3,
        "u+": 3,
        "*": 2,
        "/": 2,
        "//": 2,
        "%": 2,
        "+": 1,
        "-": 1,
    }
    for i in range(len(tokens)):
        token = tokens[i]
        if is_number(token):
            output.append(token)
        elif token in ("+", "-", "*", "/", "//", "%"):
            if token == "-" and (i == 0 or tokens[i - 1] in ("(","+", "-", "*", "/", "//", "%")):
                token = "u-"
            if token == "+" and (i == 0 or tokens[i - 1] in ("(","+", "-", "*", "/", "//", "%")):
                token = "u+"
            while operators and operators[-1] != "(" and \
                priors[operators[-1]] >= priors[token]:
                output.append(operators.pop())
            operators.append(token)
        elif token == "(":
            operators.append(token)
        elif token == ")":
            while operators[-1] != "(":
                output.append(operators.pop())
            operators.pop()
    while operators:
        output.append(operators.pop())
    return output


def calculate_postfix(postfix: list[str]) -> Decimal:
    """Вычисляет значение выражения в постфиксной записи"""
    stack = []
    for char in postfix:
        if is_number(char):
            stack.append(Decimal(char))
        elif char in ("+", "-", "*", "/", "//", "%"):
            right = stack.pop()
            left = stack.pop()
            if char == "+":
                stack.append(left + right)
            elif char == "-":
                stack.append(left - right)
            elif char == "*":
                stack.append(left * right)
            elif char == "/":
                if right == 0:
                    raise CalculatorError("Деление на 0")
                stack.append(left / right)
            elif char == "//":
                if right == 0:
                    raise CalculatorError("Деление на 0")
                quotient = (left / right).to_integral_value(rounding=ROUND_FLOOR)
                stack.append(quotient)
            else:
                if right == 0:
                    raise CalculatorError("Деление на 0")
                quotient = (left / right).to_integral_value(rounding=ROUND_FLOOR)
                stack.append(left - quotient * right)
        elif char == "u-":
            stack.append(-stack.pop())
        elif char == "u+":
            continue
    if len(stack) != 1:
        raise CalculatorError("Некорректное выражение")
    result = stack[0]
    return result.quantize(Decimal("1e-10"), rounding=ROUND_HALF_UP)


def calculate(expr: str) -> Decimal:
    """Вычисляет математическое выражение и возвращает результат"""
    tokens = tokenize(expr)
    validate(tokens)
    postfix = to_postfix(tokens)
    result = calculate_postfix(postfix)
    return result
