# Vacancy Salary Analyzer

Этот проект предназначен для анализа зарплат по вакансиям, извлеченным из файла Excel с названиями вакансий. Он использует API hh.ru для получения данных о вакансиях и анализирует диапазоны зарплат, чтобы предоставить минимальные, максимальные и средние значения зарплат по каждой вакансии.

## Описание

Проект включает в себя:

- Чтение данных о вакансиях из файла Excel.
- Получение данных о вакансиях с помощью API hh.ru.
- Анализ зарплат по вакансиям.
- Сохранение результатов в JSON файл и последующее преобразование их в Excel.

## Установка

1. Клонируйте репозиторий:

    ```bash
    git clone https://github.com/gremvanek/https---github.com-gremvanek-Vacancy-Salary
    cd <Папка с репозиторием>
    ```

2. Установите необходимые библиотеки:

    ```bash
    pip install pandas requests openpyxl
    ```

## Использование

1. Подготовьте файл `vacancies.xlsx` с названиями вакансий в первом столбце.

2. Запустите скрипт `main.py`:

    ```bash
    python main.py
    ```

3. Результаты будут сохранены в два файла:
    - `vacancy_salaries.json`: JSON файл с анализом зарплат.
    - `vacancy_salaries.xlsx`: Excel файл с данными о зарплатах.

## Скрипт `services.py`

Скрипт `services.py` содержит функции для получения данных о вакансиях с API hh.ru и анализа зарплат.

```python
import time
import requests

# Функция для получения данных с hh.ru по вакансиям
def get_vacancies_data(vacancy_title):
    url = 'https://api.hh.ru/vacancies'
    params = {
        'text': vacancy_title,
        'area': 1,  # Москва
        'per_page': 100,
    }
    response = requests.get(url, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Ошибка {response.status_code} при получении данных для вакансии '{vacancy_title}'")
        return None

# Функция для анализа зарплат
def analyze_salaries(vacancies):    
    if vacancies is None:
        return None
    
    salaries = []
    for vacancy in vacancies:
        salary = vacancy.get('salary')
        if salary and salary.get('currency') == 'RUR':
            if salary['from'] and salary['to']:
                salaries.append((salary['from'] + salary['to']) / 2)
            elif salary['from']:
                salaries.append(salary['from'])
            elif salary['to']:
                salaries.append(salary['to'])
    if salaries:
        return {
            'min_salary': min(salaries),
            'max_salary': max(salaries),
            'avg_salary': sum(salaries) / len(salaries)
        }
    return None

# Основная функция для сбора данных и сохранения в JSON
def collect_vacancy_salaries(vacancy_titles):
    results = {}
    for title in vacancy_titles:
        print(f"Ищу данные по вакансии: {title}")
        data = get_vacancies_data(title)
        if data:
            salary_analysis = analyze_salaries(data.get('items'))
            if salary_analysis:
                results[title] = salary_analysis
            else:
                results[title] = "Нет данных по зарплатам"
        else:
            results[title] = "Ошибка при получении данных"
        
        # Задержка перед следующим запросом, чтобы не блокировали за частые запросы
        time.sleep(1)
    
    return results

