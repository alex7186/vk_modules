from socket import timeout as timeout
from urllib3.exceptions import ReadTimeoutError
from requests.exceptions import ReadTimeout

from vk_api import VkApi
from vk_api.longpoll import VkLongPoll
import os

from back.token_manager import get_token
from back.config_manager import get_config
from back.import_manager import import_modules, start_modules, execute_modules

SCRIPT_PATH = "/".join(os.path.realpath(__file__).split("/")[:-1])

CONFIG = get_config(SCRIPT_PATH)
VK_TOKEN = get_token(SCRIPT_PATH)

events_codes_white_list = CONFIG["events_codes_white_list"]
modules_list = CONFIG["loaded_modules"]

# importing inlisted modules with importlib
imported_modules = import_modules(modules_list=modules_list)
# executing the `setup` method of every module
start_modules(imported_modules, SCRIPT_PATH=SCRIPT_PATH, modules_list=modules_list)


def get_vk_variables(VK_TOKEN):
    vk_session = VkApi(token=VK_TOKEN)
    vk_long_poll = VkLongPoll(vk_session)

    return vk_session, vk_long_poll


vk_session, vk_long_poll = get_vk_variables(VK_TOKEN)

while True:
    try:
        for event in vk_long_poll.listen():
            # checking if the event is valueable
            should_react_on_event = str(event.type) in events_codes_white_list

            if should_react_on_event:
                # executing modules
                execute_modules(
                    imported_modules=imported_modules,
                    SCRIPT_PATH=SCRIPT_PATH,
                    vk_session=vk_session,
                    event=event,
                )

    # sometimes the longpoll timeout error occure
    # so that its necessary to update vk_session and vk_longpoll variables
    except (timeout, ReadTimeoutError, ReadTimeout):
        vk_session, vk_long_poll = get_vk_variables(VK_TOKEN)
