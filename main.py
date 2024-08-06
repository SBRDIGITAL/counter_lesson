import traceback
from core.handler import MyHandler



if __name__ == "__main__":
    try:
        mh = MyHandler()
        mh.start()
        print(f'\nВесь процесс завершен')

    except:
        traceback.print_exc()