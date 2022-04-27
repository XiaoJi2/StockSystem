from django.db import models

# Create your models here.
from Fupan.models import QingXuBiao
from Utils.Spiders import Spider


class SummaryTable():
    def __init__(self):
        pass

    def get_market_temperature(self):
        myspider = Spider(
            "https://flash-api.xuangubao.cn/api/market_indicator/line?fields=market_temperature")
        htmljson = myspider.getJson()
        # print(htmljson)
        dataok = htmljson['message']
        if dataok:
            data = htmljson['data']
            # print(data)
            return data[-1]

    def get_lianban_hight(self):
        qingxu = QingXuBiao()
        data = qingxu.get_lianban()
        lianban_list = []
        for lianban in data:
            if lianban.lianbanmax == None:
                lianban.lianbanmax = 0
            tmp_list = [lianban.rdatatime, lianban.lianbanmax]
            lianban_list.append(tmp_list)
        # print(lianban_list)
        return  lianban_list
