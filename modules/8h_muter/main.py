import logging

from back.config_manager import get_config

CONFIG = None


async def module_start(SCRIPT_PATH):
    global CONFIG

    CONFIG = get_config(
        SCRIPT_PATH=SCRIPT_PATH,
        full_file_path=f"{SCRIPT_PATH}/modules/8h_muter/config.json",
    )

    print("MODULE 8h_muter INITIALIZED")


async def module_execute(SCRIPT_PATH, event, vk_session):
    global CONFIG

    vk_event_new_message = event.type == "VkEventType.MESSAGE_NEW"
    message_from_target_user = str(event.user_id) in CONFIG["vk_ids_to_restrict"]

    if vk_event_new_message and message_from_target_user:
        vk_session.account.setSilenceMode(
            peer_id=event.user_id, time=CONFIG["mute_timeout_seconds"], sound=0
        )
