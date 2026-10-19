import re
import logging
import traceback
import hashlib


# Настройка логирования
logger = logging.getLogger("registration")
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

# Логирование в файл
file_handler = logging.FileHandler(
    "registration.log",
    encoding="utf-8"
)
file_handler.setFormatter(formatter)

# Логирование в консоль
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(console_handler)



# Черный список логинов
BLACKLIST = {
    "admin",
    "administrator",
    "root",
    "user",
    "test",
    "support"
}



# Маскирование пароля
def mask_password(password):
    """
    Возвращает одинаковую строку для одинаковых паролей
    и разные строки для разных паролей.
    """

    return hashlib.sha256(
        password.encode("utf-8")
    ).hexdigest()[:12]



# Проверка телефона
def is_phone(login):
    pattern = r"^\+\d-\d{3}-\d{3}-\d{4}$"
    return re.fullmatch(pattern, login) is not None


# Проверка email
def is_email(login):
    pattern = r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$"
    return re.fullmatch(pattern, login) is not None



# Проверка обычного логина
def is_regular_login(login):
    pattern = r"^[A-Za-z0-9_]+$"

    return (
        len(login) >= 5
        and re.fullmatch(pattern, login) is not None
    )



# Проверка пароля
def validate_password(password):
    # Причина 1
    if len(password) < 7:
        return False, "Пароль должен содержать минимум 7 символов."

    # Только кириллица, цифры и спецсимволы
    allowed_pattern = r"^[А-Яа-яЁё0-9\W_]+$"

    if re.fullmatch(allowed_pattern, password) is None:
        return False, (
            "Пароль содержит недопустимые символы. "
            "Разрешены кириллица, цифры и спецсимволы."
        )

    # Причина 3
    if not re.search(r"[А-ЯЁ]", password):
        return False, "Пароль должен содержать хотя бы одну заглавную букву."

    # Причина 4
    if not re.search(r"[а-яё]", password):
        return False, "Пароль должен содержать хотя бы одну строчную букву."

    # Причина 5
    if not re.search(r"\d", password):
        return False, "Пароль должен содержать хотя бы одну цифру."

    # Причина 6
    if not re.search(r"[^\w\s]", password):
        return False, "Пароль должен содержать хотя бы один спецсимвол."

    return True, ""



# Основная функция регистрации
def register_user(login, password, confirm_password):

    try:

        # Проверка пустого логина
        if not login:
            message = "Логин не может быть пустым."

            logger.warning(
                "Неуспешная регистрация | "
                "login=%s | причина=%s | password=%s",
                login,
                message,
                mask_password(password)
            )

            return False, message


        # Проверка черного списка
        if login.lower() in BLACKLIST:
            message = "Данный логин запрещен."

            logger.warning(
                "Неуспешная регистрация | "
                "login=%s | причина=%s | password=%s",
                login,
                message,
                mask_password(password)
            )

            return False, message


        # Проверка типа логина
        if not (
            is_phone(login)
            or is_email(login)
            or is_regular_login(login)
        ):
            message = (
                "Логин должен быть телефоном, email "
                "или содержать минимум 5 символов "
                "латиницы, цифр и знака '_'."
            )

            logger.warning(
                "Неуспешная регистрация | "
                "login=%s | причина=%s | password=%s",
                login,
                message,
                mask_password(password)
            )

            return False, message


        # Проверка пароля
        password_valid, password_message = validate_password(password)

        if not password_valid:

            logger.warning(
                "Неуспешная регистрация | "
                "login=%s | причина=%s | password=%s",
                login,
                password_message,
                mask_password(password)
            )

            return False, password_message


        # Проверка совпадения паролей
        if password != confirm_password:
            message = "Пароль и подтверждение пароля не совпадают."

            logger.warning(
                "Неуспешная регистрация | "
                "login=%s | причина=%s | password=%s | confirm_password=%s",
                login,
                message,
                mask_password(password),
                mask_password(confirm_password)
            )

            return False, message


        # Успешная регистрация
        logger.info(
            "Успешная регистрация | "
            "login=%s | результат=True | password=%s",
            login,
            mask_password(password)
        )

        return True, ""

    except Exception as error:

        logger.error(
            "Ошибка при регистрации | "
            "login=%s | ошибка=%s | password=%s\n%s",
            login,
            str(error),
            mask_password(password),
            traceback.format_exc()
        )

        return False, "Произошла внутренняя ошибка при регистрации."
result, message = register_user(
    "student_123",
    "Пароль1!",
    "Пароль1!"
)

print("Результат:", result)
print("Сообщение:", message)