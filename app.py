from vk_api import VkApi
from vk_api.longpoll import VkLongPoll
import os


from back.token_manager import get_token
from back.config_manager import get_config
from back.import_manager import import_modules, start_modules, execute_modules

SCRIPT_PATH = "/".join(os.path.realpath(__file__).split("/")[:-1])
CONFIG = get_config(SCRIPT_PATH)
events_codes_white_list = CONFIG["events_codes_white_list"]


VK_TOKEN = get_token(SCRIPT_PATH)
vk_session = VkApi(token=VK_TOKEN)
vk_long_poll = VkLongPoll(vk_session)


imported_modules = import_modules(CONFIG["loaded_modules"])
print("ALL MODULES IMPORTED")
start_modules(imported_modules, SCRIPT_PATH=SCRIPT_PATH)

while True:
    for event in vk_long_poll.listen():

        event_type = str(event.type)
        event_confidential = (not event.from_group) and (not event.from_group)

        if event_type not in events_codes_white_list:  # and event_confidential:
            continue

        execute_modules(
            imported_modules=imported_modules,
            SCRIPT_PATH=SCRIPT_PATH,
            vk_session=vk_session,
            event=event,
        )
