import pandas as pd
import numpy as np

pd.set_option("mode.chained_assignment", None)


def transform(data):

    cleansed = cleanse(data)
    normalised = normalise(cleansed)

    return normalised


def cleanse(data):

    # remove customer_info and card_details columns as they contain sensitive data
    sensitive_data = ["customer_info", "card_details"]
    data = data.drop(columns=sensitive_data)

    # lowercase all string fields
    data["location"] = data["location"].str.lower()
    data["basket"] = data["basket"].str.lower()
    data["payment_method"] = data["payment_method"].str.lower()

    # ensure datetime column uses datetime type
    # - errors="coerce" makes any datetime that throws an error become a none type
    data["datetime"] = pd.to_datetime(data["datetime"], errors="coerce")

    # ensure total_price is a number
    data["total_price"] = pd.to_numeric(data["total_price"], errors="coerce")

    # loop through data frame and check format/types/data
    for x in data.index:

        # if location is not a string, remove the row
        if type(data["location"].iloc[x]) != str:
            # inplace=True performs the action on the original dataframe
            data.drop(x, inplace=True, errors="coerce")

        # if payment method is not card or cash, make it a non type for removal
        if data.loc[x, "payment_method"] != "card":
            if data.loc[x, "payment_method"] != "cash":
                data.loc[x] = np.nan

        # if the total_price is too high, remove the row because it's likely an error
        if data.loc[x, "total_price"] > 50:
            data.drop(x, inplace=True, errors="coerce")

    # remove any duplicates, if found
    data.drop_duplicates(inplace=True)

    # remove rows that contain empty cells
    # this is last because of coerce
    data = data.dropna()

    return data


def normalise(data):

    transaction = []

    # loop through each row in data frame
    for i, row in data.iterrows():

        # each row will contain transaction details and one item from the basket
        new_row = {}

        new_row["datetime"] = row[0]
        new_row["location"] = row[1]
        new_row["payment_method"] = row[3]
        new_row["total_price"] = row[4]

        # split basket using commas
        row["basket"] = row["basket"].split(",")

        row["basket"] = list(zip(*[iter(row["basket"])] * 3))

        for item in row["basket"]:
            x = 0
            while x < len(item):
                if item[x] == "":
                    # assuming size is regular if not specified
                    new_row["size"] = "regular"
                else:
                    new_row["size"] = item[x]
                new_row["name"] = item[x + 1]
                new_row["price"] = item[x + 2]
                transaction.append(new_row.copy())
                x += 3

    data = pd.DataFrame(transaction)

    return data