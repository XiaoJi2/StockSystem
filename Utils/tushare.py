import tushare as ts

class TuShareModule(object):
    def __init__(self):
        ts.set_token("01661304735b341060f01bf30a5ac6041a05702dd732bdaffa2e47f5")
        self.pro = ts.pro_api()

    def trade_calendar(self,date):
        result = self.pro.trade_cal(exchange='', start_date=date, end_date=date)
        print(result.get('is_open'))
        return result.get('is_open')[0]

