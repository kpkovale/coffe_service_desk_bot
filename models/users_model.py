# Admin role
from config import BASE_DIR
from json import loads

class Admin():
    with open(str(BASE_DIR)+"/allowed_admins.json", "r") as file:
        adm_json = file.read()
    admins_dict: dict = loads(adm_json)
    ADMINS = set(admins_dict['admins']) # specify admins' telegram_id list here
    if ADMINS == {}: ADMINS = 203506853 # Присваиваем свой ID если файл пустой

    def is_admin(user_id: int):
        return user_id in Admin.ADMINS