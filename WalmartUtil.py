# [Available, Limited Supply, Last few items, Not available]

def encode_stock_level(stock_level):
    map2num = {
        "Not available": 0,
        "Last few items": 1,
        "Limited Supply": 2,
        "Available": 3
    }
    if stock_level not in map2num.keys():
        return 0
    return map2num[stock_level]