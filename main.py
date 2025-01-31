import requests
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

def get_headers():
    return Headers(browser='firefox', os='win').generate()

def get_vacancies(url):
    vacancies = []

    headers = get_headers()

    response = requests.get(url, headers=headers)
    response.raise_for_status()  
    print("Главная страница загружена успешно")

    soup = BeautifulSoup(response.text, 'lxml')

    
    vacancy_items = soup.find_all('div', class_='vacancy-serp-item')  
    print(f"Найдено {len(vacancy_items)} вакансий")

    for item in vacancy_items:
        link_tag = item.find('a', class_='bloko-link')  
        if not link_tag:
            continue

        link = link_tag['href']
        title = link_tag.text.strip()

        company_tag = item.find('a', class_='bloko-link bloko-link_secondary')  
        company = company_tag.text.strip() if company_tag else 'Не указано'

        city_tag = item.find('div', class_='vacancy-serp-item__address')  
        city = city_tag.text.strip() if city_tag else 'Не указан'

        salary_tag = item.find('div', class_='vacancy-serp-item__compensation')  
        salary = salary_tag.text.strip() if salary_tag else 'Не указана'

        print(f"Проверка вакансии: {title}")

        
        full_link = urllib.parse.urljoin(url, link)

        vacancy_response = requests.get(full_link, headers=headers)
        vacancy_response.raise_for_status()
        vacancy_soup = BeautifulSoup(vacancy_response.text, 'lxml')
        description_tag = vacancy_soup.find('div', {'data-qa': 'vacancy-description'})
        description = description_tag.text if description_tag else ''

        if 'Django' in description and 'Flask' in description:
            print(f"Найдена подходящая вакансия: {title}")
            vacancies.append({
                'link': full_link,
                'salary': salary,
                'company': company,
                'city': city
            })

    return vacancies

url = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'
vacancies = get_vacancies(url)

with open('vacancies.json', 'w', encoding='utf-8') as f:
    json.dump(vacancies, f, ensure_ascii=False, indent=4)

print("Вакансии сохранены в файл vacancies.json")
