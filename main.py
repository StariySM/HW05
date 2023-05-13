import aiohttp
import asyncio
import sys
import platform
from datetime import datetime, timedelta


def get_date(n):
    date_now = datetime.now()
    return list(map(lambda x: datetime.strftime(date_now - timedelta(days=x + 1), '%d.%m.%Y'), range(n)))


async def index(session, i):
    url = f'https://api.privatbank.ua/p24api/exchange_rates?json&date={i}'
    async with session.get(url) as response:
        # print("Status:", response.status)
        # print("Content-type:", response.headers['content-type'])
        result = await response.json()
        return result


def currency_result(result: list, currency_list):
    currency_result = []
    for res in result:
        day_result = {}
        for i in res['exchangeRate']:
            if i['currency'] in currency_list:
                day_result.update({i['currency']: {'sale': i['saleRateNB'], 'purchase': i['purchaseRateNB']}})
        currency_result.append({res['date']: day_result})
    return currency_result


def check(n):
    while n > 10:
        print("max request for 10 days")
        n = int(input("input number from 1 to 10: "))
    else:
        return n


async def main(n=5, currency_list=['EUR', 'USD']):
    n = check(n)
    async with aiohttp.ClientSession() as session:
        try:
            result = await asyncio.gather(*(index(session, i) for i in get_date(n)))
        except Exception as err:
            print(f'Connection error:', str(err))
        else:
            return currency_result(result, currency_list)


if __name__ == "__main__":
    n = int(sys.argv[1])
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    r = asyncio.run(main(n))

    print(r)
