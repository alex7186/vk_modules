import logging
from back.print_manager import mprint


async def module_start(SCRIPT_PATH, vk_session_api):
    mprint("message_logger : initializing with path " + SCRIPT_PATH)
    logging.basicConfig(
        filename=f"{SCRIPT_PATH}/modules/message_logger/logfile.txt",
        filemode="a",
        format="%(asctime)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO,
    )


async def module_execute(SCRIPT_PATH, event, vk_session_api):
    event_type_new_message = str(event.type) == "VkEventType.MESSAGE_NEW"
    event_type_edited = str(event.type) == "VkEventType.MESSAGE_EDIT"
    event_from_user = event.from_user
    event_app_prefix_found = event.text.startswith("-&gt;")

    if event_app_prefix_found:
        return None

    elif event_type_new_message and event_from_user:
        logging_info_str = ""

        logging_info_str += f"Message {event.text}::: "
        logging_info_str += f"{event.message_id}::: "
        logging_info_str += f"{event.user_id}::: "
        logging_info_str += f"{event.peer_id}::: "
        logging.info(logging_info_str)

    elif event_type_edited and event_from_user:
        logging_info_str = ""

        logging_info_str += f"Edited {event.text}::: "
        logging_info_str += f"{event.message_id}::: "
        logging_info_str += f"{event.user_id}::: "
        logging_info_str += f"{event.peer_id}::: "
        logging.info(logging_info_str)
