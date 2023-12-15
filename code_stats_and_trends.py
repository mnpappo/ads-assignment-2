"""
ADS-1 Assignment 2: Statistics and trends

Author: Md Nadimozzaman Pappo <mnpappo@gmail.com>
Date: 10-12-2023
Used Python Version: 3.11.4
Format: Black
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# World Bank data CSV file path
# Download data as a Zip file and unzip it, folder name and version can be different :(
# Data: https://data.worldbank.org/topic/climate-change
file_path = "./API_19_DS2_en_csv_v2_5998250/API_19_DS2_en_csv_v2_5998250.csv"

# Read the CSV data
df = pd.read_csv(file_path, skiprows=4)


def explore_statistics(df):
    """
    Explore statistical properties
    params: df
    return: None
    """
    print(df.describe())


# CO2 Indicators
indicators_co2 = [
    "EN.ATM.CO2E.SF.KT",
    "EN.ATM.CO2E.LF.KT",
    "EN.ATM.CO2E.KT",
    "EN.ATM.CO2E.GF.KT",
]

# Electricity Indicators
indicators_elec = [
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

    # Convert the index to datetime, now index represents years
    combined_data_transposed.index = pd.to_datetime(
        combined_data_transposed.index, format="%Y"
    )

    # Convert all columns to numeric data type
    combined_data_transposed = combined_data_transposed.apply(
        pd.to_numeric, errors="coerce"
    )
    return combined_data, combined_data_transposed


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


# visalize heat map
# def visualize_heat_map(combined_data_transposed, indicators):
#     """
#     Visualize the data
#     params: df
#     return: None
#     """
#     # Normalize the data for heatmap
#     normalized_data = (combined_data_transposed - combined_data_transposed.min()) / (
#         combined_data_transposed.max() - combined_data_transposed.min()
#     )

#     for indicator in indicators:
#         plt.figure(figsize=(10, 8))

#         # Get the data for the heatmap
#         heatmap_data = normalized_data.xs(
#             indicator, level="Indicator Code", axis=1
#         ).values

#         # Create the heatmap
#         plt.imshow(heatmap_data, aspect="auto", cmap="viridis")

#         # Add color bar
#         plt.colorbar()

#         # Add titles and labels
#         plt.title(f"Heatmap of {indicator}")
#         plt.ylabel("Year")
#         plt.xlabel("Country")

#         # Set the y-axis labels to years
#         plt.yticks(
#             np.arange(len(combined_data_transposed.index)),
#             [year.year for year in combined_data_transposed.index],
#         )

#         # Set the x-axis labels to countries
#         plt.xticks(np.arange(2), combined_data_transposed.columns.levels[0])

#         plt.show()


explore_statistics(df)
# CO2 data
combined_data_co2, combined_data_transposed_co2 = process_data(indicators_co2, df)
explore_statistics(combined_data_transposed_co2)
visualize_data(combined_data_transposed_co2, indicators_co2)

# Electricity data
combined_data_elec, combined_data_transposed_elec = process_data(indicators_elec, df)
explore_statistics(combined_data_transposed_elec)
visualize_data(combined_data_transposed_elec, indicators_elec)

# visualize_heat_map(combined_data_transposed, indicators)
