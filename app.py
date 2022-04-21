from vk_api import VkApi
from vk_api.longpoll import VkLongPoll, VkEventType

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


# asyncio.set_event_loop(modules_event_loop)


imported_modules = import_modules(CONFIG["loaded_modules"])
start_modules(imported_modules, SCRIPT_PATH=SCRIPT_PATH)


while True:
    for event in vk_long_poll.listen():

        event_type = str(event.type)

        if event_type not in events_codes_white_list:
            continue

        execute_modules(
            imported_modules=imported_modules,
            SCRIPT_PATH=SCRIPT_PATH,
            VK_TOKEN=VK_TOKEN,
            event=event,
        )
