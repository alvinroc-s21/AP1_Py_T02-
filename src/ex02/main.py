import asyncio
import aiohttp
import aiofiles
from prettytable import PrettyTable
import os

async def downloading(session, link, path):
    try:
        async with session.get(link) as response:
            if response.status == 200:
                img = await response.read()
                file_name = os.path.join(path, link.split('/')[-1])
                async with aiofiles.open(file_name, 'wb') as f:
                    await f.write(img)
                return link, "Успех"
            else:
                return link, "Ошибка"
    except:
        return link, "Ошибка"

async def main():
    path = input("Введите путь, куда будут сохраняться изображения: ")

    while not os.path.exists(path) or not os.access(path, os.W_OK):
        print("Нет доступа к каталогу или некорректно указан путь. Попробуйте ещё раз.")
        path = input("Введите путь, куда будут сохраняться изображения: ")

    links = []
    while True:
        link = input("Введите ссылку на изображение: ")
        if not link:
            break
        links.append(link)

    print("Загрузка...")

    async with aiohttp.ClientSession() as session:
        res = await asyncio.gather(*[downloading(session, link, path) for link in links])

    table = PrettyTable(["Ссылка", "Статус"])

    for link, status in res:
        table.add_row([link, status])

    print(table)

if __name__ == "__main__":
    asyncio.run(main())