from asyncio import run, to_thread
from asyncio.tasks import create_task

from core.downloader import MyDownloader as MD


class MyHandler:

    def __init__(self) -> None:
        self.md = MD()
        self.max_parsed_sites:int = 0
    
    async def __check_updates(self) -> None:
        """ ## Проверяет обновления """
        async for d_info in self.md.get_updates():
            current_site, self.max_parsed_sites = d_info
            await to_thread(print, f'Парсим сайт: {current_site}\nСайт №: {self.max_parsed_sites}')
            if self.md.process_done:
                break
        await to_thread(print, f'Всего спарсили сайтов: {self.max_parsed_sites}')

    async def __create_my_tasks(self) -> None:
        """ ## Создаёт задачи на выполнение """
        downloading_task = create_task(self.md.start_downloading())
        check_task = create_task(self.__check_updates())

        await downloading_task
        await check_task

    def start(self) -> None:
        """ ## Запускать весь процесс """
        run(self.__create_my_tasks())