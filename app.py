import asyncio
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


def react_on_event(event, SCRIPT_PATH, vk_session):

    # checking event
    should_react_on_event = str(event.type) in events_codes_white_list

    if should_react_on_event:
        # executing modules
        execute_modules(
            imported_modules=imported_modules,
            SCRIPT_PATH=SCRIPT_PATH,
            vk_session=vk_session,
            event=event,
        )


while True:
    # try:
    # modules_react_tasks = []
    # modules_execution_event_loop = asyncio.new_event_loop()

    for event in vk_long_poll.listen():
        # modules_react_tasks.append(
        #     modules_execution_event_loop.create_task(
        react_on_event(event=event, SCRIPT_PATH=SCRIPT_PATH, vk_session=vk_session)
    #     )
    # )

    # wait_tasks = asyncio.wait(modules_react_tasks)
    # modules_execution_event_loop.run_until_complete(wait_tasks)
    # modules_execution_event_loop.close()


# except Exception:
#     vk_session = VkApi(token=VK_TOKEN)
#     vk_long_poll = VkLongPoll(vk_session)
