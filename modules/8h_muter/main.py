import random

# backend default modules
from back.config_manager import get_config
from back.vk_manager import send_vk_message_api, set_vk_silent_api

CONFIG = None


async def module_start(SCRIPT_PATH):
    global CONFIG

    CONFIG = get_config(
        SCRIPT_PATH=SCRIPT_PATH,
        full_file_path=f"{SCRIPT_PATH}/modules/8h_muter/config.json",
    )


async def module_execute(SCRIPT_PATH, event, vk_session_api):
    global CONFIG

    message_from_target_user = str(event.user_id) in CONFIG["vk_ids_to_restrict"]
    correct_time = (event.datetime.hour >= 20) or (event.datetime.hour <= 8)

    if message_from_target_user and correct_time and (not event.from_me):

        # notifications.markAsViewed
        set_vk_silent_api(
            vk_session_api=vk_session_api,
            peer_id=event.user_id,
            timeout_seconds=CONFIG["mute_timeout_seconds"],
            sound_mute=0,
        )

        if random.randint(0, 30) > 20:

            message = ""
            message += "TypeError: '<' not supported between"
            message += "instances of 'NoneType' and 'int'"

            send_vk_message_api(
                vk_session_api=vk_session_api,
                peer_id=event.user_id,
                random_id=0,
                message=message,
            )
