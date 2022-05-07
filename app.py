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

modules_list = CONFIG["loaded_modules"]
imported_modules = import_modules(modules_list=modules_list)
start_modules(imported_modules, SCRIPT_PATH=SCRIPT_PATH, modules_list=modules_list)


def react_on_event(imported_modules, SCRIPT_PATH, vk_session, event):
    execute_modules(
        imported_modules=imported_modules,
        SCRIPT_PATH=SCRIPT_PATH,
        vk_session=vk_session,
        event=event,
    )


while True:
    try:
        for event in vk_long_poll.listen():

            event_type = str(event.type)
            event_confidential = not event.from_group
            should_reatc_on_event = event_type in events_codes_white_list

            if not should_reatc_on_event:  # and event_confidential:
                continue

            react_on_event(
                imported_modules=imported_modules,
                SCRIPT_PATH=SCRIPT_PATH,
                vk_session=vk_session,
                event=event,
            )
    except Exception:
        vk_session = VkApi(token=VK_TOKEN)
        vk_long_poll = VkLongPoll(vk_session)
