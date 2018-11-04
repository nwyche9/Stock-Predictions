# where we will handle the data
import requests


def get_data(symbol, start, end):
    base_url = 'https://marketdata.websol.barchart.com/getHistory.json'
    api_key = 'f89392b5bae2f7e9737a66feaba2d376'
    params = {'apikey': api_key, 'symbol': symbol, 'type': 'daily', 'startDate': start, 'endDate': end}
    response = requests.get(base_url, params)
    print(response.url)
    return response.json()


# used to transfer json return data into the arrays needed
def decode_json(json_data):
    open_price = []
    close_price = []
    highs = []
    lows = []
    volume = []
    results = json_data.get('results')

    for result in results:
        open_price.append(result.get('open'))
        close_price.append(result.get('close'))
        highs.append(result.get('high'))
        lows.append(result.get('low'))
        volume.append(result.get('volume'))

    return open_price, close_price, highs, lows, volume


# calculating difference in values from start to end(current) inputs
# if increase store a 1, if decrease store a 0
def calculate(input_array):
    differences = []
    for i in range(len(input_array) - 1):
        difference = input_array[i + 1] - input_array[i]
        if difference >= 0:
            differences.append(1)
        else:
            differences.append(0)
        return differences


# difference in open price of end day and close price of previous day
# if open price for the end day is higher than close price of previous day store [1,0] else [0,1]
def calculate_price(open_price, close_price):
    price_difference = []
    for i in range(len(open_price) - 1):
        difference = open_price[i + 1] - close_price[i]
        if difference >= 0:
            price_difference.append([1, 0])
        else:
            price_difference.append([0, 1])
        return price_difference


# getting data find diffs assigns labels and makes array of variables and putting them in a new array
# will be used fro training and testing
def build_subsets(symbol: object, start: object, end: object) -> object:
    # getting the data
    json_data = get_data(symbol, start, end)
    open_price, close_price, highs, lows, volume = decode_json(json_data)
    # doing the calculations
    open_diffs = calculate(open_price)
    close_diffs = calculate(close_price)
    highs_diffs = calculate(highs)
    lows_diffs = calculate(lows)
    volume_diffs = calculate(volume)

    labels = calculate_price(open_price, close_price)
    # new array
    final = []
    # putting the values into the final array
    for i in range(len(open_diffs)):
        final.append([open_diffs[i], close_diffs[i], highs_diffs[i], lows_diffs[i], volume_diffs[i]])

    return final, labels
