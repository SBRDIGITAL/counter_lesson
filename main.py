import traceback
from core.config.config_reader import config

if __name__ == "__main__":
    try:
        token = config.BOT_TOKEN.get_secret_value()
        print(f'\nВесь процесс завершен')

    except:
        traceback.print_exc()