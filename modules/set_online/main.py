from back.vk_manager import set_vk_account_online


async def module_start(SCRIPT_PATH, vk_session_api):
    pass


async def module_execute(SCRIPT_PATH, event, vk_session_api):
    event_type_new_message = str(event.type) == "VkEventType.MESSAGE_NEW"
    event_from_user = event.from_user

    set_vk_account_online(vk_session_api)
