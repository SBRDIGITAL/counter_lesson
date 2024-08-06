from typing import List

from asyncio import Event
from asyncio import to_thread, sleep



class MyDownloader:

    def __init__(self) -> None:
        self.process_done:bool = False
        self.parsing_sites:List[str] = ['yandex.ru', 'google.com', 'mail.ru']
        self.pages_counter:int = 0
        self.current_site:str = ''
        self.current_site_index:int = 0
        self.updating_event = Event()

    
    async def get_updates(self):
        """
        ## Возвращает генератор с обновленными данными
        
        ### Return:
            - Generator[tuple[str, int], Any, None]: кортеж с информацией о сайте, который парсим,\
            и количестве страниц, которые спарсили
        """
        while self.process_done is False:
            await self.updating_event.wait()
            yield self.current_site, self.pages_counter, self.current_site_index
        yield self.current_site, self.pages_counter, self.current_site_index

    def __plus_conter(self) -> None:
        """ ## Увеличивает счётчик на +1 """
        self.pages_counter += 1

    def __set_current_site(self, this_site:str, this_site_index: int) -> None:
        """ ## Обновляет значение актуального сайта """
        self.current_site = this_site
        self.current_site_index = this_site_index

    async def start_downloading(self) -> None:
        """ ## Проходит циклом по сайтам """
        for index, site in enumerate(self.parsing_sites):
            try:
                await sleep(0.1)
                # Предположительно спарсили данные
                await to_thread(self.__set_current_site, site, index)
                await to_thread(self.__plus_conter)

                await to_thread(self.updating_event.set)
                await to_thread(self.updating_event.clear)

            except Exception as ex:
                await to_thread(print, f'Произошла ошибка:\n\n{ex}')
        
        self.process_done = True
        await to_thread(self.updating_event.set)
            