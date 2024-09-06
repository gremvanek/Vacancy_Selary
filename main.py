import pandas as pd
import json
import time
from services import get_vacancies_data, analyze_salaries, collect_vacancy_salaries

def main():
    # Чтение данных из Excel файла
    file_path = 'vacancies.xlsx'
    df = pd.read_excel(file_path)

    # Получаем список вакансий из файла
    vacancy_title = df.iloc[:, 0].tolist()

    # Сбор данных
    vacancy_salaries = collect_vacancy_salaries(vacancy_title)

    # Сохранение результата в JSON
    with open('vacancy_salaries.json', 'w', encoding='utf-8') as json_file:
        json.dump(vacancy_salaries, json_file, ensure_ascii=False, indent=4)

    print("Результаты сохранены в файл vacancy_salaries.json")

    # Чтение данных из JSON файла
    with open('vacancy_salaries.json', 'r', encoding='utf-8') as json_file:
        vacancy_data = json.load(json_file)
        
    # Преобразование данных в DataFrame для записи в Excel
    vacancy_list = []
    for vacancy, salaries in vacancy_data.items():
        if isinstance(salaries, dict):  # Если данные о зарплатах существуют
            vacancy_list.append({
                'Вакансия': vacancy,
                'Минимальная зарплата': salaries.get('min_salary'),
                'Максимальная зарплата': salaries.get('max_salary'),
                'Средняя зарплата': salaries.get('avg_salary')
            })
        else:
            vacancy_list.append({
                'Вакансия': vacancy,
                'Минимальная зарплата': None,
                'Максимальная зарплата': None,
                'Средняя зарплата': None
            })

    # Преобразование в DataFrame
    df = pd.DataFrame(vacancy_list)

    # Сохранение данных в Excel файл
    output_file = 'vacancy_salaries.xlsx'
    df.to_excel(output_file, index=False)

    print(f"Данные успешно сохранены в файл {output_file}")

if __name__ == "__main__":
    main()
