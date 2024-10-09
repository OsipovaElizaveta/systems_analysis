import csv
import io
import math

def parse_matrix(csv_str):
    """Парсит CSV строку в матрицу."""
    reader = csv.reader(io.StringIO(csv_str))
    matrix = [list(map(int, row)) for row in reader]
    return matrix

def calculate_entropy(matrix):
    """Вычисляет энтропию структуры графа."""
    num_nodes = len(matrix)
    entropy = 0.0
    
    for j in range(num_nodes):
        for i in range(num_nodes):
            l_ij = matrix[i][j]
            if l_ij == 0:
                continue
            term = l_ij / (num_nodes - 1)
            entropy -= term * math.log2(term)
    
    return round(entropy, 1)

def task(var):
    matrix = parse_matrix(var)
    return calculate_entropy(matrix)

# Пример использования
csv_input = """2,0,2,0,0
0,1,0,0,1
2,1,0,0,1
0,1,0,1,1
0,1,0,0,1"""
result = task(csv_input)
print(result)  # Ожидается примерно 6.5
