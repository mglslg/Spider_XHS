# encoding: utf-8
import time

from loguru import logger

import inspect

from apis.xhs_pc_apis import XHS_Apis
from functools import wraps
import urllib

# 默认延迟时间
default_delay_time = 2.0


class SlgXhsApi(XHS_Apis):
    min_delay = default_delay_time
    last_request_time = 0.0

    def __init__(self):
        super().__init__()

        # 读取基类的所有方法列表
        base_class = self.__class__.__bases__[0]
        default_methods_to_limit = [
            name for name, attr in inspect.getmembers(base_class, predicate=inspect.isfunction)
            if not name.startswith('_') and not name.startswith('__')
        ]

        logger.info(f'default_methods_to_limit:{default_methods_to_limit}')

        # default_methods_to_limit的真子集,自定义指定等待秒数,可以覆盖默认值(预留配置)
        self.specific_methods_to_limit = {'get_user_all_collect_note_info': 0.1, 'get_user_all_notes': 0.1}

        # AOP
        for method_name in default_methods_to_limit:
            original_method = getattr(self, method_name)
            limited_method = self.rate_limited(method_name)(original_method)
            setattr(self, method_name, limited_method)  # 恢复这行，让替换生效

    def rate_limited(self, method_name):
        def decorator(original_method):
            @wraps(original_method)
            def wrapped(*args, **kwargs):
                if method_name in self.specific_methods_to_limit:
                    self._rate_limit(method_name, self.specific_methods_to_limit[method_name], args, kwargs)
                else:
                    self._rate_limit(method_name, None, args, kwargs)

                return original_method(*args, **kwargs)

            return wrapped

        return decorator

    def get_user_all_notes_ext(self, user_url: str, cookies_str: str, proxies: dict = None, break_point: str = ''):
        """
           获取用户所有笔记
           :param user_id: 你想要获取的用户的id
           :param cookies_str: 你的cookies
           返回用户的所有笔记
        """
        cursor = ''
        note_list = []
        try:
            urlParse = urllib.parse.urlparse(user_url)
            user_id = urlParse.path.split("/")[-1]
            kvs = urlParse.query.split('&')
            kvDist = {kv.split('=')[0]: kv.split('=')[1] for kv in kvs}
            xsec_token = kvDist['xsec_token'] if 'xsec_token' in kvDist else ""
            xsec_source = kvDist['xsec_source'] if 'xsec_source' in kvDist else "pc_search"
            while True:
                success, msg, res_json = self.get_user_note_info(user_id, cursor, cookies_str, xsec_token, xsec_source,
                                                                 proxies)
                if not success:
                    raise Exception(msg)
                notes = res_json["data"]["notes"]
                if 'cursor' in res_json["data"]:
                    cursor = str(res_json["data"]["cursor"])
                else:
                    break
                note_list.extend(notes)

                # 匹配到断点时直接跳出
                note_id_set = {n.get('note_id') for n in notes}
                if break_point in note_id_set:
                    break

                if len(notes) == 0 or not res_json["data"]["has_more"]:
                    break
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, note_list

    def get_user_all_collect_note_info_ext(self, user_url: str, cookies_str: str, proxies: dict = None,
                                           break_point: str = ''):
        """
            获取用户所有收藏笔记
            :param user_id: 你想要获取的用户的id
            :param cookies_str: 你的cookies
            返回用户的所有收藏笔记
        """
        cursor = ''
        note_list = []
        try:
            urlParse = urllib.parse.urlparse(user_url)
            user_id = urlParse.path.split("/")[-1]
            kvs = urlParse.query.split('&')
            kvDist = {kv.split('=')[0]: kv.split('=')[1] for kv in kvs}
            xsec_token = kvDist['xsec_token'] if 'xsec_token' in kvDist else ""
            xsec_source = kvDist['xsec_source'] if 'xsec_source' in kvDist else "pc_search"
            while True:
                success, msg, res_json = self.get_user_collect_note_info(user_id, cursor, cookies_str, xsec_token,
                                                                         xsec_source, proxies)
                if not success:
                    raise Exception(msg)
                notes = res_json["data"]["notes"]
                if 'cursor' in res_json["data"]:
                    cursor = str(res_json["data"]["cursor"])
                else:
                    break
                note_list.extend(notes)

                # 匹配到断点时直接跳出
                note_id_set = {n.get('note_id') for n in notes}
                if break_point in note_id_set:
                    break

                if len(notes) == 0 or not res_json["data"]["has_more"]:
                    break
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, note_list

    def get_user_all_like_note_info_ext(self, user_url: str, cookies_str: str, proxies: dict = None,
                                        break_point: str = ''):
        """
            获取用户所有喜欢笔记
            :param user_id: 你想要获取的用户的id
            :param cookies_str: 你的cookies
            返回用户的所有喜欢笔记
        """
        cursor = ''
        note_list = []
        try:
            urlParse = urllib.parse.urlparse(user_url)
            user_id = urlParse.path.split("/")[-1]
            kvs = urlParse.query.split('&')
            kvDist = {kv.split('=')[0]: kv.split('=')[1] for kv in kvs}
            xsec_token = kvDist['xsec_token'] if 'xsec_token' in kvDist else ""
            xsec_source = kvDist['xsec_source'] if 'xsec_source' in kvDist else "pc_user"
            while True:
                success, msg, res_json = self.get_user_like_note_info(user_id, cursor, cookies_str, xsec_token,
                                                                      xsec_source, proxies)
                if not success:
                    raise Exception(msg)
                notes = res_json["data"]["notes"]
                if 'cursor' in res_json["data"]:
                    cursor = str(res_json["data"]["cursor"])
                else:
                    break
                note_list.extend(notes)

                # 匹配到断点时直接跳出
                note_id_set = {n.get('note_id') for n in notes}
                if break_point in note_id_set:
                    break

                if len(notes) == 0 or not res_json["data"]["has_more"]:
                    break
        except Exception as e:
            success = False
            msg = str(e)
        return success, msg, note_list

    @classmethod
    def _rate_limit(cls, method_name, delay_time=None, args=None, kwargs=None):
        if delay_time is not None:
            cls.min_delay = delay_time
        else:
            cls.min_delay = default_delay_time

        # 直接 sleep 指定的延迟时间，并打印 args 和 kwargs
        logger.info(f'Rate Limit [{method_name}]: sleeping for [{cls.min_delay}] seconds, args={args}, kwargs={kwargs}')
        time.sleep(cls.min_delay)

    @staticmethod
    def get_note_no_water_video(note_id):
        SlgXhsApi._rate_limit('get_note_no_water_video')
        return XHS_Apis.get_note_no_water_video(note_id)

    @staticmethod
    def get_note_no_water_img(img_url):
        SlgXhsApi._rate_limit('get_note_no_water_img')
        return XHS_Apis.get_note_no_water_img(img_url)
