from django.db import models

# Create your models here.
from Utils.Spiders import Spider
import time, datetime

from Utils.mode import get_today_time
from Utils.tushare import TuShareModule

EXPERIENCE_CHOICES = (
    (1, '涨'),
    (2, '跌'),
    (3, '平'),
    (4, '休'),
)


class QingXuMode(models.Model):
    uid = models.AutoField(primary_key=True)
    # 日期
    rdatatime = models.CharField(max_length=15)
    # 涨
    hongpan = models.IntegerField()
    # 跌
    lvpan = models.IntegerField()
    # 实际涨停
    realzhangting = models.IntegerField()
    # 实际跌停
    dieting = models.IntegerField()
    # 炸板
    zhaban = models.IntegerField()
    # 连板
    lianban = models.IntegerField()
    # 2连板
    lianban2 = models.IntegerField()
    # 3连板
    liangban3 = models.IntegerField()
    # 3连板个股
    liangban3gegu = models.CharField(max_length=1000)
    # 3连板以上
    liangban3up = models.IntegerField()
    # 3连板个股
    liangban3upgegu = models.CharField(max_length=256)
    # 金额
    Total = models.IntegerField()
    # 更新时间
    updatetime = models.DateTimeField(auto_now=True)
    zhangdie = models.CharField(max_length=4)
    #最大连板数
    lianbanmax = models.IntegerField()
    lowtohigh = models.IntegerField()
    hightohigh = models.IntegerField()
    intensity = models.CharField(max_length=4)

    class Meta:
        db_table = 'qingxu'

# class DATListTable(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     # 日期
#     rdatatime = db.Column(db.String(15))
#     # 游资姓名
#     yzname = db.Column(db.String(255))
#     # 股票代码
#     stockcode = db.Column(db.String(15))
#     # 股票名称
#     stockname = db.Column(db.String(25))
#     # 买入
#     buy = db.Column(db.Integer)
#     # 卖出
#     sell = db.Column(db.Integer)


class QingXuBiao(object):
    def __init__(self):
        pass
    def update(self,uptime = ''):
        moodtable = QingXuMode()
        zhangtingmood = ''
        limitupcount = 0
        limitdowncount = 0
        risecount = 0
        fallcount = 0
        brokencount = 0
        ztcount = 0
        twocount = 0
        threecount = 0
        threeupcount = 0
        threestockname = ''
        threeupstockname = ''

        # now = get_today_time("%Y%m%d")
        # tsmodule = TuShareModule()
        # if tsmodule.trade_calendar(now) == False:
        #     # moodtable.hongpan = 0
        #     # moodtable.rdatatime = str(datetime.date.today())
        #     # moodtable.lvpan = 0
        #     # moodtable.realzhangting = 0
        #     # moodtable.dieting = 0
        #     # moodtable.zhaban = 0
        #     # moodtable.lianban = 0
        #     # moodtable.lianban2 = 0
        #     # moodtable.liangban3 = 0
        #     # moodtable.liangban3gegu = ''
        #     # moodtable.liangban3up = 0
        #     # moodtable.liangban3upgegu = ''
        #     # moodtable.Total = 0
        #     # moodtable.zhangdie = '休'
        #     # moodtable.save()
        #     return True

        # 大盘指数
        url = "https://api-ddc-wscn.xuangubao.cn/market/trend?fields=tick_at,close_px&prod_code=000001.SS&date=" + uptime
        myspider = Spider(url)
        htmljson = myspider.getJson()
        dictDate = htmljson['message']
        if dictDate == 'OK':
            todayshoupan = htmljson['data']['candle']['000001.SS']['lines'][-1][-1]
            yesterdayshoupan = htmljson['data']['candle']['000001.SS']['pre_close_px']
            zhishu = todayshoupan - yesterdayshoupan
            print(zhishu)
            if zhishu > 0:
                zhangtingmood = '涨'
            elif zhishu < 0:
                zhangtingmood = '跌'
            else:
                zhangtingmood = '平'

        # 涨跌停数量
        url = "https://flash-api.xuangubao.cn/api/market_indicator/line?fields=limit_up_count,limit_down_count&date=" + uptime
        myspider.setUrl(url)
        htmljson = myspider.getJson()
        dictDate = htmljson['message']
        if dictDate == 'OK':
            limitupcount  = htmljson['data'][-1]["limit_up_count"]
            limitdowncount = htmljson['data'][-1]["limit_down_count"]

        # 涨跌数量
        url = "https://flash-api.xuangubao.cn/api/market_indicator/line?fields=rise_count,fall_count&date=" + uptime
        myspider.setUrl(url)
        htmljson = myspider.getJson()
        dictDate = htmljson['message']
        if dictDate == 'OK':
            risecount = htmljson['data'][-1]["rise_count"]
            fallcount = htmljson['data'][-1]["fall_count"]

        # 炸板数量
        url = "https://flash-api.xuangubao.cn/api/market_indicator/line?fields=limit_up_broken_count,limit_up_broken_ratio&date=" + uptime
        myspider.setUrl(url)
        htmljson = myspider.getJson()
        dictDate = htmljson['message']
        if dictDate == 'OK':
            brokencount = htmljson['data'][-1]["limit_up_broken_count"]

        # 涨停
        url = "https://flash-api.xuangubao.cn/api/pool/detail?pool_name=limit_up&date=" + uptime
        myspider.setUrl(url)
        htmljson = myspider.getJson()
        dictDate = htmljson['message']
        max_num = 0
        if dictDate == 'OK':
            dictDate = htmljson['data']
            for list in dictDate:
                # 去除ST
                if (list["stock_chi_name"].__contains__('ST')):
                    continue
                ztcount += 1
                if list["limit_up_days"] == 2:
                    twocount += 1
                if list["limit_up_days"] == 3:
                    threecount += 1
                    threestockname += list["stock_chi_name"] + ','
                if list["limit_up_days"] > 3:
                    threeupcount += 1
                    threeupstockname += list["stock_chi_name"] + '(' + str(list["limit_up_days"]) + ')' ','
                tmp_num = list["limit_up_days"]
                if tmp_num > max_num:
                    max_num = tmp_num

        moodtable.hongpan = risecount
        moodtable.rdatatime = uptime#str(datetime.date.today())
        moodtable.lvpan = fallcount
        moodtable.realzhangting = limitupcount
        moodtable.dieting = limitdowncount
        moodtable.zhaban = brokencount
        moodtable.lianban = ztcount
        moodtable.lianban2 = twocount
        moodtable.liangban3 = threecount
        moodtable.liangban3gegu = threestockname
        moodtable.liangban3up = threeupcount
        moodtable.liangban3upgegu = threeupstockname
        moodtable.Total = 0
        moodtable.zhangdie = zhangtingmood
        moodtable.lianbanmax = max_num
        moodinfo = QingXuMode.objects.all().order_by('rdatatime').last()
        print("------")
        print(type(moodinfo))
        print(moodinfo.lianban2)
        if (moodinfo.lianban2 != 0):
            print()
            moodtable.lowtohigh = int(round((threecount/moodinfo.lianban2)*100, 0))
        else:
            moodtable.lowtohigh = 0
        if ((moodinfo.liangban3 + moodinfo.liangban3up) != 0):
            moodtable.hightohigh = int(round((threeupcount/(moodinfo.liangban3 + moodinfo.liangban3up))*100, 0))
        else:
            moodtable.hightohigh = 0

        if(moodinfo.hightohigh != None):
            if( moodtable.hightohigh > int(moodinfo.hightohigh)  ):
                moodtable.intensity = '强'
            elif (moodtable.hightohigh == int(moodinfo.hightohigh) and moodtable.lowtohigh > int(moodinfo.lowtohigh)):
                moodtable.intensity = '强'
            else:
                moodtable.intensity = '弱'
        else:
            moodtable.intensity = '强'
        moodtable.save()
        return True

    def getinfo(self):
        moodinfo = QingXuMode.objects.all().order_by('rdatatime')#('-rdatatime')
        return moodinfo

    def checkdata(self, datetime):
        moodinfo = QingXuMode.objects.filter(rdatatime=datetime)
        if moodinfo:
            deleted = moodinfo.delete()
            if deleted:
                return True
            else:
                return False
        else:
            return True

    def get_lianban(self):
        moodinfo = QingXuMode.objects.all().order_by('-rdatatime')[:10]
        return moodinfo


class LongHuBang(object):
    def __init__(self):
        pass

    def get_info(self):
        myspider = Spider(
            "https://apphq.longhuvip.com/w1/api/index.php?a=GetYTFP_LHBDX&c=FuPanLa&PhoneOSNew=1&DeviceID=4477a863-a14e-3284-900f-8a6e71e24349&apiv=w25&")
        htmljson = myspider.getJson()
        # print(htmljson)
        dataok = htmljson['Date']
        if dataok:
            # lists = htmljson['List']
            # print(len(lists))
            # for list in lists:
            #     bname = list['BName']
            #     print(bname)
            #     buylists = list['Buy']
            #     for buylist in buylists:
            #         stono = buylist['Sto']
            #         stoname = buylist['StoN']
            #         money = buylist['Money']
            #         print('buy')
            #         print(stono, stoname, money)
            #     selllists = list['Sell']
            #     for selllist in selllists:
            #         stono = selllist['Sto']
            #         stoname = selllist['StoN']
            #         money = selllist['Money']
            #         print('sell')
            #         print(stono, stoname, money)
            return dict(htmljson)
        else:
            return False


class GuPiaoFuPan(object):
    def __init__(self):
        pass

    def zhangting_reason(self):
        post_data = {
            'a': 'GetPlateInfo',
            'apiv': 'w25',
            'c': 'DailyLimitResumption',
            'DeviceID': '4477a863-a14e-3284-900f-8a6e71e24349',
            'Index': '0',
            'PhoneOSNew': '1',
            'st': '10',
        }
        my_spider = Spider("https://apphq.longhuvip.com/w1/api/index.php")
        html_json = my_spider.getPostjson(post_data)
        # print(html_json)
        # print(html_json.get('errcode'))
        if html_json.get('errcode') == '0':
            return dict(html_json)

    def panmianguanzhu(self):
        myspider = Spider(
            "https://apphq.longhuvip.com/w1/api/index.php?a=GetPMSL_PMLD&st=30&apiv=w25&c=FuPanLa&PhoneOSNew=1&DeviceID=4477a863-a14e-3284-900f-8a6e71e24349&Index=0&")
        html_json = myspider.getJson()
        print(html_json)
        if html_json.get('errcode') == '0':
            return dict(html_json)

