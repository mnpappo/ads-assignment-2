"""
ADS-1 Assignment 2: Statistics and trends

Author: Md Nadimozzaman Pappo <mnpappo@gmail.com>
Date: 10-12-2023
Used Python Version: 3.11.4
Format: Black
"""


import pandas as pd
import matplotlib.pyplot as plt

# World Bank data CSV file path
# Download data as a Zip file and unzip it, folder name and version can be different :(
# Data: https://data.worldbank.org/topic/climate-change
file_path = "./API_19_DS2_en_csv_v2_5998250/API_19_DS2_en_csv_v2_5998250.csv"

# Read the CSV data
df = pd.read_csv(file_path, skiprows=4)
print(df.columns)
print(df.head())
print(df.describe())

# CO2 Indicators
# indicators = [
#     "EN.ATM.CO2E.SF.KT",
#     "EN.ATM.CO2E.LF.KT",
#     "EN.ATM.CO2E.KT",
#     "EN.ATM.CO2E.GF.KT",
# ]

# Electricity Indicators
indicators = [
    "EG.ELC.RNEW.ZS",
    "EG.ELC.PETR.ZS",
    "EG.ELC.NUCL.ZS",
    "EG.ELC.COAL.ZS",
]


def process_data(indicators, df):
    """
    Process and clean the data
    params: indicators, df
    return: df, df_transposed
    """
    # Filter the data for the USA and China
    usa_data = df[
        (df["Country Code"] == "USA") & (df["Indicator Code"].isin(indicators))
    ]
    china_data = df[
        (df["Country Code"] == "CHN") & (df["Indicator Code"].isin(indicators))
    ]

    # Combine USA and China data
    combined_data = pd.concat([usa_data, china_data])

    # Make suer 'Year' columns are integers and get their list
    year_columns = [col for col in combined_data if col.isnumeric()]

    # Set the 'Country Code' and 'Indicator Code' as index
    combined_data.set_index(["Country Code", "Indicator Code"], inplace=True)

    # Transpose the data to have years as rows
    combined_data_transposed = combined_data[year_columns].transpose()
    print(combined_data_transposed.head())
    print(combined_data_transposed.describe())

    # Convert the index to datetime, now index represents years
    combined_data_transposed.index = pd.to_datetime(
        combined_data_transposed.index, format="%Y"
    )

    # Convert all columns to numeric data type
    combined_data_transposed = combined_data_transposed.apply(
        pd.to_numeric, errors="coerce"
    )
    return combined_data, combined_data_transposed


combined_data, combined_data_transposed = process_data(indicators, df)


def visualize_data(combined_data_transposed, indicators):
    """
    Visualize the data
    params: combined_data_transposed, indicators
    return: None
    """
    # plot row col layout calculation #
    # Number of rows for the subplots
    num_rows = (len(indicators) + 1) // 2

    # Prepare the figure layout with 2 columns
    fig, axes = plt.subplots(nrows=num_rows, ncols=2, figsize=(14, 6 * num_rows))

    # Flatten the axes array for easy iteration
    axes = axes.flatten()

    # Loop through each indicator and plot it
    for index, indicator in enumerate(indicators):
        ax = axes[index]

        # Plot USA data
        ax.plot(
            combined_data_transposed.index,
            combined_data_transposed[("USA", indicator)],
            label=f"USA {indicator}",
            # label=combined_data.at[indicator, "Indicator Name"],
            marker="o",
        )
        # Plot China data
        ax.plot(
            combined_data_transposed.index,
            combined_data_transposed[("CHN", indicator)],
            label=f"China {indicator}",
            marker="^",
        )

        # Adding labels and title to each subplot
        ax.set_xlabel("Year")
        ax.set_ylabel("Values")
        ax.set_title(f"{indicator} Over Time")
        ax.legend()
        ax.grid(True)

    # Adjust layout
    plt.tight_layout()
    plt.show()


visualize_data(combined_data_transposed, indicators)
