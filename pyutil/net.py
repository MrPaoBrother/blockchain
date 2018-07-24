# -*- coding:utf8 -*-
import logging
import requests
import random
from text.util import smart_decode


def fetch_html(url, headers={}, proxy=None, https_proxy=None, data=None):
    try:
        proxies = {"http": proxy, 'https': https_proxy}
        if not headers:
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36"}
        if not data:
            r = requests.get(url, headers=headers, timeout=100, proxies=proxies, verify=False)
        else:
            r = requests.post(url, headers=headers, timeout=100, proxies=proxies, data=data)
        if r.status_code != 200:
            return r.status_code, ''
        body = r.content
        if not body:
            return r.status_code, ''
        body, best_encoding, bad_num = smart_decode(body, with_detail=True)
    except Exception as e:
        logging.exception(e)
        return 0, ''
    return r.status_code, body