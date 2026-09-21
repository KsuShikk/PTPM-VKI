import logging

try:
    a = 10
    for b in range(0, 3):
        logging.info(f"Итерация b = {b}")

        if b == 0:
            logging.warning("Внимание, переменная b инициализирована нулем!")

        logging.debug(f"Выполнение деления {a} на {b}")
        result = a / b
        logging.info(f"Деление {a} на {b} равно {result}")

except ZeroDivisionError as ex:
    # Метод logging.exception() автоматически прикрепляет traceback (стек ошибки)
    logging.error("Что-то пошло не так...")
    logging.exception("Заход в блок обработки исключения:")