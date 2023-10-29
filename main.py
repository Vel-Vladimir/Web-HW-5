import platform
import aiohttp
import asyncio
import datetime

URL = 'https://api.privatbank.ua/p24api/exchange_rates?json&date='


async def get_course(date: str):
    url = URL + date
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            result = await response.json()
            return result


async def main(dates: list):
    tasks = []
    for date in dates:
        tasks.append(asyncio.create_task(get_course(date)))
    results = await asyncio.gather(*tasks)
    return formate(results)


def formate(list_dict):
    res = []
    dict_result = {}
    for dict_ in list_dict:
        exchange_rates = dict_['exchangeRate']
        sale_euro, purchase_euro, sale_usd, purchase_usd = None, None, None, None
        for rate in exchange_rates:
            if rate.get('currency') == "USD":
                sale_usd = rate.get('saleRate')
                purchase_usd = rate.get('purchaseRate')
            elif rate.get('currency') == "EUR":
                sale_euro = rate.get('saleRate')
                purchase_euro = rate.get('purchaseRate')
        res.append({dict_['date']: {"EUR": {'sale': sale_euro, 'purchase': purchase_euro},
                                      "USD": {'sale': sale_usd, 'purchase': purchase_usd},}})
    return res


if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    time_step = 3
    dates = [datetime.datetime.strftime((datetime.date.today() - datetime.timedelta(days=i)), '%d.%m.%Y') for i in range(time_step)]
    print(dates)
    results = asyncio.run(main(dates))
    print(results)
