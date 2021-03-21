import pandas as pd
from pandas.testing import assert_frame_equal

from src.etl.extract import extract


def test_extract():

    test_data = {
        "datetime": ["2021-02-23 17:59:04"],
        "location": ["Isle of Wight"],
        "customer_info": ["Stanley Cordano"],
        "basket": [
            ",Frappes - Coffee,2.75,,Speciality Tea - Darjeeling,1.3,,Smoothies - Berry Beautiful,2.0,Large,Latte,2.45"
        ],
        "payment_method": ["CASH"],
        "total_price": [8.5],
        "card_details": ["None"],
    }

    test_csv = "tests/test_data/test_extract_data.csv"

    actual = extract(test_csv)
    expected = pd.DataFrame(test_data)
    assert_frame_equal(actual, expected)