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
def collect_vacancy_salaries(vacancy_title):
    results = {}
    for title in vacancy_title:
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
