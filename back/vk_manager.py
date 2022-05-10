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
    vk_session, peer_id, new_message, old_message_id, disable_mentions=1
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
