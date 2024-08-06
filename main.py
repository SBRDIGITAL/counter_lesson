import traceback

from dataclasses import dataclass

from asyncio import run, to_thread, sleep as async_sleep

from aiogram.utils.callback_answer import CallbackAnswerMiddleware
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from core.config.config_reader import config
from core.logging.my_logger import MyLogger





@dataclass
class StartBot:
    logger = MyLogger(name='main_py_logger', is_console=False).get_logger()
    dp = Dispatcher()
    bot = Bot(token=config.BOT_TOKEN.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    def __post_init__(self) -> None:
        """ ## Исполнение методов после инициализации класса """
        self._include_middlwares()
        self._start()

    def _include_middlwares(self) -> None:
        """ ## Подключение мидлвейров """
        self.dp.callback_query(CallbackAnswerMiddleware())

    async def __include_routers(self) -> None:
        """ ## Подключает роуетеры к диспетчеру """
        # await to_thread(self.dp.include_routers,
        #     # Роутеры,
        #     # Роутеры,
        #     # Роутеры,
        #     )

    async def __start(self) -> None:
        """ ## Приватный метод запуска бота """
        try:
            await self.bot.delete_webhook(True)
            await self.dp.start_polling(self.bot)

        except Exception as ex:
            await to_thread(self.logger.error, 'Произошла ошибка: ', exc_info=ex)
        
        finally:
            await async_sleep(0.2)
            await self.bot.session.close()

    def _start(self) -> None:
        """ ## Запуск бота """
        run(self.__start())



if __name__ == "__main__":
    try:
        StartBot()
        
    except KeyboardInterrupt:
        print('Завершение работы по нажатию на ctrl + c')

    except:
        traceback.print_exc()