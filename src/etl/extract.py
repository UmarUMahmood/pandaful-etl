import pandas as pd


def extract(filename):

    # use these as headers for data frame
    headers = [
        "datetime",
        "location",
        "customer_info",
        "basket",
        "payment_method",
        "total_price",
        "card_details",
    ]

    data = pd.read_csv(filename, names=headers)

    return data