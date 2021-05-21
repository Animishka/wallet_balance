import os
import asyncio
import requests

import redis


# указываем какие переменные окружения используем
URL_FOR_PARSING = os.getenv("URL_FOR_PARSING")
REDIS_DB = os.getenv("REDIS_DB")

# подключаемся к Redis в роли базы данных, чтобы записывать туда данные
r = redis.StrictRedis(REDIS_DB, db=0)


async def get_balances(url):
    """
    Функция каждые n секунд парсит через API сайта ethplorer.io баланс кошелька по интересующим
    токенам и записывает данные в Redis, заменяя предыдущее значение. Итого, для каждого токена
    всегда в базе Redis только одно актуальное значение.
    """
    while True:
        data = requests.get(url).json()
        await asyncio.sleep(30)
        balance_eth = data['ETH']['balance']
        balance_pht = data['tokens'][0]['balance']
        balance_vin = data['tokens'][1]['balance']
        r.getset('balance_eth', balance_eth)
        r.getset('balance_pht', balance_pht)
        r.getset('balance_vin', balance_vin)


# запуск парсера
if __name__ == '__main__':
    asyncio.run(get_balances(URL_FOR_PARSING))
