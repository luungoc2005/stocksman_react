from models import Stock, DailyPrice
from datetime import datetime
from pytz import timezone
import codecs
import json

def readfile(filename):
    "Read file and return as string"
    with codecs.open(filename, 'r', 'utf-8-sig') as target:
        return target.read()

def normalize_string(input):
    return input.strip().upper()

def parse_date(obj):
    if 'CloseDate' in obj:
        timestamp = int(obj['CloseDate'][6:-2]) / 1000
        obj['CloseDate'] = datetime.fromtimestamp(timestamp, tz=timezone('Asia/Ho_Chi_Minh'))
    return obj

def price_from_json(json_data):
    "Gets daily price model from json data"
    # Set new daily price data
    # parsed_data = list(json.loads(json_data, encoding='utf-8'))[0]
    parsed_data = list(json.loads(json_data, encoding='utf-8', object_hook=parse_date))[0]
    stock_model = Stock.objects.get(stock_code=normalize_string(parsed_data["StockCode"]))
    # Map new price
    new_price = DailyPrice()
    new_price.stock = stock_model
    # Price fields
    new_price.close_date = parsed_data["CloseDate"]
    new_price.open_price = parsed_data["OpenPrice"]
    new_price.close_price = parsed_data["ClosePrice"]
    new_price.avg_price = parsed_data["AvrPrice"]
    new_price.floor_price = parsed_data["FloorPrice"]
    new_price.ceiling_price = parsed_data["CeilingPrice"]
    new_price.highest = parsed_data["Highest"]
    new_price.lowest = parsed_data["Lowest"]
    new_price.oscillate = parsed_data["Oscillate"]
    # Other integer fields
    new_price.dividend = parsed_data["Dividend"]
    new_price.eps = parsed_data["EPS"]
    new_price.buy_redundancy = parsed_data["BuyRedundancy"]
    new_price.sell_redundancy = parsed_data["SellRedundancy"]
    new_price.bvps = parsed_data["BVPS"]
    new_price.capital_level = parsed_data["CapitalLevel"]
    new_price.curr_room = parsed_data["CurrRoom"]
    new_price.klcplh = parsed_data["KLCPLH"]
    new_price.klcpny = parsed_data["KLCPNY"]
    # Volume
    new_price.avg_vol = parsed_data["AvgVol"]
    new_price.trading_vol = parsed_data["TradingVolume"]
    new_price.total_vol = parsed_data["TotalVal"]
    # Decimals
    new_price.beta = parsed_data["Beta"]
    new_price.dec_pb = parsed_data["PB"]
    new_price.dec_pe = parsed_data["PE"]
    new_price.fw_pe = parsed_data["FwPE"]
    # Raw data
    new_price.raw_json = json_data
    # Set URL to Stock model
    stock_model.url = parsed_data["URL"]
    # save to Db
    new_price.save()

def price_from_file(filename):
    price_from_json(readfile(filename))

