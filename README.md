#Банковское приложение

##Цель проекта 
Цель проекта - предоставление функциональности для фильтрации и сортировки
данных о банковских операциях.

## Установка

1. Клонируйте репозиторий:

   [git clone] (https://github.com:alenkasmith8-cmd/-.git)
   cd bank_operations
   

2. Установите необходимые зависимости (если есть).

## Использование

Импортируйте функции из модуля `processing`:
python
from src.processing import filter_by_state, sort_by_date
data = [...]  # ваш список словарей
executed = filter_by_state(data)  # фильтрация по состоянию 'EXECUTED'
canceled = filter_by_state(data, state='CANCELED')  # фильтрация по состоянию 'CANCELED'
sorted_data = sort_by_date(data)  # сортировка по дате (по умолчанию по убыванию)
```

Примеры
Фильтрация по состоянию
# Пример входных данных
data = [
    {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
    {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'}
]

executed = filter_by_state(data)
print(executed)
Сортировка по дате
sorted_data = sort_by_date(data)
print(sorted_data)

## Шаг 6: Добавление и загрузка изменений в репозиторий

Добавьте и закоммитьте изменения:
bash
git add .
git commit -m "Добавлена функциональность для обработки данных"

Затем выполните `push` в ветку `feature/processing`:
bash
git push origin feature/processing
```