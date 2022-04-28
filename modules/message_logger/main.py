import logging


async def module_start(SCRIPT_PATH):
    logging.basicConfig(
        filename=f"{SCRIPT_PATH}/modules/message_logger/logfile.txt",
        filemode="a",
        format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
        datefmt="%H:%M:%S",
        level=logging.INFO,
    )
    print("MODULE message_logger INITIALIZED")


async def module_execute(SCRIPT_PATH, event, vk_session):
    event_type_new_message = event.type != "VkEventType.MESSAGE_NEW"
    event_from_user = event.from_user

    if event_type_new_message and event_from_user:
        logging_info_str = ""

        logging_info_str += f"Message {event.text[:30]}::: "
        logging_info_str += f"id {event.message_id}::: "
        logging_info_str += f"from {event.user_id}::: "
        logging_info_str += f"from_user {event.from_user}::: "
        logging_info_str += f"from_me {event.from_me}"
        logging.info(logging_info_str)
