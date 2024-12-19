import json
import numpy as np
import argparse


def membership_function(value, points):
    """Вычисляет степень принадлежности значения функции принадлежности (линейная интерполяция)."""
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        if x1 <= value <= x2:
            # Линейная интерполяция
            return y1 + (value - x1) * ((y2 - y1) / (x2 - x1))
    return 0


def fuzzy_control(temp_membership_json, heat_membership_json, rules_json, current_temp):
    """
    Реализует алгоритм нечеткого управления.
    
    Args:
        temp_membership_json (str): JSON со значениями функций принадлежности температуры.
        heat_membership_json (str): JSON со значениями функций принадлежности уровня нагрева.
        rules_json (str): JSON с правилами нечеткого управления.
        current_temp (float): Текущее значение температуры.

    Returns:
        float: Значение уровня нагрева после нечеткого управления.
    """
    # Десериализация JSON
    temp_membership = json.loads(temp_membership_json)
    heat_membership = json.loads(heat_membership_json)
    rules = json.loads(rules_json)

    # Нечеткий вывод для текущей температуры
    fuzzy_temp = {}
    for term in temp_membership["температура"]:
        membership_degree = membership_function(current_temp, term["points"])
        if membership_degree > 0:
            fuzzy_temp[term["id"]] = membership_degree

    # Применение правил управления
    fuzzy_output = {}
    for rule in rules:
        if rule[0] in fuzzy_temp:
            temp_degree = fuzzy_temp[rule[0]]
            heat_term = rule[1]
            if heat_term not in fuzzy_output:
                fuzzy_output[heat_term] = 0
            fuzzy_output[heat_term] = max(fuzzy_output[heat_term], temp_degree)

    # Дефаззификация (центроидный метод)
    numerator = 0
    denominator = 0

    for term in heat_membership["температура"]:
        if term["id"] in fuzzy_output:
            membership_degree = fuzzy_output[term["id"]]
            for point in term["points"]:
                x, y = point
                numerator += x * min(y, membership_degree)
                denominator += min(y, membership_degree)

    return numerator / denominator if denominator != 0 else 0


def main():
    """Основная функция для работы через командную строку."""
    parser = argparse.ArgumentParser(description="Нечеткое управление нагревом.")
    parser.add_argument(
        "temp_membership_file",
        type=str,
        help="Путь к JSON файлу с функциями принадлежности температуры."
    )
    parser.add_argument(
        "heat_membership_file",
        type=str,
        help="Путь к JSON файлу с функциями принадлежности нагрева."
    )
    parser.add_argument(
        "rules_file",
        type=str,
        help="Путь к JSON файлу с правилами управления."
    )
    parser.add_argument(
        "current_temp",
        type=float,
        help="Текущее значение температуры, для которого нужно применить нечеткий контроль."
    )

    args = parser.parse_args()

    # Считывание JSON из файлов
    with open(args.temp_membership_file, "r") as file:
        temp_membership_json = file.read()

    with open(args.heat_membership_file, "r") as file:
        heat_membership_json = file.read()

    with open(args.rules_file, "r") as file:
        rules_json = file.read()

    # Выполнение алгоритма нечеткого управления
    result = fuzzy_control(temp_membership_json, heat_membership_json, rules_json, args.current_temp)
    print(f"Оптимальный уровень нагрева: {result}")


if __name__ == "__main__":
    main()
