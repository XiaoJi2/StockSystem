import os
import sys
import time, datetime
from django.test import TestCase

# Create your tests here.

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,parentdir)

from Utils.Spiders import Spider





def LATList():
    myspider = Spider(
        "https://hq.kaipanla.com/w1/api/index.php?a=GetYTFP_LHBDX&c=FuPanLa&PhoneOSNew=1&DeviceID=4477a863-a14e-3284-900f-8a6e71e24349&apiv=w25&")
    htmljson = myspider.getJson()
    print(htmljson)
    dataok = htmljson['Date']
    if dataok:
        lists = htmljson['List']
        print(len(lists))
        for list in lists:
            bname = list['BName']
            print(bname)
            buylists = list['Buy']
            for buylist in buylists:
                stono = buylist['Sto']
                stoname = buylist['StoN']
                money = buylist['Money']
                print('buy')
                print(stono, stoname, money)
            selllists = list['Sell']
            for selllist in selllists:
                stono = selllist['Sto']
                stoname = selllist['StoN']
                money = selllist['Money']
                print('sell')
                print(stono, stoname, money)


def gegufupan():
    post_data = {
        'a': 'GetPlateInfo',
        'apiv': 'w25',
        'c': 'DailyLimitResumption',
        'DeviceID': '4477a863-a14e-3284-900f-8a6e71e24349',
        'Index': '0',
        'PhoneOSNew': '1',
        'st': '10',
    }
    my_spider = Spider("https://hq.kaipanla.com/w1/api/index.php")
    html_json = my_spider.getPostjson(post_data)
    print(html_json)
    dict_date = html_json['list']
    fp_time = html_json['date']
    data_list = []
    if dict_date:
        for fp_list in dict_date:
            sz_code = fp_list['ZSCode']
            zs_name = fp_list['ZSName']
            print(sz_code, zs_name)
            stock_lists = fp_list['StockList']
            stock_list = []
            jrzt_dirc = {}
            for stlist in stock_lists:
                st_name = stlist[1]
                time_array = time.localtime(stlist[6])
                zt_time = time.strftime("%H:%M:%S", time_array)
                lian_ban = stlist[9]
                zhuli_liuru = stlist[12]
                reason = stlist[17]
                bkgg_list = [st_name, zt_time, lian_ban, zhuli_liuru, reason]
                stock_list.append(bkgg_list)
            jrzt_dirc['ZSName'] = zs_name
            jrzt_dirc['StockList'] = bkgg_list
            data_list.append(jrzt_dirc)
        print(data_list)


def panmianguanzhu():
    myspider = Spider(
        "https://hq.kaipanla.com/w1/api/index.php?a=GetPMSL_PMLD&st=30&apiv=w25&c=FuPanLa&PhoneOSNew=1&DeviceID=4477a863-a14e-3284-900f-8a6e71e24349&Index=0&")
    htmljson = myspider.getJson()
    print(htmljson)

def weipanqiangchou():
    myspider = Spider(
        "https://hq.kaipanla.com/w1/api/index.php?Order=1&a=GetWPQC&st=500&apiv=w24&Type=1&c=StockBidYiDong&PhoneOSNew=1&UserID=0&DeviceID=4477a863-a14e-3284-900f-8a6e71e24349&Token=0&Index=0&")
    htmljson = myspider.getJson()
    print(htmljson)


if __name__ == '__main__':
    gegufupan()
    pass
