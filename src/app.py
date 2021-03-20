from src.etl.extract import extract
from src.etl.transform import transform

filename = "data/2021-02-23-Isle-of-Wight.csv"

data = extract(filename)
transformed_data = transform(data)

print(transformed_data)