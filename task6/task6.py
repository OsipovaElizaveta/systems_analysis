# -*- coding: cp1251 -*-
import json
import numpy as np


def membership_function(value, points):
    """��������� ������� �������������� �������� ������� �������������� (�������� ������������)."""
    for i in range(len(points) - 1):
        x1, y1 = points[i]
        x2, y2 = points[i + 1]
        if x1 <= value <= x2:
            # �������� ������������
            return y1 + (value - x1) * ((y2 - y1) / (x2 - x1))
    return 0


def fuzzy_control(temp_membership_json, heat_membership_json, rules_json, current_temp):
    """
    ��������� �������� ��������� ����������.
    
    Args:
        temp_membership_json (str): JSON �� ���������� ������� �������������� �����������.
        heat_membership_json (str): JSON �� ���������� ������� �������������� ������ �������.
        rules_json (str): JSON � ��������� ��������� ����������.
        current_temp (float): ������� �������� �����������.

    Returns:
        float: �������� ������ ������� ����� ��������� ����������.
    """
    # �������������� JSON
    temp_membership = json.loads(temp_membership_json)
    heat_membership = json.loads(heat_membership_json)
    rules = json.loads(rules_json)

    # �������� ����� ��� ������� �����������
    fuzzy_temp = {}
    for term in temp_membership["�����������"]:
        membership_degree = membership_function(current_temp, term["points"])
        if membership_degree > 0:
            fuzzy_temp[term["id"]] = membership_degree

    # ���������� ������ ����������
    fuzzy_output = {}
    for rule in rules:
        if rule[0] in fuzzy_temp:
            temp_degree = fuzzy_temp[rule[0]]
            heat_term = rule[1]
            if heat_term not in fuzzy_output:
                fuzzy_output[heat_term] = 0
            fuzzy_output[heat_term] = max(fuzzy_output[heat_term], temp_degree)

    # �������������� (����������� �����)
    numerator = 0
    denominator = 0

    for term in heat_membership["�����������"]:
        if term["id"] in fuzzy_output:
            membership_degree = fuzzy_output[term["id"]]
            for point in term["points"]:
                x, y = point
                numerator += x * min(y, membership_degree)
                denominator += min(y, membership_degree)

    return numerator / denominator if denominator != 0 else 0


# ������ �������������
temp_membership_json = '''
{
    "�����������": [
        {"id": "�������", "points": [[0,1],[18,1],[22,0],[50,0]]},
        {"id": "���������", "points": [[18,0],[22,1],[24,1],[26,0]]},
        {"id": "�����", "points": [[0,0],[24,0],[26,1],[50,1]]}
    ]
}
'''
heat_membership_json = '''
{
    "�����������": [
        {"id": "�����", "points": [[0,0],[0,1],[5,1],[8,0]]},
        {"id": "��������", "points": [[5,0],[8,1],[13,1],[16,0]]},
        {"id": "����������", "points": [[13,0],[18,1],[23,1],[26,0]]}
    ]
}
'''
rules_json = '''
[
    ["�������", "����������"],
    ["���������", "��������"],
    ["�����", "�����"]
]
'''

current_temp = 20.5
result = fuzzy_control(temp_membership_json, heat_membership_json, rules_json, current_temp)
print(f"����������� ������� �������: {result}")

