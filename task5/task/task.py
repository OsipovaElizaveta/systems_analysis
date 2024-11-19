import json

def find_disagreement_core(ranking1_json, ranking2_json):
    # Преобразуем JSON-строки в списки
    ranking1 = json.loads(ranking1_json)
    ranking2 = json.loads(ranking2_json)

    # Преобразуем вложенные списки в одномерные списки для облегчения сравнения
    flat_ranking1 = [item if isinstance(item, list) else [item] for item in ranking1]
    flat_ranking2 = [item if isinstance(item, list) else [item] for item in ranking2]

    # найдем элементы которые находятся в пересечении двух ранжировок
    disagreements = []

    # Найдем наибольший подмассив без пересечений
    for group1 in flat_ranking1:
        for group2 in flat_ranking2:
            intersection = set(group1) & set(group2)
            if intersection:
                disagreements.append(list(intersection))

    # Преобразуем результат в JSON-строку и возвращаем
    return json.dumps(disagreements)

# Пример использования
ranking1_json = '[1, [2, 3], 4, [5, 6, 7], 8, 9, 10]'
ranking2_json = '[[1, 2], [3, 4, 5], 6, 7, 9, [8, 10]]'

disagreement_core_json = find_disagreement_core(ranking1_json, ranking2_json)
print(disagreement_core_json)  # Ожидаемый вывод: [["8", "9"]]

