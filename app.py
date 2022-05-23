from datetime import datetime
import os

# exceptions for vk_longpoll reloading
from socket import timeout as timeout
from urllib3.exceptions import ReadTimeoutError
from requests.exceptions import ReadTimeout

# backend default modules
from back.token_manager import get_token
from back.config_manager import get_config
from back.import_manager import import_modules, start_modules, execute_modules
from back.vk_manager import get_vk_variables, send_vk_message_api
from back.print_manager import mprint

SCRIPT_PATH = "/".join(os.path.realpath(__file__).split("/")[:-1])

CONFIG = get_config(SCRIPT_PATH)
VK_TOKEN = get_token(SCRIPT_PATH)
APP_NAME = CONFIG["APP_NAME"]


# importing inlisted modules with importlib
imported_modules = import_modules(modules_list=CONFIG["loaded_modules"])
vk_session_api, vk_long_poll = get_vk_variables(VK_TOKEN, first_start=True)
mprint(APP_NAME + ": Session variables are (re)generated")


# executing the `setup` method of every module
start_modules(
    imported_modules=imported_modules,
    SCRIPT_PATH=SCRIPT_PATH,
    modules_list=CONFIG["loaded_modules"],
    vk_session_api=vk_session_api,
)

if "dialogue_manager" in CONFIG["loaded_modules"]:
    from modules.dialogue_manager.main import CONFIG as CONFIG_dialogue_manager

    send_vk_message_api(
        vk_session_api=vk_session_api,
        peer_id=CONFIG_dialogue_manager["vk_master_id"],
        message=CONFIG_dialogue_manager["bot_prefix"]
        + "vk_modules started at "
        + datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    )


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

    except OSError:
        pass

    # sometimes the longpoll timeout error occure
    # so that its necessary to update vk_session and vk_longpoll variables
    except (timeout, ReadTimeoutError, ReadTimeout):
        vk_session, vk_long_poll = get_vk_variables(VK_TOKEN)

    # to not show extra information when the script is run in manual mode
    except KeyboardInterrupt:
        exit()
