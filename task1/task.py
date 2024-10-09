import csv
import sys

def get_cell_value(file_path, row_number, column_number):
    try:
        with open(file_path, mode='r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            rows = list(reader)

            # Проверяем допустимость номера строки и колонки
            if row_number < 1 or row_number > len(rows):
                return "Ошибка: Неверный номер строки."
            if column_number < 1 or column_number > len(rows[0]):
                return "Ошибка: Неверный номер колонки."

            # Поскольку нумерация строк и колонок начинается с 0, отнимаем 1
            value = rows[row_number - 1][column_number - 1]
            return value
    except FileNotFoundError:
        return "Ошибка: Файл не найден."
    except Exception as e:
        return f"Ошибка: {e}"

def main():
    if len(sys.argv) != 4:
        print("Использование: python script.py <путь к файлу> <номер строки> <номер колонки>")
    else:
        file_path = sys.argv[1]
        row_number = int(sys.argv[2])
        column_number = int(sys.argv[3])
        result = get_cell_value(file_path, row_number, column_number)
        print(result)

if __name__ == "__main__":
    main()
