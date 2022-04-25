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

    if event.type != "VkEventType.MESSAGE_NEW":
        return None

    logging_info_str = f"Message {event.text[:30]}, \
        id {event.message_id}, \
        from {event.user_id}, \
        from_user {event.from_user}, \
        from_me {event.from_me}".replace(
        "         ", " "
    )
    logging.info(logging_info_str)
