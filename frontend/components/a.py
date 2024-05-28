import pandas as pd
pd.read_csv(r"C:\Users\Sveta\Downloads\RLT.Hack-29.09-10.01.2023-main\data\inn_list.csv")
import csv
import json

def csv_to_json(csv_file, json_file):
    # Открываем CSV-файл для чтения
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        # Создаем читатель CSV
        csv_reader = csv.DictReader(file)
        
        # Создаем список для хранения данных
        data = []
        
        # Проходим по каждой строке CSV и добавляем данные в список
        for row in csv_reader:
            data.append(row['inn'])

    # Записываем данные в JSON-файл
    with open(json_file, mode='w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

# Указываем пути к CSV- и JSON-файлам
csv_file = r'C:\Users\Sveta\Downloads\RLT.Hack-29.09-10.01.2023-main\frontend\components\inn_list.csv'
json_file = r'C:\Users\Sveta\Downloads\RLT.Hack-29.09-10.01.2023-main\frontend\components\inn_list..json'

# Вызываем функцию для преобразования CSV в JSON
csv_to_json(csv_file, json_file)

print(f'Файл {csv_file} успешно преобразован в {json_file}.')
