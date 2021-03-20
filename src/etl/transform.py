import pandas as pd


def transform(data):

    cleansed = cleanse(data)
    # normalised = normalise(data)

    return cleansed


def cleanse(data):

    # remove customer_info and card_details columns as they contain sensitive data
    sensitive_data = ["customer_info", "card_details"]
    data = data.drop(columns=sensitive_data)

    # ensure datetime column uses datetime type
    # - errors="coerce" makes any datetime that throws an error become a none type
    data["datetime"] = pd.to_datetime(data["datetime"], errors="coerce")
    
    # ensure total_price is a number
    data["total_price"] = pd.to_numeric(data["total_price"], errors="coerce")

    # loop through data frame and check format/types/data
    for x in data.index:

        # if location is not a string, remove the row
        if type(data["location"].iloc[x]) != str:
            data.drop(x, inplace=True)

        # if the total_price is too high, remove the row because it's likely an error
        if data.loc[x, "total_price"] > 50:
            data.drop(x, inplace=True)
            

    # remove any duplicates, if found
    data.drop_duplicates(inplace=True)
    
    # remove rows that contain empty cells
    # this is last because of coerce
    data = data.dropna()

    return data