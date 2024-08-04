import asyncio

from vkbottle import API


async def create_vk_parser(vk_token, vk_groups, send_message_func):
    await asyncio.sleep(30)

    api = API(token=vk_token)
    last_ids = {}  # Словарь для отслеживания последних ID постов по группам

    while True:
        for group_id in vk_groups:
            await process_group(api, group_id, send_message_func, last_ids)
        await asyncio.sleep(30)  # Пауза между итерациями обработки всех групп


async def get_group_info(api, group_id):
    try:
        group_info = await api.request("groups.getById", {"group_id": int(group_id)})
        if 'response' in group_info and group_info['response']:
            return group_info['response'][0]  # Возвращает первый элемент ответа
    except Exception as e:
        print(f"Error fetching group info from VK: {e}")
    return None


async def get_last_post(api, owner_id):
    try:
        response = await api.request("wall.get", {"owner_id": owner_id, "count": 1})
        if 'response' in response and response['response']['items']:
            return response['response']['items'][0]  # Возвращает первый пост
    except Exception as e:
        print(f"Error fetching last post from VK: {e}")
    return None


async def process_group(api, group_id, send_message_func, last_ids):
    group_info = await get_group_info(api, group_id)
    if not group_info:
        return  # Прекратить обработку, если информация о группе не была получена

    group_name = group_info.get('name', 'Unknown')
    group_screen_name = group_info.get('screen_name', 'unknown')

    last_post = await get_last_post(api, -int(group_id))
    if last_post and (group_id not in last_ids or last_ids[group_id] != last_post['id']):
        last_ids[group_id] = last_post['id']
        group_url = f"https://vk.com/{group_screen_name}"
        data = {
            'from': 'VK',
            'channel_name': group_name,
            'channel_url': group_url,
            'post_text': last_post['text']
        }
        await send_message_func(data)
