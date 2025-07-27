# allowed chats for bot
from config import BASE_DIR
from json import loads

class AllowedGroup():
    with open(str(BASE_DIR)+"/allowed_group.json", "r") as file:
        adm_json = file.read()
    group_dict: dict = loads(adm_json)
    GROUP = int(group_dict['group'])
    if not GROUP: GROUP = -4001241424 # Если файл пустой, то присваиваем тестовую группу

    @staticmethod
    def chat_allowed(chat_id: int):
        return chat_id == AllowedGroup.GROUP