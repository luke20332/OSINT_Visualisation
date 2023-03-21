import polars as pl

df = pl.read_csv("../rtf/joined_data.csv")

# convert year data to int
df = df.with_columns([
    pl.col("Order date").cast(pl.Int64, strict=False),
    pl.col("Delivery year").cast(pl.Int64, strict=False)
])

# Convert all the is estimate data to int value
# 1 as Yes; 0 as No
# replaced by the code below now
# for col_name in df.columns:
#     if "is estimate" in col_name:
#         df = df.with_columns([
#             pl.col(col_name)
#             .map(lambda x: 1 if "Yes" in x else 0)]
#         )

# dictionary that store the mapping for those columns that transferred to numeric type
# key is the column name, value is a list of unique type names
category_mapping = {}

# list of columns that required to be transferred to numeric data
# keep country names (seller and buyer) away for now, can be added later
numerical_columns = ["Description", "Armament category",
                     "Order date is estimate", "Numbers delivered",	"Numbers delivered is estimate",
                     "Delivery year is estimate", "Status",	"Local production"]

for col_name in numerical_columns:
    category_mapping[col_name] = df[col_name].unique().to_list()
    df = df.with_columns([
        pl.col(col_name)
        .apply(lambda x: (category_mapping[col_name].index(x)))]
    )

print(category_mapping["Description"])
df.write_csv("joined_data_numeric")
