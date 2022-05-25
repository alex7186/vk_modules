from vk_api.exceptions import Captcha
from vk_api import VkApi
from vk_api.longpoll import VkLongPoll
import time


def get_vk_variables(VK_TOKEN, first_start=False):
    if not first_start:
        time.sleep(6)
    vk_session = VkApi(token=VK_TOKEN)
    vk_session_api = vk_session.get_api()
    vk_long_poll = VkLongPoll(vk_session)

    return vk_session_api, vk_long_poll


def send_vk_message_api(vk_session_api, peer_id, message):
    # exceptions for vk_longpoll reloading
    try:
        vk_session_api.messages.send(
            peer_id=peer_id,
            message=message,
            random_id=0,
        )
    except Captcha:
        pass


def edit_vk_message_api(
    vk_session_api, new_message, old_message_id, peer_id, disable_mentions=1
):
    vk_session_api.messages.edit(
        peer_id=peer_id,
        message=new_message,
        message_id=old_message_id,
        disable_mentions=disable_mentions,
    )


def delete_vk_message_api(
    vk_session_api, message_ids, peer_id, delete_for_all=0, spam=0
):
    vk_session_api.messages.delete(
        delete_for_all=delete_for_all,
        message_ids=message_ids,
        spam=spam,
        peer_id=peer_id,
    )


def set_vk_silent_api(vk_session_api, peer_id, timeout_seconds, sound_mute=0):
    vk_session_api.account.setSilenceMode(
        peer_id=peer_id,
        time=timeout_seconds,
        sound=sound_mute,
    )


def set_vk_account_online(vk_session_api):
    vk_session_api.account.setOnline()
