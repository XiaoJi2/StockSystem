from django.contrib.staticfiles.storage import staticfiles_storage
from django.template.defaulttags import load
from django.urls import reverse
from django.utils.timezone import template_localtime
from jinja2 import Environment
import time, datetime

from Utils.mode import str_of_num


def time_result_format(data):
    if data:
        time_array = time.localtime(data)
        format_time = time.strftime("%H:%M:%S", time_array)
        return format_time

def money_result_format(data):
    if data:
        money = str_of_num(data)
        return money

def environment(**options):
    env = Environment(**options)
    env.globals.update({
    'static': staticfiles_storage.url,
    'url': reverse,
    'localtime': template_localtime,
    })
    env.filters['time_result_format'] = time_result_format # 自定义过滤器
    env.filters['money_result_format'] = money_result_format  # 自定义过滤器
    return env