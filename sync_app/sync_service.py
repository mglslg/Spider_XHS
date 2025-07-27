from datetime import datetime

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
