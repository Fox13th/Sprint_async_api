import logging
import sys
import time

logger = logging.getLogger(__name__)


def backoff(err_list, start_sleep_time=0.1, factor=2, border_sleep_time=10, max_tries=5):
    """
    Функция для повторного выполнения функции через некоторое время, если возникла ошибка. Использует наивный экспоненциальный рост времени повтора (factor) до граничного времени ожидания (border_sleep_time)

    Формула:
        t = start_sleep_time * (factor ^ n), если t < border_sleep_time
        t = border_sleep_time, иначе
    :param err_list: кортеж перехватываемых исключений
    :param start_sleep_time: начальное время ожидания
    :param factor: во сколько раз нужно увеличивать время ожидания на каждой итерации
    :param border_sleep_time: максимальное время ожидания
    :param max_tries: максимальное количество итераций
    :return: результат выполнения функции
    """

    def func_wrapper(func):
        def inner(*args, **kwargs):
            iteration = 0
            curr_sleep_time = start_sleep_time

            while iteration < max_tries:
                try:
                    return func(*args, **kwargs)
                except err_list as error:
                    if curr_sleep_time < border_sleep_time:
                        curr_sleep_time = start_sleep_time * factor ** iteration

                    if curr_sleep_time > border_sleep_time:
                        curr_sleep_time = border_sleep_time

                    iteration += 1
                    logging.error(f"Остуствует соединение. Повторное подключение через {curr_sleep_time} сек. "
                                  f"Осталось попыток: {max_tries - iteration} из {max_tries}")
                    logging.error(error)

                    time.sleep(curr_sleep_time)

            sys.exit(1)

        return inner

    return func_wrapper
