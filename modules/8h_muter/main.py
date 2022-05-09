import random

# exceptions for vk_longpoll reloading
from vk_api.exceptions import Captcha

# backend default modules
from back.config_manager import get_config

CONFIG = None


async def module_start(SCRIPT_PATH):
    global CONFIG

    CONFIG = get_config(
        SCRIPT_PATH=SCRIPT_PATH,
        full_file_path=f"{SCRIPT_PATH}/modules/8h_muter/config.json",
    )


async def module_execute(SCRIPT_PATH, event, vk_session):
    global CONFIG

    message_from_target_user = str(event.user_id) in CONFIG["vk_ids_to_restrict"]
    correct_time = (event.datetime.hour >= 20) or (event.datetime.hour <= 8)

    if message_from_target_user and correct_time and (not event.from_me):
        # notifications.markAsViewed
        vk_session.method(
            method="account.setSilenceMode",
            values={
                "peer_id": event.user_id,
                "time": CONFIG["mute_timeout_seconds"],
                "sound": 0,
            },
        )

        try:
            if random.randint(0, 30) > 20:
                vk_session.method(
                    method="messages.send",
                    values={
                        "peer_id": event.user_id,
                        "random_id": 0,
                        "message": "TypeError: '<' not supported between instances of 'NoneType' and 'int'",
                    },
                )

        except Captcha:
            pass
