# allowed chats for bot
from config import BASE_DIR
from json import loads
import os
from utils.bot_logger import logger

class AllowedGroup:
    file_path = str(BASE_DIR)+"/allowed_group.json"
    try:
        with open(file_path, "r") as file:
            adm_json = file.read()
        group_dict: dict = loads(adm_json)
        GROUP = int(group_dict['group'])
    except Exception as e:
        logger.error("allowed group file is empty. group set to default value")
        GROUP = -4001241424 # Если файл пустой, то присваиваем тестовую группу

    @staticmethod
    def chat_allowed(chat_id: int):
        return chat_id == AllowedGroup.GROUP