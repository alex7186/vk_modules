from datetime import datetime
import asyncio

# backend default modules
from back.config_manager import get_config
from back.vk_manager import edit_vk_message_api
from back.vk_manager import send_vk_message_api
from back.vk_manager import delete_vk_message_api
from back.print_manager import mprint

CONFIG = None


async def module_start(SCRIPT_PATH, vk_session_api):
    global CONFIG

    CONFIG = get_config(
        full_file_path=f"{SCRIPT_PATH}/modules/status_sheduler/config.json"
    )

    send_vk_message_api(
        vk_session_api=vk_session_api,
        peer_id=CONFIG["vk_master_id"],
        message=CONFIG["bot_prefix"] + "APP : vk_modules : started",
    )


async def module_execute(SCRIPT_PATH, event, vk_session_api):
    global CONFIG

    date = ".".join(str(el) for el in list(datetime.now().date().timetuple())[:3][::-1])
    time = str(datetime.now().time()).split(".")[0]
    date = time + " " + date

    if str(event.type) != "VkEventType.MESSAGE_NEW":
        return None

    MODULE_NAME = CONFIG["MODULE_NAME"]

    event_self_dialog = str(event.peer_id) == str(CONFIG["vk_master_id"])
    event_self_dialog_from_bot = str(event.message).startswith(CONFIG["bot_prefix"])

    # message is from bot, we dont process it to avoid recursion
    if not (not (event_self_dialog_from_bot) and event_self_dialog):
        return None

    reply_message = ""

    # casing the command
    if event.message.strip().lower() == "vk_modules status":
        reply_message = ""
        reply_message += CONFIG["bot_prefix"] + "APP : vk_modules\n"
        reply_message += CONFIG["bot_prefix"] + "🕐 " + date + "\n"
        reply_message += CONFIG["bot_prefix"] + "\tEverything is fine\n"
        reply_message += CONFIG["bot_prefix"] + "\n"
        reply_message += CONFIG["bot_prefix"] + "\tThanks for asking"

        edit_res = edit_vk_message_api(
            vk_session_api=vk_session_api,
            peer_id=CONFIG["vk_master_id"],
            new_message=reply_message,
            old_message_id=event.message_id,
        )
        mprint(MODULE_NAME + " : Status message sent")

        await asyncio.sleep(5)

        delete_vk_message_api(
            vk_session_api=vk_session_api,
            peer_id=CONFIG["vk_master_id"],
            message_ids=event.message_id,
        )
        mprint(MODULE_NAME + " : Status message deleted")
