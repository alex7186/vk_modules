import logging


async def module_start(SCRIPT_PATH, vk_session_api):
    logging.basicConfig(
        filename=f"{SCRIPT_PATH}/modules/message_logger/logfile.txt",
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )


async def module_execute(SCRIPT_PATH, event, vk_session_api):
    event_type_new_message = str(event.type) == "VkEventType.MESSAGE_NEW"
    event_from_user = event.from_user

    if event_type_new_message and event_from_user:
        logging_info_str = ""

        logging_info_str += f"Message {event.text}::: "
        logging_info_str += f"{event.message_id}::: "
        logging_info_str += f"{event.user_id}::: "
        logging_info_str += f"{event.peer_id}::: "
        logging.info(logging_info_str)
