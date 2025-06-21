# -*- coding: utf-8 -*-

import os
import sys

from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    MessagingApiBlob,
    RichMenuRequest,
    RichMenuArea,
    RichMenuSize,
    RichMenuBounds,
    URIAction,
    RichMenuSwitchAction,
    CreateRichMenuAliasRequest,
    UpdateRichMenuAliasRequest,
    PostbackAction,
)

from linebot.v3.messaging.exceptions import ApiException
from linebot.v3.messaging.models import UpdateRichMenuAliasRequest

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

configuration = Configuration(access_token=channel_access_token)

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



def rich_menu_object_a_json():
    return {
        "size": {
            "width": 2500,
            "height": 1686
        },
        "selected": False,
        "name": "richmenu-a",
        "chatBarText": "精緻客製化彌月禮品",
        "areas": [
            {
                "bounds": {
                    "x": 843,
                    "y": 0,
                    "width": 818,
                    "height": 216
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-b",
                    "data": "richmenu-changed-to-b"
                }
            },
            {
                "bounds": {
                    "x": 1758,
                    "y": 0,
                    "width": 742,
                    "height": 216
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-c",
                    "data": "richmenu-changed-to-c"
                }
            }
        ]
    }


def rich_menu_object_b_json():
    return {
        "size": {
            "width": 2500,
            "height": 1686
        },
        "selected": False,
        "name": "richmenu-b",
        "chatBarText": "高價黃金回收",
        "areas": [
            {
                "bounds": {
                    "x": 0,
                    "y": 0,
                    "width": 754,
                    "height": 216
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-a",
                    "data": "richmenu-changed-to-a"
                }
            },
            {
                "bounds": {
                    "x": 1758,
                    "y": 0,
                    "width": 742,
                    "height": 216
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-c",
                    "data": "richmenu-changed-to-c"
                }
            },
            {
                "bounds": {
                "x": 1748,
                "y": 1158,
                "width": 752,
                "height": 528
                },
                "action": {
                    "type": "postback",
                    "label": "查詢金價",
                    "data": "action=gold",
                    "displayText": "查詢今日金價"
            }
            }
        ]
    }


def rich_menu_object_c_json():
    return {
        "size": {
            "width": 2500,
            "height": 1686
        },
        "selected": False,
        "name": "richmenu-c",
        "chatBarText": "精美飾品販售中",
        "areas": [
            {
                "bounds": {
                    "x": 0,
                    "y": 225,
                    "width": 755,
                    "height": 500
                },
                "action": {
                    "type": "uri",
                    "uri": "https://www.instagram.com/jinyue.gold/"
                }
            },
            {
                "bounds": {
                    "x": 0,
                    "y": 725,
                    "width": 755,
                    "height": 460
                },
                "action": {
                    "type": "uri",
                    "uri": "https://www.facebook.com/profile.php?id=61575298454165"
                }
            },
            {
                "bounds": {
                    "x": 0,
                    "y": 0,
                    "width": 754,
                    "height": 216
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-a",
                    "data": "richmenu-changed-to-a"
                }
            },
            {
                "bounds": {
                    "x": 847,
                    "y": 0,
                    "width": 818,
                    "height": 216
                },
                "action": {
                    "type": "richmenuswitch",
                    "richMenuAliasId": "richmenu-alias-b",
                    "data": "richmenu-changed-to-b"
                }
            }
        ]
    }


def main():
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_blob_api = MessagingApiBlob(api_client)

        menus = [
            ("a", rich_menu_object_a_json(), "p-01.png"),
            ("b", rich_menu_object_b_json(), "p-02.png"),
            ("c", rich_menu_object_c_json(), "p-03.png")
        ]

        rich_menu_ids = {}

        for key, menu_json, image_file in menus:
            areas = [
                RichMenuArea(
                    bounds=RichMenuBounds(**info["bounds"]),
                    action=create_action(info["action"])
                ) for info in menu_json["areas"]
            ]
            rich_menu_request = RichMenuRequest(
                size=RichMenuSize(**menu_json["size"]),
                selected=menu_json["selected"],
                name=menu_json["name"],
                chat_bar_text=menu_json["chatBarText"],
                areas=areas
            )
            menu_id = line_bot_api.create_rich_menu(rich_menu_request=rich_menu_request).rich_menu_id
            with open(f"./public/{image_file}", 'rb') as image:
                line_bot_blob_api.set_rich_menu_image(
                    rich_menu_id=menu_id,
                    body=bytearray(image.read()),
                    _headers={'Content-Type': 'image/png'}
                )
            rich_menu_ids[key] = menu_id

        # 設定預設選單 A
        line_bot_api.set_default_rich_menu(rich_menu_id=rich_menu_ids["a"])

        # 建立 alias（有就更新）
        create_or_update_alias(line_bot_api, "richmenu-alias-a", rich_menu_ids["a"])
        create_or_update_alias(line_bot_api, "richmenu-alias-b", rich_menu_ids["b"])
        create_or_update_alias(line_bot_api, "richmenu-alias-c", rich_menu_ids["c"])

        print("✅ 所有 Rich Menu 建立與圖片上傳成功！")

if __name__ == "__main__":
    main()
