import pymysql
from datetime import datetime, timedelta
import requests
import json
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import binance
from data_config import *
from decimal import Decimal

#import bot

#b = bot.Bot(token=TELEGRAM_TOKEN)
# ----------------- #

def exec_cron():

    db = db_con()

    now = datetime.now()
    fd = now.strftime('%Y-%m-%d %H:%M:%S')

    curs = db.cursor()

    binance.set(p_key, s_key)
    
    sql = "select distinct a.symbol, a.rods, a.gname, a.fr_dt, a.fr_pc, a.to_dt, a.to_pc, b.timing, b.tdtype, b.pctype, b.qty, b.num, b.slippage, b.pre_num from %s as a join %s as b on a.symbol = b.symbol and a.rods = b.rods and a.gname = b.gname where a.rods = %s and a.is_extension = %s and b.is_complete = %s" %(tline, trading, "%s", "%s", "%s")
    isql = "update %s set is_complete = 1 where num = %s " % (trading, "%s")
    psql = "select price from fbase_btc where symbol = %s order by dt desc limit 1"
    csql = "select close from fchart where rods = %s order by dt desc limit 1"

    todt = time.strftime('%Y%m%d%H')

    curs.execute(psql, ('BTCUSDT'))
    price = curs.fetchone()[0]



    # 15min
    if int(now.strftime('%M')) in [0,15, 30, 45]:
        
        curs.execute(sql, ('min15', '1', '0'))
        rows = curs.fetchall()
        
        for row in rows:
            
            now_price = ext_tline_query(row[3], row[5], row[4], row[6], row[1], todt)

            # if start
            if price >= now_price and row[7] == 'breakthrough' and row[9] == 'market':
                print(price, now_price, row[7], row[8])
                data = f_order(row[0], binance.BUY, row[10], 0.0, orderType='MARKET')
                print(data)
                curs.execute(isql, (row[11]))
                
            elif price >= now_price and row[7] == 'breakthrough' and row[9] == 'limit':
                print(price, now_price, row[7], row[8])
                data = f_order_limit(row[0], binance.BUY, row[10], price + round(Decimal(row[12] if row[12] else 0)), orderType='LIMIT')
                print(data)
                curs.execute(isql, (row[11]))
                
            elif price <= now_price and row[7] == 'downwdbreak' and row[9] == 'market':
                print(price, now_price, row[7], row[8])
                data = f_order(row[0], binance.SELL, row[10], 0.0, orderType='MARKET')
                print(data)
                curs.execute(isql, (row[11]))
                
            elif price <= now_price and row[7] == 'downwdbreak' and row[9] == 'limit':
                print(price, now_price, row[7], row[8])
                data = f_order_limit(row[0], binance.SELL, row[10], price + round(Decimal(row[12] if row[12] else 0)), orderType='LIMIT')
                print(data)
                curs.execute(isql, (row[11]))
                
            else:
                data = {}

            try:
                status = data['status']
                if row[9] == 'limit':
                    msg = '[거래체결] ' + row[1]+'/'+row[2] +' / '+ ('상향돌파 ' if row[7] == 'breakthrough' else '하향돌파 ') + ' / '+ ('지정가 ' if row[9] == 'limit' else '시장가 ') +' / '+ str(row[10])+'btc' + ' / price: '+ str(price) +' usdt'+' | oderId:'+str(row[11]) 
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)
                else:
                    msg = '[거래체결] ' + row[1]+'/'+row[2] +' / '+ ('상향돌파 ' if row[7] == 'breakthrough' else '하향돌파 ') + ' / '+ ('지정가 ' if row[9] == 'limit' else '시장가 ') +' / '+ str(row[10])+'btc'+' | oderId:'+str(row[11]) 
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)

            except:
                try:
                    code = data['code']
                    if code == -2019:
                        msg = '[거래오류] ' + row[1]+'/'+row[2]+' | oderId:'+str(row[11])+ ': 금액이 부족합니다.' 
                    else:
                        msg = '[거래오류] ' + row[1]+'/'+row[2]+' | oderId:'+str(row[11])+ ': 기타 오류' 
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)
                except NameError:
                    pass
                except KeyError:
                    pass
                except:
                    msg = '[시스템 에러] 관리자에게 문의 하세요'
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)

        db.commit()

    # 30min
    if int(now.strftime('%M')) in [0, 30]:
        
        curs.execute(sql, ('min30', '1', '0'))
        rows = curs.fetchall()
        
        for row in rows:
            
            now_price = ext_tline_query(row[3], row[5], row[4], row[6], row[1], todt)

            # if start
            if price >= now_price and row[7] == 'breakthrough' and row[9] == 'market':
                print(price, now_price, row[7], row[8])
                data = f_order(row[0], binance.BUY, row[10], 0.0, orderType='MARKET')
                print(data)
                curs.execute(isql, (row[11]))
                
            elif price >= now_price and row[7] == 'breakthrough' and row[9] == 'limit':
                print(price, now_price, row[7], row[8])
                data = f_order_limit(row[0], binance.BUY, row[10], price + round(Decimal(row[12] if row[12] else 0)), orderType='LIMIT')
                print(data)
                curs.execute(isql, (row[11]))
                
            elif price <= now_price and row[7] == 'downwdbreak' and row[9] == 'market':
                print(price, now_price, row[7], row[8])
                data = f_order(row[0], binance.SELL, row[10], 0.0, orderType='MARKET')
                print(data)
                curs.execute(isql, (row[11]))
                
            elif price <= now_price and row[7] == 'downwdbreak' and row[9] == 'limit':
                print(price, now_price, row[7], row[8])
                data = f_order_limit(row[0], binance.SELL, row[10], price + round(Decimal(row[12] if row[12] else 0)), orderType='LIMIT')
                print(data)
                curs.execute(isql, (row[11]))
                
            else:
                data = {}

            try:
                status = data['status']
                if row[9] == 'limit':
                    msg = '[거래체결] ' + row[1]+'/'+row[2] +' / '+ ('상향돌파 ' if row[7] == 'breakthrough' else '하향돌파 ') + ' / '+ ('지정가 ' if row[9] == 'limit' else '시장가 ') +' / '+ str(row[10])+'btc' + ' / price: '+ str(price) +' usdt'+' | oderId:'+str(row[11]) 
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)
                else:
                    msg = '[거래체결] ' + row[1]+'/'+row[2] +' / '+ ('상향돌파 ' if row[7] == 'breakthrough' else '하향돌파 ') + ' / '+ ('지정가 ' if row[9] == 'limit' else '시장가 ') +' / '+ str(row[10])+'btc'+' | oderId:'+str(row[11]) 
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)

            except:
                try:
                    code = data['code']
                    if code == -2019:
                        msg = '[거래오류] ' + row[1]+'/'+row[2]+' | oderId:'+str(row[11])+ ': 금액이 부족합니다.' 
                    else:
                        msg = '[거래오류] ' + row[1]+'/'+row[2]+' | oderId:'+str(row[11])+ ': 기타 오류' 
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)
                except NameError:
                    pass
                except KeyError:
                    pass
                except:
                    msg = '[시스템 에러] 관리자에게 문의 하세요'
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)
        db.commit()


    # 1hour
    if int(now.strftime('%M')) in [0]:
        
        curs.execute(sql, ('hour1', '1', '0'))
        rows = curs.fetchall()
        
        for row in rows:
            
            now_price = ext_tline_query(row[3], row[5], row[4], row[6], row[1], todt)

            # if start
            if price >= now_price and row[7] == 'breakthrough' and row[9] == 'market':
                print(price, now_price, row[7], row[8])
                data = f_order(row[0], binance.BUY, row[10], 0.0, orderType='MARKET')
                print(data)
                curs.execute(isql, (row[11]))

            elif price >= now_price and row[7] == 'breakthrough' and row[9] == 'limit':
                print(price, now_price, row[7], row[8])
                data = f_order_limit(row[0], binance.BUY, row[10], price + round(Decimal(row[12] if row[12] else 0)), orderType='LIMIT')
                print(data)
                curs.execute(isql, (row[11]))
                
            elif price <= now_price and row[7] == 'downwdbreak' and row[9] == 'market':
                print(price, now_price, row[7], row[8])
                data = f_order(row[0], binance.SELL, row[10], 0.0, orderType='MARKET')
                print(data)
                curs.execute(isql, (row[11]))
                
            elif price <= now_price and row[7] == 'downwdbreak' and row[9] == 'limit':
                print(price, now_price, row[7], row[8])
                data = f_order_limit(row[0], binance.SELL, row[10], price + round(Decimal(row[12] if row[12] else 0)), orderType='LIMIT')
                print(data)
                curs.execute(isql, (row[11]))
                
            else:
                data = {}

            try:
                status = data['status']
                if row[9] == 'limit':
                    msg = '[거래체결] ' + row[1]+'/'+row[2] +' / '+ ('상향돌파 ' if row[7] == 'breakthrough' else '하향돌파 ') + ' / '+ ('지정가 ' if row[9] == 'limit' else '시장가 ') +' / '+ str(row[10])+'btc' + ' / price: '+ str(price) +' usdt'+' | oderId:'+str(row[11]) 
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)
                else:
                    msg = '[거래체결] ' + row[1]+'/'+row[2] +' / '+ ('상향돌파 ' if row[7] == 'breakthrough' else '하향돌파 ') + ' / '+ ('지정가 ' if row[9] == 'limit' else '시장가 ') +' / '+ str(row[10])+'btc'+' | oderId:'+str(row[11]) 
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)

            except:
                try:
                    code = data['code']
                    if code == -2019:
                        msg = '[거래오류] ' + row[1]+'/'+row[2]+' | oderId:'+str(row[11])+ ': 금액이 부족합니다.' 
                    else:
                        msg = '[거래오류] ' + row[1]+'/'+row[2]+' | oderId:'+str(row[11])+ ': 기타 오류' 
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)
                except NameError:
                    pass
                except KeyError:
                    pass
                except:
                    msg = '[시스템 에러] 관리자에게 문의 하세요'
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)
        db.commit()

    # 4hour
    if int(now.strftime('%M')) in [0] and int(now.strftime('%H')) in [0, 4, 8, 12, 16, 20]:
        
        curs.execute(sql, ('hour4', '1', '0'))
        rows = curs.fetchall()
        
        for row in rows:
            
            now_price = ext_tline_query(row[3], row[5], row[4], row[6], row[1], todt)

            # if start
            if price >= now_price and row[7] == 'breakthrough' and row[9] == 'market':
                print(price, now_price, row[7], row[8])
                data = f_order(row[0], binance.BUY, row[10], 0.0, orderType='MARKET')
                print(data)
                curs.execute(isql, (row[11]))
                
            elif price >= now_price and row[7] == 'breakthrough' and row[9] == 'limit':
                print(price, now_price, row[7], row[8])
                data = f_order_limit(row[0], binance.BUY, row[10], price + round(Decimal(row[12] if row[12] else 0)), orderType='LIMIT')
                print(data)
                curs.execute(isql, (row[11]))
                
            elif price <= now_price and row[7] == 'downwdbreak' and row[9] == 'market':
                print(price, now_price, row[7], row[8])
                data = f_order(row[0], binance.SELL, row[10], 0.0, orderType='MARKET')
                print(data)
                curs.execute(isql, (row[11]))
                
            elif price <= now_price and row[7] == 'downwdbreak' and row[9] == 'limit':
                print(price, now_price, row[7], row[8])
                data = f_order_limit(row[0], binance.SELL, row[10], price + round(Decimal(row[12] if row[12] else 0)), orderType='LIMIT')
                print(data)
                curs.execute(isql, (row[11]))
                
            else:
                data = {}

            try:
                status = data['status']
                if row[9] == 'limit':
                    msg = '[거래체결] ' + row[1]+'/'+row[2] +' / '+ ('상향돌파 ' if row[7] == 'breakthrough' else '하향돌파 ') + ' / '+ ('지정가 ' if row[9] == 'limit' else '시장가 ') +' / '+ str(row[10])+'btc' + ' / price: '+ str(price) +' usdt'+' | oderId:'+str(row[11]) 
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)
                else:
                    msg = '[거래체결] ' + row[1]+'/'+row[2] +' / '+ ('상향돌파 ' if row[7] == 'breakthrough' else '하향돌파 ') + ' / '+ ('지정가 ' if row[9] == 'limit' else '시장가 ') +' / '+ str(row[10])+'btc'+' | oderId:'+str(row[11]) 
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)

            except:
                try:
                    code = data['code']
                    if code == -2019:
                        msg = '[거래오류] ' + row[1]+'/'+row[2]+' | oderId:'+str(row[11])+ ': 금액이 부족합니다.' 
                    else:
                        msg = '[거래오류] ' + row[1]+'/'+row[2]+' | oderId:'+str(row[11])+ ': 기타 오류' 
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)
                except NameError:
                    pass
                except KeyError:
                    pass
                except:
                    msg = '[시스템 에러] 관리자에게 문의 하세요'
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)
        db.commit() 
    

    # 5min
    if int(now.strftime('%M')) in [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55]:

        curs.execute(sql, ('min5', '1', '0'))
        rows = curs.fetchall()

        for row in rows:
            
            now_price = ext_tline_query(row[3], row[5], row[4], row[6], row[1], todt)

            # if start
            if price >= now_price and row[7] == 'breakthrough' and row[9] == 'market':
                print(price, now_price, row[7], row[8])
                data = f_order(row[0], binance.BUY, row[10], 0.0, orderType='MARKET')
                print(data)
                curs.execute(isql, (row[11]))
                
            elif price >= now_price and row[7] == 'breakthrough' and row[9] == 'limit':
                print(price, now_price, row[7], row[8])
                data = f_order_limit(row[0], binance.BUY, row[10], price + round(Decimal(row[12] if row[12] else 0)), orderType='LIMIT')
                print(data)
                curs.execute(isql, (row[11]))
                
            elif price <= now_price and row[7] == 'downwdbreak' and row[9] == 'market':
                print(price, now_price, row[7], row[8])
                data = f_order(row[0], binance.SELL, row[10], 0.0, orderType='MARKET')
                print(data)
                curs.execute(isql, (row[11]))
                
            elif price <= now_price and row[7] == 'downwdbreak' and row[9] == 'limit':
                print(price, now_price, row[7], row[8])
                data = f_order_limit(row[0], binance.SELL, row[10], price + round(Decimal(row[12] if row[12] else 0)), orderType='LIMIT')
                print(data)
                curs.execute(isql, (row[11]))
                
            else:
                data = {}

            try:
                status = data['status']
                if row[9] == 'limit':
                    msg = '[거래체결] ' + row[1]+'/'+row[2] +' / '+ ('상향돌파 ' if row[7] == 'breakthrough' else '하향돌파 ') + ' / '+ ('지정가 ' if row[9] == 'limit' else '시장가 ') +' / '+ str(row[10])+'btc' + ' / price: '+ str(price) +' usdt'+' | oderId:'+str(row[11]) 
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)
                else:
                    msg = '[거래체결] ' + row[1]+'/'+row[2] +' / '+ ('상향돌파 ' if row[7] == 'breakthrough' else '하향돌파 ') + ' / '+ ('지정가 ' if row[9] == 'limit' else '시장가 ') +' / '+ str(row[10])+'btc'+' | oderId:'+str(row[11]) 
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)

            except:
                try:
                    code = data['code']
                    if code == -2019:
                        msg = '[거래오류] ' + row[1]+'/'+row[2]+' | oderId:'+str(row[11])+ ': 금액이 부족합니다.' 
                    else:
                        msg = '[거래오류] ' + row[1]+'/'+row[2]+' | oderId:'+str(row[11])+ ': 기타 오류' 
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)
                except NameError:
                    pass
                except KeyError:
                    pass
                except:
                    msg = '[시스템 에러] 관리자에게 문의 하세요'
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)

        db.commit()

    # 1day
    if int(now.strftime('%M')) in [0] and int(now.strftime('%H')) in [0]:
        
        curs.execute(sql, ('day1', '1', '0'))
        rows = curs.fetchall()
        
        for row in rows:
            
            now_price = ext_tline_query(row[3], row[5], row[4], row[6], row[1], todt)

            # if start
            if price >= now_price and row[7] == 'breakthrough' and row[9] == 'market':
                print(price, now_price, row[7], row[8])
                data = f_order(row[0], binance.BUY, row[10], 0.0, orderType='MARKET')
                print(data)
                curs.execute(isql, (row[11]))

            elif price >= now_price and row[7] == 'breakthrough' and row[9] == 'limit':
                print(price, now_price, row[7], row[8])
                data = f_order_limit(row[0], binance.BUY, row[10], price + round(Decimal(row[12] if row[12] else 0)), orderType='LIMIT')
                print(data)
                curs.execute(isql, (row[11]))

            elif price <= now_price and row[7] == 'downwdbreak' and row[9] == 'market':
                print(price, now_price, row[7], row[8])
                data = f_order(row[0], binance.SELL, row[10], 0.0, orderType='MARKET')
                print(data)
                curs.execute(isql, (row[11]))

            elif price <= now_price and row[7] == 'downwdbreak' and row[9] == 'limit':
                print(price, now_price, row[7], row[8])
                data = f_order_limit(row[0], binance.SELL, row[10], price + round(Decimal(row[12] if row[12] else 0)), orderType='LIMIT')
                print(data)
                curs.execute(isql, (row[11]))

            else:
                data = {}

            try:
                status = data['status']
                if row[9] == 'limit':
                    msg = '[거래체결] ' + row[1]+'/'+row[2] +' / '+ ('상향돌파 ' if row[7] == 'breakthrough' else '하향돌파 ') + ' / '+ ('지정가 ' if row[9] == 'limit' else '시장가 ') +' / '+ str(row[10])+'btc' + ' / price: '+ str(price) +' usdt'+' | oderId:'+str(row[11]) 
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)
                else:
                    msg = '[거래체결] ' + row[1]+'/'+row[2] +' / '+ ('상향돌파 ' if row[7] == 'breakthrough' else '하향돌파 ') + ' / '+ ('지정가 ' if row[9] == 'limit' else '시장가 ') +' / '+ str(row[10])+'btc'+' | oderId:'+str(row[11]) 
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)

            except:
                try:
                    code = data['code']
                    if code == -2019:
                        msg = '[거래오류] ' + row[1]+'/'+row[2]+' | oderId:'+str(row[11])+ ': 금액이 부족합니다.' 
                    else:
                        msg = '[거래오류] ' + row[1]+'/'+row[2]+' | oderId:'+str(row[11])+ ': 기타 오류' 
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)
                except NameError:
                    pass
                except KeyError:
                    pass
                except:
                    msg = '[시스템 에러] 관리자에게 문의 하세요'
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)
        db.commit()

    


    # ---------------- #
    # telegram continue message
    if int(now.strftime('%M'))%5 == 0:
        curs.execute(psql, ('BTCUSDT'))
        price = curs.fetchone()[0]
        alarm_sql = """insert into trading_alarm(orderId) values (%s)"""
        cnt_sql = "select count(*) as cnt from trading_alarm where orderId = %s "
        
        rods = ['min5', 'min15', 'min30', 'hour1', 'hour4', 'day1']

        for rod in rods:
            curs.execute(sql, (rod, '1', '0'))
            rows = curs.fetchall()

            for row in rows:

                now_price = ext_tline_query(row[3], row[5], row[4], row[6], row[1], todt)
                # curs.execute(cnt_sql, (row[11]))
                # cnt = curs.fetchone()[0] 
                # if cnt >= 2:
                #     continue   

                if (price >= now_price and row[7] == 'breakthrough') or (price <= now_price and row[7] == 'downwdbreak'):
                    msg = '[금액도달] ' + row[1]+'/'+row[2] +' / '+ ('상향돌파 ' if row[7] == 'breakthrough' else '하향돌파 ') + ' / '+ ('지정가 ' if row[9] == 'limit' else '시장가 ') +' / '+ str(row[10])+'btc'+' | oderId:'+str(row[11]) 
                    # curs.execute(alarm_sql, (row[11]))
                    #if tline == tline_1:
                        #b.sendMessage(chat_id=chat_id, text=msg)
                else:
                    continue
        db.commit()

    # --------------- #
    db.close()


# extension tline query function
def ext_tline_query(frdate, todate, frprice, toprice, rod, todt):
    if rod == 'min5':
        per = 300
        thd_time = int(time.strftime('%M'))//5
        to_datetime = datetime(year=int(todt[:4]), month=int(todt[4:6]), day=int(todt[6:8]), hour=int(todt[8:10]), minute=thd_time*5)
    elif rod == 'min15':
        per = 900
        thd_time = int(time.strftime('%M'))//15
        to_datetime = datetime(year=int(todt[:4]), month=int(todt[4:6]), day=int(todt[6:8]), hour=int(todt[8:10]), minute=thd_time*15)
    elif rod == 'min30':
        per = 1800
        thd_time = int(time.strftime('%M'))//30
        to_datetime = datetime(year=int(todt[:4]), month=int(todt[4:6]), day=int(todt[6:8]), hour=int(todt[8:10]), minute=thd_time*30)
    elif rod == 'hour1':
        per = 3600
        thd_time = int(time.strftime('%H'))
        to_datetime = datetime(year=int(todt[:4]), month=int(todt[4:6]), day=int(todt[6:8]), hour=thd_time)
    elif rod == 'hour4':
        per = 14400
        thd_time = int(time.strftime('%H'))/4
        to_datetime = datetime(year=int(todt[:4]), month=int(todt[4:6]), day=int(todt[6:8]), hour=thd_time*4)
    else:
        per = 86400
        thd_time = int(time.strftime('%d'))
        to_datetime = datetime(year=int(todt[:4]), month=int(todt[4:6]), day=thd_time,)
        
    xs = [datetime(year=int(frdate[:4]), month=int(frdate[4:6]), day=int(frdate[6:8]), hour=int(frdate[8:10]), minute=int(frdate[10:12])),
            datetime(year=int(todate[:4]), month=int(todate[4:6]), day=int(todate[6:8]), hour=int(todate[8:10]), minute=int(todate[10:12])),
            to_datetime]
    
    diff_min = ((xs[1]-xs[0]).total_seconds())/per
    diff_n_min = ((xs[2]-xs[1]).total_seconds())/per

    diff_price = round(toprice - frprice, 8)
    
    add_price = diff_price/diff_min
    
    return round(toprice+(add_price*diff_n_min),8)

# DB connect function
def db_con():
    db = pymysql.connect(
        host='192.168.0.112',
        user='sslee',
        password='rhddbtjqj',
        charset='utf8mb4',
        database='sslee_DB',
    )
    return db


def f_order_limit(symbol, side, quantity, price, orderType=binance.LIMIT, timeInForce=binance.GTC,
          test=False, **kwargs):
    """Send in a new order.
    Args:
        symbol (str)
        side (str): BUY or SELL.
        quantity (float, str or decimal)
        price (float, str or decimal)
        orderType (str, optional): LIMIT or MARKET.
        timeInForce (str, optional): GTC or IOC.
        test (bool, optional): Creates and validates a new order but does not
            send it into the matching engine. Returns an empty dict if
            successful.
        newClientOrderId (str, optional): A unique id for the order.
            Automatically generated if not sent.
        stopPrice (float, str or decimal, optional): Used with stop orders.
        icebergQty (float, str or decimal, optional): Used with iceberg orders.
    """
    params = {
        "symbol": symbol,
        "side": side,
        "type": orderType,
        "timeInForce": timeInForce,
        "quantity": formatNumber(quantity),
        "price": formatNumber(price),
        "timestamp": int(time.time() * 1000)
    }
    params.update(kwargs)
    # path = "/fapi/v3/order/test" if test else "/fapi/v3/order"
    path = "/fapi/v1/order/"
    data = binance.signedRequest("POST", path, params)
    return data

def f_order(symbol, side, quantity, price, orderType=binance.MARKET, timeInForce=binance.GTC,
          test=False, **kwargs):
    """Send in a new order.
    Args:
        symbol (str)
        side (str): BUY or SELL.
        quantity (float, str or decimal)
        price (float, str or decimal)
        orderType (str, optional): LIMIT or MARKET.
        timeInForce (str, optional): GTC or IOC.
        test (bool, optional): Creates and validates a new order but does not
            send it into the matching engine. Returns an empty dict if
            successful.
        newClientOrderId (str, optional): A unique id for the order.
            Automatically generated if not sent.
        stopPrice (float, str or decimal, optional): Used with stop orders.
        icebergQty (float, str or decimal, optional): Used with iceberg orders.
    """
    params = {
        "symbol": symbol,
        "side": side,
        "type": orderType,
        # "timeInForce": timeInForce,
        "quantity": formatNumber(quantity),
        # "price": formatNumber(price),
        "timestamp": int(time.time() * 1000)
    }
    params.update(kwargs)
    # path = "/fapi/v3/order/test" if test else "/fapi/v3/order"
    path = "/fapi/v1/order/"
    data = binance.signedRequest("POST", path, params)
    return data

def formatNumber(x):
    if isinstance(x, float):
        return "{:.8f}".format(x)
    else:
        return str(x)

sched = BlockingScheduler()
sched.add_job(exec_cron, 'cron', minute='*')

sched.start()
