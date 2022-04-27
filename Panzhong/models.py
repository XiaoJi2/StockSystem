from django.db import models

# Create your models here.
from Utils.Spiders import Spider
import time, datetime

from Utils.mode import str_of_num


class PanZhongData():
    def __init__(self):
        pass
    def getnews(self):
        myspider = Spider("https://api.xuangubao.cn/api/pc/msgs?subjids=9,10,723,35,469,821&limit=30")
        htmljson = myspider.getJson()
        dictDate = htmljson['NewMsgs']
        datalist = []
        if dictDate:
            for list in dictDate:
                datadict = {}
                title = list.get('Title')
                summary = list.get('Summary')
                timeArray = time.localtime(list.get('CreatedAtInSec'))
                ZhiBodatatime = time.strftime("%H:%M:%S", timeArray)
                datadict['title'] = title
                datadict['summary'] = summary
                datadict['datatime'] = ZhiBodatatime
                datalist.append(datadict)
            return datalist
        else:
            return False

    def getdapanzhibo(self):
        myspider = Spider("https://apphq.longhuvip.com/w1/api/index.php?st=10&a=ZhiBoContent&apiv=w24&c=ConceptionPoint&PhoneOSNew=1&DeviceID=4477a863-a14e-3284-900f-8a6e71e24349&index=0&")
        htmljson = myspider.getJson()
        dictDate = htmljson['List']
        datalist = []
        if dictDate:
            for list in dictDate:
                zhibodict = {}
                timeArray = time.localtime(list.get('Time'))
                ZhiBodatatime = time.strftime("%H:%M:%S", timeArray)
                comment = list.get('Comment')
                stocks = list.get('Stock')
                zhibo_type = list.get('Type')
                stocklists = []
                for stockls in stocks:
                    stock = stockls[1]
                    increase = stockls[2]
                    stls = [stock, increase]
                    stocklists.append(stls)
                zhibodict['time'] = ZhiBodatatime
                zhibodict['comment'] = comment
                zhibodict['stock'] = stocklists
                zhibodict['type'] = zhibo_type
                datalist.append(zhibodict)
            return datalist
        else:
            return False

    def duanxianjingling(self):
        post_data = {
            'a': 'Radar',
            'st': '100',
            'apiv': 'w25',
            'c': 'HomeDingPan',
            'PhoneOSNew': '1',
            'DeviceID': '4477a863-a14e-3284-900f-8a6e71e24349',
            'Index': '0',
        }
        my_spider = Spider("https://apphq.longhuvip.com/w1/api/index.php")
        html_json = my_spider.getPostjson(post_data)
        # print(html_json)
        dict_date = html_json['list']
        data_list = []
        if dict_date:
            for dx_list in dict_date:
                dx_dict = {}
                time_array = time.localtime(dx_list.get('time'))
                dx_time = time.strftime("%H:%M:%S", time_array)
                stock_name = dx_list.get('stock_name')
                dx_status = dx_list.get('status')
                dx_content = dx_list.get('content')
                dx_dict['time'] = dx_time
                dx_dict['stock'] = stock_name
                dx_dict['status'] = dx_status
                dx_dict['content'] = dx_content
                dx_dict['status_color'] = dx_list.get('status_color')
                data_list.append(dx_dict)
            return data_list
        else:
            return False

    def gegurenqi(self):
        my_spider = Spider(
            "https://apphq.longhuvip.com/w1/api/index.php?Order=1&a=GetHotPHB&st=30&apiv=w25&Type=1&c=StockBidYiDong&PhoneOSNew=1&UserID=879026&DeviceID=4477a863-a14e-3284-900f-8a6e71e24349&Token=d993f4b77d9d16b9585a504e58795dbf&Index=0&")
        html_json = my_spider.getJson()

        dict_date = html_json['List']
        data_list = []
        if dict_date:
            for list1 in dict_date:
                ggrq_list = {}
                stock_name = list1[1]
                change = list1[3]
                increase = list1[2]
                ggrq_list = [stock_name, change, increase]
                data_list.append(ggrq_list)
            return data_list
        else:
            return False

    def bankuairenqi(self):
        my_spider = Spider(
            "https://apphq.longhuvip.com/w1/api/index.php?Order=1&a=RealRankingInfo&st=30&apiv=w25&Type=1&c=ZhiShuRanking&PhoneOSNew=1&DeviceID=4477a863-a14e-3284-900f-8a6e71e24349&Index=0&ZSType=7&")
        html_json = my_spider.getJson()
        dict_date = html_json['list']
        data_list = []
        if dict_date:
            for list1 in dict_date:
                bk_code = list1[0]
                bk_name = list1[1]
                bk_popularity = list1[2]
                bk_speed = list1[4]
                bk_zhuli = list1[6]
                bkrq_list = [bk_code, bk_name, bk_popularity, bk_speed, bk_zhuli]
                data_list.append(bkrq_list)
            return data_list
        else:
            return False

    def bankuaigegu(self, code=801001):
        url = "https://apphq.longhuvip.com/w1/api/index.php?Order=1&st=30&a=ZhiShuStockList_W8&c=ZhiShuRanking&PhoneOSNew=1&old=1&DeviceID=4477a863-a14e-3284-900f-8a6e71e24349&Token=d993f4b77d9d16b9585a504e58795dbf&Index=0&apiv=w25&Type=6&UserID=879026&PlateID=" + str(code) + "&"
        my_spider = Spider(url)
        html_json = my_spider.getJson()
        print(html_json)
        dict_data = html_json['list']
        data_list = []
        if dict_data:
            for list1 in dict_data:
                gp_code = list1[0]
                gp_name = list1[1]
                gp_zhangfu = list1[6]
                gp_zongchengjiao = str_of_num(list1[7])
                gp_zhuli = list1[24]
                gp_zhulijinge = str_of_num(list1[13])
                gp_lianban = list1[23]
                gp_bankuai = list1[4]
                bkgg_list = [gp_code, gp_name, gp_zhangfu, gp_zongchengjiao, gp_zhuli, gp_zhulijinge, gp_lianban,
                             gp_bankuai]
                data_list.append(bkgg_list)
            bk_dict = {}
            bk_dict['data'] = data_list
            return bk_dict
        else:
            return False

