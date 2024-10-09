import csv
import io
from collections import defaultdict

def parse_edges(csv_str):
    """Парсит строку CSV в список рёбер."""
    reader = csv.reader(io.StringIO(csv_str))
    return [(int(row[0]), int(row[1])) for row in reader]

def compute_relations(edges, num_nodes):
    """Вычисляет матрицу отношений для графа."""
    relations = [[0] * num_nodes for _ in range(num_nodes)]

    # Заполняем матрицу отношений
    for u, v in edges:
        relations[u-1][v-1] += 1

    return relations

def convert_to_csv(matrix):
    """Конвертирует матрицу в CSV-строку."""
    output = io.StringIO()
    writer = csv.writer(output)
    for row in matrix:
        writer.writerow(row)
    return output.getvalue().strip()

def main(var):
    edges = parse_edges(var)
    
    # Определяем количество узлов, предполагаем, что узлы нумеруются с 1
    num_nodes = max(max(u, v) for u, v in edges)
    
    relations = compute_relations(edges, num_nodes)
    return convert_to_csv(relations)

# Пример использования
csv_input = "1,2\n2,3\n1,3\n3,4\n4,5\n3,5\n2,5"
result = main(csv_input)
print(result)
