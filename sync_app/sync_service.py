from datetime import datetime
import pandas as pd
from notion_client import Client
from loguru import logger

from sync_app.sync_util import *
from xhs_utils.common_util import init
from sync_app.slg_xhs_spider import SlgDataSpider


def spider_note(break_point: str = ''):
    cookies_str, base_path = init()
    if cookies_str is None:
        return False, 'cookies_str is None'
    data_spider = SlgDataSpider()
    note_url = get_xhs_profile_base_url() + get_user_profile() + '?tab=note'
    excel_name = get_user_profile() + '_note_' + datetime.now().strftime('%Y%m%d%H%M%S')

    note_list, success, msg = data_spider.spider_user_all_note(note_url, cookies_str, base_path, 'excel', excel_name,
                                                               break_point)
    return success, msg


def spider_collection(break_point: str = ''):
    cookies_str, base_path = init()
    if cookies_str is None:
        return False, 'cookies_str is None'
    data_spider = SlgDataSpider()
    note_url = get_xhs_profile_base_url() + get_user_profile() + '?tab=fav&subTab=note'
    excel_name = get_user_profile() + '_collection_' + datetime.now().strftime('%Y%m%d%H%M%S')

    note_list, success, msg = data_spider.spider_user_all_collection(note_url, cookies_str, base_path, 'excel',
                                                                     excel_name,
                                                                     break_point)
    return success, msg


def spider_like(break_point: str = ''):
    cookies_str, base_path = init()
    if cookies_str is None:
        return False, 'cookies_str is None'
    data_spider = SlgDataSpider()
    note_url = get_xhs_profile_base_url() + get_user_profile() + '?tab=liked&subTab=note'
    excel_name = get_user_profile() + '_like_' + datetime.now().strftime('%Y%m%d%H%M%S')

    note_list, success, msg = data_spider.spider_user_all_like(note_url, cookies_str, base_path, 'excel',
                                                               excel_name,
                                                               break_point)
    return success, msg


def parse_number(s):
    if isinstance(s, (int, float)):
        return int(s)
    s = str(s).strip()
    if s.endswith('万'):
        num_str = s[:-1]
        try:
            return int(float(num_str) * 10000)
        except ValueError:
            return 0
    try:
        return int(s)
    except ValueError:
        return 0


def import_xls_to_notion(file_path: str):
    logger.info("Starting import for file: {}", file_path)
    notion_token = get_notion_token()
    database_id = get_notion_database_id()
    if not notion_token or not database_id:
        print("Notion token or database ID not configured.")
        return

    try:
        notion = Client(auth=notion_token)

        df = pd.read_excel(file_path)

        # Define required properties
        required_properties = {
            '标题': {'title': {}},
            '笔记id': {'rich_text': {}},
            '笔记url': {'url': {}},
            '笔记类型': {'select': {}},
            '用户id': {'rich_text': {}},
            '用户主页url': {'url': {}},
            '昵称': {'rich_text': {}},
            '头像url': {'url': {}},
            '点赞数量': {'number': {}},
            '收藏数量': {'number': {}},
            '评论数量': {'number': {}},
            '分享数量': {'number': {}},
            '视频封面url': {'url': {}},
            '视频地址url': {'url': {}},
            '图片地址url列表': {'rich_text': {}},
            '标签': {'rich_text': {}},
            '上传时间': {'date': {}},
            'ip归属地': {'rich_text': {}},
            '笔记来源': {'select': {}}
        }

        # Retrieve current database
        database = notion.databases.retrieve(database_id)
        current_properties = database['properties']

        # Find current title property
        current_title_name = None
        for name, prop in current_properties.items():
            if prop['type'] == 'title':
                current_title_name = name
                break

        # 将title类型的属性重命名为「标题」
        if current_title_name and current_title_name != '标题':
            # Rename the title property
            notion.databases.update(
                database_id,
                properties={
                    current_title_name: {
                        "name": '标题'
                    }
                }
            )
            # Refresh current properties
            database = notion.databases.retrieve(database_id)
            current_properties = database['properties']

        # Prepare updated properties
        updated_properties = current_properties.copy()
        for name, config in required_properties.items():
            if name not in current_properties:
                updated_properties[name] = config

        # Update database if necessary
        if updated_properties != current_properties:
            notion.databases.update(database_id, properties=updated_properties)

        filename = os.path.basename(file_path)
        if '_note_' in filename:
            note_from = '笔记'
        elif '_collection_' in filename:
            note_from = '收藏'
        elif '_like_' in filename:
            note_from = '笔记'
        else:
            note_from = '未知'

        for index, row in df.iterrows():
            logger.info(f'处理行 {index + 1}/{len(df)}: 笔记id {row["笔记id"]}')

            # Query for existing page with matching 笔记id
            query_filter = {
                "property": "笔记id",
                "rich_text": {
                    "equals": str(row['笔记id'])
                }
            }
            query_results = notion.databases.query(
                database_id=database_id,
                filter=query_filter
            )['results']
            logger.info(f'找到 {len(query_results)} 个现有页面 for 笔记id {row["笔记id"]}')

            properties = {
                '标题': {
                    'title': [
                        {
                            'text': {
                                'content': str(row['标题'])
                            }
                        }
                    ]
                },
                '笔记id': {
                    'rich_text': [
                        {
                            'text': {
                                'content': str(row['笔记id'])
                            }
                        }
                    ]
                },
                '笔记url': {
                    'url': str(row['笔记url'])
                },
                '笔记类型': {
                    'select': {
                        'name': str(row['笔记类型'])
                    }
                },
                '用户id': {
                    'rich_text': [
                        {
                            'text': {
                                'content': str(row['用户id'])
                            }
                        }
                    ]
                },
                '用户主页url': {
                    'url': str(row['用户主页url'])
                },
                '昵称': {
                    'rich_text': [
                        {
                            'text': {
                                'content': str(row['昵称'])
                            }
                        }
                    ]
                },
                '头像url': {
                    'url': str(row['头像url'])
                },
                '点赞数量': {
                    'number': parse_number(row['点赞数量'])
                },
                '收藏数量': {
                    'number': parse_number(row['收藏数量'])
                },
                '评论数量': {
                    'number': parse_number(row['评论数量'])
                },
                '分享数量': {
                    'number': parse_number(row['分享数量'])
                },
                '视频封面url': {
                    'url': str(row['视频封面url']) if pd.notna(row['视频封面url']) else None
                },
                '视频地址url': {
                    'url': str(row['视频地址url']) if pd.notna(row['视频地址url']) else None
                },
                '图片地址url列表': {
                    'rich_text': [
                        {
                            'text': {
                                'content': str(row['图片地址url列表'])
                            }
                        }
                    ]
                },
                '标签': {
                    'rich_text': [
                        {
                            'text': {
                                'content': str(row['标签'])
                            }
                        }
                    ]
                },
                '上传时间': {
                    'date': {
                        'start': str(row['上传时间'])
                    }
                },
                'ip归属地': {
                    'rich_text': [
                        {
                            'text': {
                                'content': str(row['ip归属地'])
                            }
                        }
                    ]
                },
                '笔记来源': {
                    'select': {
                        'name': note_from
                    }
                }
            }

            # Remove None values for url properties
            if properties['视频封面url']['url'] is None:
                del properties['视频封面url']
            if properties['视频地址url']['url'] is None:
                del properties['视频地址url']

            description = str(row['描述']).strip()
            children = []
            if description:
                children = [
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": description
                                    }
                                }
                            ]
                        }
                    }
                ]

            if query_results:
                # Update existing page
                page_id = query_results[0]['id']
                notion.pages.update(
                    page_id=page_id,
                    properties=properties
                )
                # Update children: clear existing and append new
                existing_blocks = notion.blocks.children.list(page_id)['results']
                for block in existing_blocks:
                    notion.blocks.delete(block['id'])
                if children:
                    notion.blocks.children.append(page_id, children=children)
                logger.info(f'更新页面 {page_id} for 笔记id {row["笔记id"]}')
            else:
                # Create new page
                notion.pages.create(
                    parent={'database_id': database_id},
                    properties=properties,
                    children=children
                )
                logger.info(f'创建新页面 for 笔记id {row["笔记id"]}')
    except Exception as e:
        logger.error('导入失败:{}', e)
        raise e
    finally:
        logger.info("Import completed successfully")
