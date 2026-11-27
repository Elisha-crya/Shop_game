from rich.console import Console
from rich.table import Table
from rich.table import box
from rich.pretty import pprint
import time
# from rich.progress import track
from rich.panel import Panel
import rich
from random import *

# for i in track(range(13), description = 'Загрузка...'):
    # time.sleep(0.27)

def clear():
    print("\033[2J\033[3J\033[H", end="", flush=True)

ages = {'пожилой': [75, 100], 'взрослый': [30, 74], 'ребенок': [0, 29]}
status = {'Богатый': [75, 100],
          'Состоятельный': [30, 74],
          'Обычный': [0, 29]
}
coff = {'Богатый': 1.6, 'Состоятельный': 1.3, 'Обычный': 1.15}
clients = []
shop_items = {
    1: 'Хлеб',
    2: 'Молоко',
    3: 'Яйца',
    4: 'Мясо'
}
prices = {'Хлеб': 40, 'Молоко': 80, 'Яйца': 100, 'Мясо': 150}
base_price = {
            'Хлеб': {'Закупка': 20, 'Цена': 40},
            'Молоко': {'Закупка': 40, 'Цена': 80},
            'Яйца': {'Закупка': 50, 'Цена': 100},
            'Мясо': {'Закупка': 75, 'Цена': 150}
            }
player = {'cash': 150,
          'level': 1,
          'inventory': {},
          'EXP': 0
}


def employyer(clients, player):
    clients.clear()
    if len(player['inventory']) == 0:
        print('Ваш инвентарь пуст. Сходите на склад и купите что-нибудь!')
    else:
        count = randint(1, 4)
        print(f'Сейчас клиентов: {count}')
        for i in range(count):
            if len(player['inventory']) == 0:
                print(f'Ваш инвентарь пуст. Всё выкупили-и-и-и...! Потеряно клиентов: {count - i}')
                break
            randomizer_stat = randint(0, 100)
            randomizer_age = randint(0, 100)
            for key, (min_item, max_item) in status.items():
                if min_item <= randomizer_stat <= max_item:
                    stat_res = key
            for key, (min_item, max_item) in ages.items():
                if min_item <= randomizer_age <= max_item:
                    age_res = key
            product = choice(list(player['inventory'].keys()))
            clients.append({stat_res: age_res})
            print(f'Клиент {stat_res.lower()} {age_res} хочет купить {product.lower()}.')
            if base_price[product]['Цена'] * coff[stat_res] >= prices[product]:
                print(stat_res, age_res,': Я могу купить это. Покупаю.')

                player['inventory'][product] -= 1
                player['cash'] += prices[product]
                print(f'Вы успешно продали {product.lower()}, ваши деньги: {player['cash']}.')
                if player['inventory'][product] == 0:
                    del player['inventory'][product]
                    print(f'У вас закончился {product.lower()}, сходите и купите ещё!')
            else:
                print(stat_res, age_res,': Я не куплю это, слишком дорого! Я бы купил за цену чуть поменьше...')
        

def buying_items(shop_items, base_price, prices, buy, player):
    if buy in shop_items:
        item = shop_items[buy]
        if player['cash'] >= base_price[item]['Закупка']:
            player['cash'] -= base_price[item]['Закупка']

            print(f'Вы успешно купили {item.lower()}.')
            if item not in player['inventory']:
                player['inventory'][item] = 1
                prices[item] = base_price[item]['Цена']
            else:
                player['inventory'][item] += 1
            print('Ваш инвентарь:', player['inventory'], 'Ваши деньги: ', player['cash'])
    
        else:
            print('У вас недостаточно денег, Вам нужно заработать их! Вам нехватает: ',
                base_price[item]['Закупка'] - player['cash']) 

def change_prices(prices, player):
    print('Ваш инвентарь: ', player['inventory'])
    for tovar, count in player['inventory'].items():
        print(tovar, ': Количество -', count,', Цена -', prices[tovar])
        item = int(input('Изменить этот товар или идем дальше? 1. - Изменим. 2. - Идем дальше. '))
        if item == 1:
            print('Вы изменяете цену', tovar,', Текущая цена: ', prices[tovar])
            change = int(input('Напишите любую цену, которую хотите установить. (числом, без лишних знаков.) '))
            prices[tovar] = change
    clear()

main = int(input('Добро пожаловать в ваш магазин! \n 1. Зайдем в магазин. \n 2. Зайдем на склад за продуктами. \n 3. Сохранимся и выйдем. \n (Выберите цифру от одного до трех.) '))

while main != 3:
    if main == 1:
        shop = int(input('Вы в своем магазине. 1. Поменять цены. 2. Закрыть магазин (сейчас доступен для клиентов). 3. Обслужить клиентов. 4. Выйти из магазина. '))
        while shop != 4:
            if shop == 1:
                change_prices(prices, player)
            elif shop == 3:
                employyer(clients, player)
            shop = int(input('Вы в своем магазине. 1. Поменять цены. 2. Открыть магазин. 3. Обслужить клиентов. 4. Выйти из магазина. '))
    
    elif main == 2:
        buy = int(input('Вы на складе. Что хотите купить: \n 1. Хлеб. \n 2. Молоко. \n 3. Яйца. \n 4. Мясо. \n 5. Уйдем со склада. '))
        while buy != 5:
            buying_items(shop_items, base_price, prices, buy, player)
            buy = int(input('Вы на складе. Что хотите купить: \n 1. Хлеб. \n 2. Молоко. \n 3. Яйца. \n 4. Мясо. \n 5. Уйдем со склада. '))

    clear()
    main = int(input('Добро пожаловать в ваш магазин! \n 1. Зайдем в магазин. \n 2. Зайдем на склад за продуктами. \n 3. Сохранимся и выйдем. \n (Выберите цифру от одного до трех.) '))

print('До свидания! (Игра сохранена.)')