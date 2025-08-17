# Admin role
from config import BASE_DIR
from json import loads
from utils.bot_logger import logger

class Admin:
    file_path = str(BASE_DIR) + "/allowed_admins.json"
    try:
        with open(file_path, "r") as file:
            adm_json = file.read()
        admins_dict: dict = loads(adm_json)
        ADMINS = set(admins_dict['admins']) # specify admins' telegram_id list here
    except Exception as e:
        logger.error("allowed admins file is empty. admins list set to default value")
        ADMINS = {203506853, 211524378} # Присваиваем свои ID если файл пустой ли не существует

    @staticmethod
    def is_admin(user_id: int):
        return user_id in Admin.ADMINS