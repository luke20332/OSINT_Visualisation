import polars as pl
import pandas as pd
import re


def read_csv_data(filename):
    # read the column names from the file
    with open(filename, 'r') as file:
        for i in range(5):
            file.readline()
        column_names = file.readline().strip().split(';')

    # read the data into a polars dataframe
    df = pd.read_csv(filename, skiprows=5, delimiter=';', skipfooter=2, engine='python', encoding="ISO-8859-1")

    return pl.from_pandas(df)


def replace_unicode_chars(df: pl.DataFrame, col_name: str) -> pl.Series:
    # Get the column to be iterated
    col = df[col_name]
    regex = re.compile(r"\\u(\d+)\?")
    # Iterate through each row in the column
    for i, val in enumerate(col):
        # Check if the value contains a unicode character
        match = regex.search(val)
        if match:
            # Extract the unicode character code from the string
            hex_code = val.split("\\u")[1].split("?")[0]
            # Convert the hex code to an integer and then to its corresponding unicode character
            char = chr(int(hex_code))

            # Replace the original value with the new value containing the unicode character
            col[i] = val.replace(match.group(), char)

    return col


def strip_strings(x):
    if isinstance(x, str):
        return x.strip()
    else:
        return x


def rtf_data_processing(df):
    df = df.with_columns([
        pl.col('Year(s) Weapon of Order')
        .map(lambda x: 'Yes' if '(' in x and ')' in x else 'No').alias("is estimated year order")
    ])

    # define lambda function to remove parentheses
    def remove_parentheses(s: str) -> str:
        return s.replace('(', '').replace(')', '').strip()

    df = df.with_columns(df['Year(s) Weapon of Order'].apply(lambda x: remove_parentheses(x)))
    df = df.with_columns([
        pl.col('Year(s) Weapon of Order')
        .cast(pl.Int64)
    ])

    return df


def joinedTable(df_rtf, csv_df):
    processedDF = rtf_data_processing(df_rtf)
    # remove possible spaces for the designations
    csv_df = csv_df.with_columns(csv_df['Designation'].str.strip())

    processedDF = processedDF.with_columns(replace_unicode_chars(df_rtf, "No. Designation"))
    processedDF = processedDF.with_columns(replace_unicode_chars(df_rtf, "No. Comments"))

    joinedDF = csv_df.join(processedDF,
                           left_on=['Seller', 'Buyer',
                                    'Designation', 'Order date',
                                    ],
                           right_on=["Supplier", "Recipient",
                                     "No. Designation", 'Year(s) Weapon of Order',
                                     ],
                           how="left")
    joinedDF = joinedDF.select(
        ['Deal ID', 'Seller', 'Buyer', 'Designation', 'Description', 'Armament category', 'Order date',
         'Order date is estimate', 'Numbers delivered', 'Numbers delivered is estimate', 'Delivery year',
         'Delivery year is estimate', 'Status', 'SIPRI estimate', 'TIV deal unit', 'TIV delivery values',
         'Local production', 'No. Comments'])

    return joinedDF


if __name__ == '__main__':
    print(read_csv_data("DealsAndTIVs-2023-03-11-16_22_41 (1).txt").columns
          )
