import polars as pl

df = pl.read_csv("../rtf/joined_data.csv")

# convert year data to int
df = df.with_columns([
    pl.col("Order date").cast(pl.Int64, strict=False),
    pl.col("Delivery year").cast(pl.Int64, strict=False)
])

# Convert all the is estimate data to int value
# 1 as Yes; 0 as No
for col_name in df.columns:
    if "is estimate" in col_name:
        df = df.with_columns([
            pl.col(col_name)
            .map(lambda x: 1 if "Yes" in x else 0)]
        )

print(df["Order date is estimate"].dtype)
