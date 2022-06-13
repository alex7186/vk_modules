from datetime import datetime
import os

# exceptions for vk_longpoll reloading
from socket import timeout as timeout
from urllib3.exceptions import ReadTimeoutError
from requests.exceptions import ReadTimeout

# backend default modules
from back.config_manager import get_config
from back.import_manager import import_modules
from back.import_manager import start_modules, execute_modules
from back.print_manager import mprint
from back.token_manager import get_token
from back.vk_manager import get_vk_variables, status_vk_message_api


SCRIPT_PATH = "/".join(os.path.realpath(__file__).split("/")[:-1])

CONFIG = get_config(SCRIPT_PATH)
VK_TOKEN = get_token(SCRIPT_PATH)
APP_NAME = CONFIG["APP_NAME"]


# importing inlisted modules with importlib
imported_modules = import_modules(modules_list=CONFIG["loaded_modules"])
vk_session_api, vk_long_poll = get_vk_variables(VK_TOKEN, timeout=-1)


# executing the `setup` method of every module
tasks_group = start_modules(
    imported_modules=imported_modules,
    SCRIPT_PATH=SCRIPT_PATH,
    modules_list=CONFIG["loaded_modules"],
    vk_session_api=vk_session_api,
)


status_vk_message_api(vk_session_api=vk_session_api)


while True:
    try:

        for event in vk_long_poll.listen():

            should_react_on_event = str(event.type) in CONFIG["events_codes_white_list"]

            if should_react_on_event:
                # executing modules
                execute_modules(
                    imported_modules=imported_modules,
                    SCRIPT_PATH=SCRIPT_PATH,
                    vk_session_api=vk_session_api,
                    event=event,
                )

    # vk_api library will corrupt all the time
    # the messages.delete method is executed (but still works)
    # so that it`s necessary to ignore this error
    except TypeError:
        pass

    # except OSError:
    #     pass

    # sometimes the longpoll timeout error occure
    # so that its necessary to update vk_session and vk_longpoll variables
    except (timeout, ReadTimeoutError, ReadTimeout):
        vk_session, vk_long_poll = get_vk_variables(VK_TOKEN)

    # to not show extra information when the script is run in manual mode
    except KeyboardInterrupt:
        exit()
