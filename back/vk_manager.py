from vk_api.exceptions import Captcha


def send_vk_message(vk_session, peer_id, message):
    try:
        res = vk_session.method(
            method="messages.send",
            values={
                "peer_id": peer_id,
                "message": message,
                "random_id": 0,
            },
        )
    except Captcha:
        pass

    return res


def edit_vk_message(
    vk_session, new_message, old_message_id, peer_id, disable_mentions=1
):
    res = vk_session.method(
        method="messages.edit",
        values={
            "peer_id": peer_id,
            "message": new_message,
            "message_id": old_message_id,
            "disable_mentions": disable_mentions,
        },
    )

    return res


def send_vk_message_api(vk_session_api, peer_id, message):
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
