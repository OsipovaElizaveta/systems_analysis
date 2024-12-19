import json
import numpy as np
import argparse

# ▎Находит ядро противоречий
def find_S(A, B):
    # Вычисление матриц отношений для A и B
    Y_a = find_Y(A)
    Y_b = find_Y(B)

    # Транспонирование матриц отношений
    Y_ta = np.transpose(Y_a)
    Y_tb = np.transpose(Y_b)

    # Элементное умножение матриц A и B
    Y_AB = np.multiply(Y_a, Y_b)
    Y_tAB = np.multiply(Y_ta, Y_tb)

    # Поиск ядер противоречий
    n = len(Y_a)
    S = [
        (i + 1, j + 1) 
        for i in range(n) 
        for j in range(n) 
        if i < j and Y_AB[i, j] == 0 and Y_tAB[i, j] == 0
    ]

    return S

# ▎Находит матрицу отношений
def find_Y(ranking):
    levels = {}
    
    # Создание словаря уровня из ранжирования
    for i, x in enumerate(ranking):
        if isinstance(x, list):
            for item in x:
                levels[item] = i
        else:
            levels[x] = i
    
    n = len(levels)
    matrix = np.zeros((n, n), dtype=int)

    # Формирование матрицы отношений
    for i in range(1, n + 1):
        for j in range(1, n + 1):
            if levels[j] >= levels[i]:
                matrix[i - 1, j - 1] = 1

    return matrix

# ▎Основная функция
def main(str_A, str_B):
    # Парсинг строк JSON в объекты Python
    A = json.loads(str_A)
    B = json.loads(str_B)

    # Вычисление ядра противоречий
    S = find_S(A, B)
    
    return json.dumps(S)

if __name__ == "__main__":
    # Создаем парсер аргументов командной строки
    parser = argparse.ArgumentParser(description="Обработка двух JSON-файлов.")
    
    parser.add_argument(
        "file_A",
        nargs="?",
        default="task5/A.json",
        help="Путь к первому JSON-файлу (по умолчанию task5/A.json)",
    )
    parser.add_argument(
        "file_B",
        nargs="?",
        default="task5/B.json",
        help="Путь ко второму JSON-файлу (по умолчанию task5/B.json)",
    )

    # Считывание и парсинг файлов JSON
    args = parser.parse_args()
    
    with open(args.file_A, "r") as file:
        str_A = file.read()
    
    with open(args.file_B, "r") as file:
        str_B = file.read()

    # Вывод результата
    print(main(str_A, str_B))
