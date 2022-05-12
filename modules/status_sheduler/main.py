from datetime import datetime
import asyncio

# backend default modules
from back.config_manager import get_config
from back.vk_manager import edit_vk_message
from back.vk_manager import delete_vk_message_api


full_file_path = None


async def module_start(SCRIPT_PATH):
    global CONFIG

    full_file_path = f"{SCRIPT_PATH}/modules/status_sheduler/config.json"
    CONFIG = get_config(full_file_path=full_file_path)


async def module_execute(SCRIPT_PATH, event, vk_session):
    global CONFIG

    vk_session_api = vk_session.get_api()

    date = ".".join(str(el) for el in list(datetime.now().date().timetuple())[:3][::-1])
    time = str(datetime.now().time()).split(".")[0]
    date = time + " " + date

    if str(event.type) != "VkEventType.MESSAGE_NEW":
        return None

    bot_prefix = CONFIG["bot_prefix"]
    MODULE_NAME = CONFIG["MODULE_NAME"]

    event_self_dialog = str(event.peer_id) == str(CONFIG["vk_master_id"])
    event_self_dialog_from_bot = str(event.message).startswith(bot_prefix)

    # message is from bot, we dont process it to avoid recursion
    if not (not (event_self_dialog_from_bot) and event_self_dialog):
        return None

    reply_message = ""

    # casing the command
    if event.message.strip().lower() == "vk_modules status":
        reply_message = ""
        reply_message += bot_prefix + "APP : vk_modules\n"
        reply_message += bot_prefix + "🕐 " + date + "\n"
        reply_message += bot_prefix + "\tEverything is fine\n"
        reply_message += bot_prefix + "\n"
        reply_message += bot_prefix + "\tThanks for asking"

        edit_res = edit_vk_message(
            vk_session=vk_session,
            peer_id=CONFIG["vk_master_id"],
            new_message=reply_message,
            old_message_id=event.message_id,
        )
        print(MODULE_NAME, ": Status message sent")

        await asyncio.sleep(5)

        delete_vk_message_api(
            vk_session_api=vk_session_api,
            peer_id=CONFIG["vk_master_id"],
            message_ids=event.message_id,
        )
        print(MODULE_NAME, ": Status message deleted")
