# -*- coding: utf-8 -*-
import os
import sys
from linebot.v3.messaging import (
    Configuration, ApiClient, MessagingApi, MessagingApiBlob,
    RichMenuRequest, RichMenuArea, RichMenuSize, RichMenuBounds,
    URIAction, RichMenuSwitchAction, PostbackAction,
    CreateRichMenuAliasRequest, UpdateRichMenuAliasRequest
)
from linebot.v3.messaging.exceptions import ApiException

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN')
if not channel_access_token:
    print('缺少 LINE_CHANNEL_ACCESS_TOKEN')
    sys.exit(1)

configuration = Configuration(access_token=channel_access_token)

rich_menus = [
    {
        "alias": "richmenu-alias-a",
        "name": "richmenu-a",
        "chatBarText": "精緻客製化彌月禮品",
        "image": "p-01.png",
        "areas": [
            {"x": 843, "y": 0, "width": 818, "height": 216, "action": {"type": "richmenuswitch", "richMenuAliasId": "richmenu-alias-b", "data": "richmenu-changed-to-b"}},
            {"x": 1758, "y": 0, "width": 742, "height": 216, "action": {"type": "richmenuswitch", "richMenuAliasId": "richmenu-alias-c", "data": "richmenu-changed-to-c"}},
        ]
    },
    {
        "alias": "richmenu-alias-b",
        "name": "richmenu-b",
        "chatBarText": "高價黃金回收",
        "image": "p-02.png",
        "areas": [
            {"x": 0, "y": 0, "width": 754, "height": 216, "action": {"type": "richmenuswitch", "richMenuAliasId": "richmenu-alias-a", "data": "richmenu-changed-to-a"}},
            {"x": 1758, "y": 0, "width": 742, "height": 216, "action": {"type": "richmenuswitch", "richMenuAliasId": "richmenu-alias-c", "data": "richmenu-changed-to-c"}},
            {"x": 1758, "y": 220, "width": 752, "height": 512, "action": {"type": "uri", "uri": "https://line.me/R/app/2007349658-zme8568w"}},
            {"x": 1758, "y": 733, "width": 752, "height": 425, "action": {"type": "postback", "label": "回收流程", "data": "action=recycle", "displayText": "回收流程"}},
            {"x": 1748, "y": 1158, "width": 752, "height": 528, "action": {"type": "postback", "label": "今日金價", "data": "action=gold", "displayText": "今日金價"}},
        ]
    },
    {
        "alias": "richmenu-alias-c",
        "name": "richmenu-c",
        "chatBarText": "精美飾品販售中",
        "image": "p-03.png",
        "areas": [
            {"x": 0, "y": 225, "width": 755, "height": 500, "action": {"type": "uri", "uri": "https://www.instagram.com/jinyue.gold/"}},
            {"x": 0, "y": 725, "width": 755, "height": 460, "action": {"type": "uri", "uri": "https://www.facebook.com/profile.php?id=61575298454165"}},
            {"x": 0, "y": 0, "width": 754, "height": 216, "action": {"type": "richmenuswitch", "richMenuAliasId": "richmenu-alias-a", "data": "richmenu-changed-to-a"}},
            {"x": 847, "y": 0, "width": 818, "height": 216, "action": {"type": "richmenuswitch", "richMenuAliasId": "richmenu-alias-b", "data": "richmenu-changed-to-b"}},
        ]
    }
]

def create_action(action):
    if action['type'] == 'uri':
        return URIAction(uri=action.get('uri'))
    elif action['type'] == 'richmenuswitch':
        return RichMenuSwitchAction(
            rich_menu_alias_id=action.get('richMenuAliasId'),
            data=action.get('data')
        )
    elif action['type'] == 'postback':
        return PostbackAction(
            data=action.get('data'),
            label=action.get('label'),
            display_text=action.get('displayText', '')
        )

def create_or_update_alias(api, alias_id, menu_id):
    try:
        api.create_rich_menu_alias(CreateRichMenuAliasRequest(
            rich_menu_alias_id=alias_id,
            rich_menu_id=menu_id
        ))
    except ApiException as e:
        if "409" in str(e) or "conflict" in str(e).lower():
            api.update_rich_menu_alias(
                alias_id,
                UpdateRichMenuAliasRequest(rich_menu_id=menu_id)
            )
        else:
            raise

def main():
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_blob_api = MessagingApiBlob(api_client)
        rich_menu_ids = {}

        for menu in rich_menus:
            areas = [
                RichMenuArea(
                    bounds=RichMenuBounds(x=a["x"], y=a["y"], width=a["width"], height=a["height"]),
                    action=create_action(a["action"])
                ) for a in menu["areas"]
            ]

            request = RichMenuRequest(
                size=RichMenuSize(width=2500, height=1686),
                selected=False,
                name=menu["name"],
                chat_bar_text=menu["chatBarText"],
                areas=areas
            )

            menu_id = line_bot_api.create_rich_menu(rich_menu_request=request).rich_menu_id
            with open(f"./public/{menu['image']}", 'rb') as image:
                line_bot_blob_api.set_rich_menu_image(
                    rich_menu_id=menu_id,
                    body=image.read(),  # ✅ 改成 bytes
                    _headers={'Content-Type': 'image/png'}
                )
            create_or_update_alias(line_bot_api, menu["alias"], menu_id)
            rich_menu_ids[menu["alias"]] = menu_id

        line_bot_api.set_default_rich_menu(rich_menu_id=rich_menu_ids["richmenu-alias-a"])
        print("✅ 所有 Rich Menu 建立與圖片上傳成功！")

if __name__ == "__main__":
    main()
