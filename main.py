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
    CreateRichMenuAliasRequest
)

channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

configuration = Configuration(
    access_token=channel_access_token
)


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


def create_action(action):
    if action['type'] == 'uri':
        return URIAction(uri=action.get('uri'))
    else:
        return RichMenuSwitchAction(
            rich_menu_alias_id=action.get('richMenuAliasId'),
            data=action.get('data')
        )


def main():
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_blob_api = MessagingApiBlob(api_client)

        # 2. Create rich menu A (richmenu-a)
        rich_menu_object_a = rich_menu_object_a_json()
        areas = [
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=info['bounds']['x'],
                    y=info['bounds']['y'],
                    width=info['bounds']['width'],
                    height=info['bounds']['height']
                ),
                action=create_action(info['action'])
            ) for info in rich_menu_object_a['areas']
        ]

        rich_menu_to_a_create = RichMenuRequest(
            size=RichMenuSize(width=rich_menu_object_a['size']['width'],
                              height=rich_menu_object_a['size']['height']),
            selected=rich_menu_object_a['selected'],
            name=rich_menu_object_a['name'],
            chat_bar_text=rich_menu_object_a['chatBarText'],
            areas=areas
        )

        rich_menu_a_id = line_bot_api.create_rich_menu(
            rich_menu_request=rich_menu_to_a_create
        ).rich_menu_id

# 3. Upload image to rich menu A
        with open('./public/p-01.png', 'rb') as image:
            line_bot_blob_api.set_rich_menu_image(
                rich_menu_id=rich_menu_a_id,
                body=bytearray(image.read()),
                _headers={'Content-Type': 'image/png'}
            )

# 4. Create rich menu B (richmenu-b)
        rich_menu_object_b = rich_menu_object_b_json()
        areas = [
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=info['bounds']['x'],
                    y=info['bounds']['y'],
                    width=info['bounds']['width'],
                    height=info['bounds']['height']
                ),
                action=create_action(info['action'])
            ) for info in rich_menu_object_b['areas']
        ]

        rich_menu_to_b_create = RichMenuRequest(
            size=RichMenuSize(width=rich_menu_object_b['size']['width'],
                              height=rich_menu_object_b['size']['height']),
            selected=rich_menu_object_b['selected'],
            name=rich_menu_object_b['name'],
            chat_bar_text=rich_menu_object_b['chatBarText'],
            areas=areas
        )

        rich_menu_b_id = line_bot_api.create_rich_menu(
            rich_menu_request=rich_menu_to_b_create
        ).rich_menu_id

# 5. Upload image to rich menu B
        with open('./public/p-02.png', 'rb') as image:
            line_bot_blob_api.set_rich_menu_image(
                rich_menu_id=rich_menu_b_id,
                body=bytearray(image.read()),
                _headers={'Content-Type': 'image/png'}
            )

# 6. Create rich menu C (richmenu-c)
        rich_menu_object_c = rich_menu_object_c_json()
        areas = [
            RichMenuArea(
                bounds=RichMenuBounds(
                    x=info['bounds']['x'],
                    y=info['bounds']['y'],
                    width=info['bounds']['width'],
                    height=info['bounds']['height']
                ),
                action=create_action(info['action'])
            ) for info in rich_menu_object_c['areas']
        ]

        rich_menu_to_c_create = RichMenuRequest(
            size=RichMenuSize(width=rich_menu_object_c['size']['width'],
                              height=rich_menu_object_c['size']['height']),
            selected=rich_menu_object_c['selected'],
            name=rich_menu_object_c['name'],
            chat_bar_text=rich_menu_object_c['chatBarText'],
            areas=areas
        )

        rich_menu_c_id = line_bot_api.create_rich_menu(
            rich_menu_request=rich_menu_to_c_create
        ).rich_menu_id

# 7. Upload image to rich menu C
        with open('./public/p-03.png', 'rb') as image:
            line_bot_blob_api.set_rich_menu_image(
                rich_menu_id=rich_menu_c_id,
                body=bytearray(image.read()),
                _headers={'Content-Type': 'image/png'}
            )

        
# 8. Set rich menu A as the default rich menu
        line_bot_api.set_default_rich_menu(rich_menu_id=rich_menu_a_id)

# 9. Create rich menu alias A
        alias_a = CreateRichMenuAliasRequest(
            rich_menu_alias_id='richmenu-alias-a',
            rich_menu_id=rich_menu_a_id
        )
        line_bot_api.create_rich_menu_alias(alias_a)

# 10. Create rich menu alias B
        alias_b = CreateRichMenuAliasRequest(
            rich_menu_alias_id='richmenu-alias-b',
            rich_menu_id=rich_menu_b_id
        )
        line_bot_api.create_rich_menu_alias(alias_b)

# 11. Create rich menu alias C
        alias_c = CreateRichMenuAliasRequest(
            rich_menu_alias_id='richmenu-alias-c',
            rich_menu_id=rich_menu_c_id
        )
        line_bot_api.create_rich_menu_alias(alias_c)        
        print('success')


main()
