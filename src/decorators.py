import functools
import logging
import sys
from typing import Any
from typing import Callable
from typing import Optional


def log(filename: Optional[str] = None) -> Callable[[Callable[..., Any]], Callable[..., Any]]:
    """
    Декоратор для логирования начала и конца выполнения функции.

    :param filename: Опциональное имя файла для записи логов. Если None, логируется в консоль.
    :return: Декорированная функция с логированием.
    """

    # Настройка логирования
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)

    # Удаляем старые обработчики
    logger.handlers.clear()

    # Настройка обработчика для логов
    handler: logging.Handler  # Объявляем обработчик как Handler

    if filename:
        handler = logging.FileHandler(filename)
    else:
        handler = logging.StreamHandler(sys.stdout)  # Обработчик для вывода в консоль

    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    def decorator(func: Callable[..., Any]) -> Callable[..., Any]:
        """
        Декоратор для функции, добавляющий логирование.

        :param func: Функция, которую необходимо декорировать.
        :return: Обернутая функция с логированием.
        """

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """
            Обертка для логирования выполнения функции.

            :param args: Позиционные аргументы для передаваемой функции.
            :param kwargs: Именованные аргументы для передаваемой функции.
            :return: Результат выполнения декорируемой функции.
            """

            try:
                logger.info(f'Запуск функции: {func.__name__}, входные параметры: {args}, {kwargs}')
                result = func(*args, **kwargs)
                logger.info(f'Функция: {func.__name__} завершена успешно, результат: {result}')
                return result
            except Exception as e:
                logger.error(
                    f'Функция: {func.__name__} завершена с ошибкой: {type(e).__name__},'
                    f' входные параметры: {args}, {kwargs}'
                )
                raise

        return wrapper

    return decorator
