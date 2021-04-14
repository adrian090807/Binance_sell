from binance.client import Client
from binance.enums import *
from collections import defaultdict
import pandas as pd
import json
import math

keys=pd.read_csv('keys.csv')

client = Client(keys['api_key'][0], keys['api_secret'][0])
PRIMARY = ['EUR','BUSD','USDT']
SECONDARY = ['BNB', 'BTC', 'ETH']
Sell_Perc  = .25

#Get account info

info = client.get_account()
Balance_info = pd.json_normalize(info,record_path=['balances'])
Balance_info
coins = ['']
balances = ['']
for ind in Balance_info.index:
    if  float(Balance_info['free'][ind]) != 0:
        print(Balance_info['asset'][ind], Balance_info['free'][ind])
        coin = Balance_info['asset'][ind]
        for primary in PRIMARY:
            ticker = coin + primary
            try:
                avg_price = client.get_avg_price(symbol=ticker)
                if avg_price != 0:
                    print(ticker, avg_price)
                    print('Balance = ', Balance_info['free'][ind])
                    value = float(Balance_info['free'][ind]) * float(avg_price['price'])
                    print('Value=',value,primary)
                    
            except:
                print(ticker, ' gave an error')
        coins.append(Balance_info['asset'][ind])
        balances.append(Balance_info['free'][ind])
coins.remove('')
balances.remove('')
print(coins, balances)
balancedf=pd.DataFrame({'coins':coins, 'balance':balances})
print(balancedf)
#balancedf=balancedf.drop([0,1,2])

### Sell Sell_Perc x Balance of each coins

for ind in balancedf.index:
    coin = balancedf['coins'][ind]
    if coin in PRIMARY:
        break
    else:
        for primary in PRIMARY:
            ticker = coin + primary
            try:
                avg_price = client.get_avg_price(symbol=ticker)
                if avg_price != 0:
                    print(ticker, avg_price)
                    coin_balance=client.get_asset_balance(asset=coin)['free']
                    print('Balance = ', coin_balance)
                    q=float(Sell_Perc) * coin_balance
                    q=float("{:.8f}".format(q))
                    print(q)

                    try:
                        order = client.order_market_sell(symbol=ticker,quantity=round(q,6))
                    except Exception as a:
                        print(a)
                        if a.message == 'Filter failure: LOT_SIZE':
                                decimal_place = 15
                                while decimal_place > -1:
                                    try:
                                        order = client.order_market_sell(symbol=ticker,quantity=round(q,6))
                                        print(q, decimal_place)
                                        sold1 = True
                                        break
                                    except:
                                        decimal_place -= 1
                                        q = round(float(q), decimal_place)    
                        if decimal_place == -1:
                            order = client.order_market_sell(symbol=ticker,quantity=math.ceil(q))
                            print(math.ceil(q))
                            sold1 = True
                    break
            except Exception as a:
                    print(a)
                    if a.message == 'Invalid symbol':
                        break
                     
            if sold1 == False:
                sold2 = False
            if coin in SECONDARY:
                break
            else:
                for secondary in SECONDARY:
                    ticker = coin + secondary
                    try:
                        avg_price = client.get_avg_price(symbol=ticker)
                        if avg_price != 0:
                            coin_balance=client.get_asset_balance(asset=coin)['free']
                            ibalance = client.get_asset_balance(asset=secondary)['free']
                            print(ticker, avg_price)
                            print('Balance = ', ibalance)
                            q=float(Sell_Perc) * float(coin_balance)
                            q=float("{:.8f}".format(q))
                            print(q)

                            try:
                                order = client.order_market_sell(symbol=ticker,quantity=round(q,6))
                            except Exception as a:
                                print(a)
                                if a.message == 'Filter failure: LOT_SIZE':
                                        decimal_place = 15
                                        while decimal_place > -1:
                                            try:
                                                order = client.order_market_sell(symbol=ticker,quantity=round(q,6))
                                                print(q, decimal_place)
                                                sold2= True
                                                break
                                            except:
                                                decimal_place -= 1
                                                q = round(float(q), decimal_place)   

                        fbalance = client.get_asset_balance(asset=secondary)['free']
                        SecQ = float(fbalance) - float(ibalance)

                        for primary in PRIMARY:
                            ticker = secondary + primary
                        #try:
                            avg_price = client.get_avg_price(symbol=ticker)
                            if avg_price != 0:
                                print(ticker, avg_price)
                                print('Balance = ', Balance_info['free'][ind])
                                q=float(SecQ)
                                q=float("{:.8f}".format(q))
                                print(q)

                                try:
                                    order = client.order_market_sell(symbol=ticker,quantity=round(q,6))
                                except Exception as a:
                                    print(a)
                                    if a.message == 'Filter failure: LOT_SIZE':
                                            decimal_place = 15
                                            while decimal_place > -1:
                                                try:
                                                    order = client.order_market_sell(symbol=ticker,quantity=round(q,6))
                                                    print(q, decimal_place)
                                                    sold = True
                                                    break
                                                except:
                                                    decimal_place -= 1
                                                    q = round(float(q), decimal_place)              
                                break
                    except Exception as a:
                        print(a)
                        if a.message == 'Invalid symbol':
                            break

print(balancedf['balance'][ind])

for ind in Balance_info.index:
    if  float(Balance_info['free'][ind]) != 0:
        print(Balance_info['asset'][ind], Balance_info['free'][ind])
        coin = Balance_info['asset'][ind]
        sold1 = False
        for primary in PRIMARY:
            ticker = coin + primary
            #try:
            avg_price = client.get_avg_price(symbol=ticker)
            if avg_price != 0:
                print(ticker, avg_price)
                print('Balance = ', Balance_info['free'][ind])
                q=float(Sell_Perc) * float(Balance_info['free'][ind])
                q=float("{:.8f}".format(q))
                print(q)
                
                try:
                    order = client.order_market_sell(symbol=ticker,quantity=round(q,6))
                except Exception as a:
                    print(a)
                    if a.message == 'Filter failure: LOT_SIZE':
                            decimal_place = 15
                            while decimal_place > -1:
                                try:
                                    order = client.order_market_sell(symbol=ticker,quantity=round(q,6))
                                    print(q, decimal_place)
                                    sold1 = True
                                    break
                                except:
                                    decimal_place -= 1
                                    q = round(float(q), decimal_place)              
                break
        if sold1 == False:
            sold2 = False
            if coin in SECONDARY:
                break
            else:
                for secondary in SECONDARY:
                    ticker = coin + secondary
                    try:
                        avg_price = client.get_avg_price(symbol=ticker)
                        if avg_price != 0:
                            ibalance = client.get_asset_balance(asset='SECONDARY')
                            print(ticker, avg_price)
                            print('Balance = ', Balance_info['free'][ind])
                            q=float(Sell_Perc) * float(Balance_info['free'][ind])
                            q=float("{:.8f}".format(q))
                            print(q)

                            try:
                                order = client.order_market_sell(symbol=ticker,quantity=round(q,6))
                            except Exception as a:
                                print(a)
                                if a.message == 'Filter failure: LOT_SIZE':
                                        decimal_place = 15
                                        while decimal_place > -1:
                                            try:
                                                order = client.order_market_sell(symbol=ticker,quantity=round(q,6))
                                                print(q, decimal_place)
                                                sold2= True
                                                break
                                            except:
                                                decimal_place -= 1
                                                q = round(float(q), decimal_place)   

                        fbalance = client.get_asset_balance(asset=secondary)
                        SecQ = fbalance['free'] - ibalance['free']

                        for primary in PRIMARY:
                            ticker = secondary + primary
                        #try:
                            avg_price = client.get_avg_price(symbol=ticker)
                            if avg_price != 0:
                                print(ticker, avg_price)
                                print('Balance = ', Balance_info['free'][ind])
                                q=float(SecQ)
                                q=float("{:.8f}".format(q))
                                print(q)

                                try:
                                    order = client.order_market_sell(symbol=ticker,quantity=round(q,6))
                                except Exception as a:
                                    print(a)
                                    if a.message == 'Filter failure: LOT_SIZE':
                                            decimal_place = 15
                                            while decimal_place > -1:
                                                try:
                                                    order = client.order_market_sell(symbol=ticker,quantity=round(q,6))
                                                    print(q, decimal_place)
                                                    sold = True
                                                    break
                                                except:
                                                    decimal_place -= 1
                                                    q = round(float(q), decimal_place)              
                                break
                    except Exception as a:
                        print(a)
                        if a.message == 'Invalid symbol':
                            break

## Get final account info

info = client.get_account()
Balance_info = pd.json_normalize(info,record_path=['balances'])
Balance_info
coins = ['']
for ind in Balance_info.index:
    if  float(Balance_info['free'][ind]) != 0:
        print(Balance_info['asset'][ind], Balance_info['free'][ind])
        coin = Balance_info['asset'][ind]
        for primary in PRIMARY:
            ticker = coin + primary
            try:
                avg_price = client.get_avg_price(symbol=ticker)
                if avg_price != 0:
                    print(ticker, avg_price)
                    print('Balance = ', Balance_info['free'][ind])
                    break
            except:
                print(ticker, ' gave an error')
