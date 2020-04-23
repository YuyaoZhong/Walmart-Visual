import random
import time
import decimal
import mysql.connector
from datetime import datetime, timedelta
from WalmartUtil import encode_stock_level

from flask import Flask, Response, render_template, jsonify, json

# Modifying Python Json encoder to allow it to accept DECIMAL
class MyJSONEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        return super(MyJSONEncoder, self).default(obj)

app = Flask(__name__)
app.json_encoder = MyJSONEncoder
app.config['SEND_FILE_MAX_AGE_DEFAULT']=timedelta(seconds=1)
random.seed()  

@app.route('/')
def index():
    mydb = mysql.connector.connect(
    host="database-1.ce3fedwq8bda.us-east-1.rds.amazonaws.com",
    port=3306,
    user="admin",
    password="AXiF6Z46SiBUZopw9xgw",
    database="walmartTrack"
    )

    mycursor = mydb.cursor()
    mycursor.execute("SELECT productID, name FROM products ORDER BY name")
    items = [d[0] for d in mycursor.description] # get the column
    # list of dictionary as items: {productId: int, name: string}
    products = [dict(zip(items, row)) for row in mycursor.fetchall()]
    return render_template('plotting.html', products=products)


# @app.route('/<int:productID>')
# def index(productID):
#     product  = tracker(productID)
#     return render_template('index.html', name = product['name'], imageURL = product['imageURL'], productID=productID)


# Live Route, this route provides a live stream for data
# @app.route('/chart-data/<int:productID>')
# def chart_data(productID):
#     # products = {
#     # '53084870' : 'Method All Purpose Wipes Lime and Sea Salt - 70ct',
#     # '75663300' : 'Charmin Ultra Soft Toilet Paper - 24 Mega Rolls',
#     # '53398642' : 'Clorox Scentiva Wipes Bleach Free Cleaning Wipes - Tuscan Lavender & Jasmine - 70ct',
#     # '11454824' : 'Isopropyl 70% Alcohol Antiseptic - 32oz',
#     # '11633443' : 'Hand Sanitizer - Up&Up',
#     # '50953424' : 'Purell Advanced Hand Sanitizer Refreshing Gel Pump Bottle - 33.8 fl oz'
#     # }
    
#     def generate_random_data():
#         # while True:
#         #     json_data = json.dumps(
#         #         {'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': random.random() * 20})
#         #     yield f"data:{json_data}\n\n"
#         #     # print(f"data:{json_data}\n\n")
#         #     time.sleep(1)
#         while True:
#             product  = tracker(productID)
#             json_data = json.dumps({'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': product['onlineStock'], 'price': product['price']})
#             yield f"data:{json_data}\n\n"
#             print(json_data)
#             time.sleep(5)

#     return Response(generate_random_data(), mimetype='text/event-stream')

@app.route('/product-data/<int:productID>')
def product_data(productID):
    mydb = mysql.connector.connect(
    host="database-1.ce3fedwq8bda.us-east-1.rds.amazonaws.com",
    port=3306,
    user="admin",
    password="AXiF6Z46SiBUZopw9xgw",
    database="walmartTrack"
    )
    mycursor = mydb.cursor()

    mycursor.execute("SELECT stockLevel, price, scrapetime FROM products_price WHERE productID =%s", (productID,))
    items = [d[0] for d in mycursor.description]
    # print(items)
    data = [dict(zip(items, row)) for row in mycursor.fetchall()]
    # encode stock level to be number
    for item in data:
        item['stockLevel'] = encode_stock_level(item['stockLevel'])
    # print(data)
    return jsonify(data)

@app.route('/product-data-time-series/<int:productID>')
def product_data_time(productID):
    mydb = mysql.connector.connect(
    host="database-1.ce3fedwq8bda.us-east-1.rds.amazonaws.com",
    port=3306,
    user="admin",
    password="AXiF6Z46SiBUZopw9xgw",
    database="walmartTrack"
    )

    mycursor = mydb.cursor()
    # todo: modified to number the stock level
    mycursor.execute("SELECT scrapetime, stockLevel FROM products_price WHERE productID =%s", (productID,))
    # items = [d[0] for d in mycursor.description]
    items = ['t', 'y']
    # print(items)
    data = [dict(zip(items, row)) for row in mycursor.fetchall()]
    print(data)
    for item in data:
        item['y'] = encode_stock_level(item['y'])
    for i in range(len(data)):
        data[i]['t'] = data[i]['t'].timestamp()*1000
    # print(data)

    return jsonify(data)

@app.route('/product-info/<int:productID>')
def product_info(productID):
    mydb = mysql.connector.connect(
    host="database-1.ce3fedwq8bda.us-east-1.rds.amazonaws.com",
    port=3306,
    user="admin",
    password="AXiF6Z46SiBUZopw9xgw",
    database="walmartTrack"
    )

    mycursor = mydb.cursor()

    mycursor.execute("SELECT name, largeImage imagehref, productUrl href FROM products WHERE productID =%s", (productID,))
    items = [d[0] for d in mycursor.description]
    data = [dict(zip(items, row)) for row in mycursor.fetchall()]
    # print(data)
    return jsonify(data)

if __name__ == '__main__':
    app.run(port=5000, debug=True, threaded=True)