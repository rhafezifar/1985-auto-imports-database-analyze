import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

header_names = [
    "symboling", "normalized-losses", "make", "fuel-type", "aspiration",
    "num-of-doors", "body-style", "drive-wheels", "engine-location", "wheel-base",
    "length", "width", "height", "curb-weight", "engine-type",
    "num-of-cylinders", "engine-size", "fuel-system", "bore", "stroke",
    "compression-ratio", "horsepower", "peak-rpm", "city-mpg", "highway-mpg", "price"
]

df = pd.read_csv("imports-85.data", names=header_names, na_values="?")
# *********************************************************************
# Question 1
fourwd = []
fwd = []
rwd = []

for row in df.index:
    if df["drive-wheels"][row] == "4wd":
        fourwd.append(df["price"][row])
    elif df["drive-wheels"][row] == "fwd":
        fwd.append(df["price"][row])
    else:
        rwd.append(df["price"][row])

# print(fourwd)
# print(fwd)
# print(rwd)

df_4wd = pd.DataFrame({"price": fourwd})
df_fwd = pd.DataFrame({"price": fwd})
df_rwd = pd.DataFrame({"price": rwd})

mean_4wd = df_4wd.mean()
mean_fwd = df_fwd.mean()
mean_rwd = df_rwd.mean()

# print(f"mean price of 4wd cars is: {mean_4wd[0]:.3f}")
# print(f"mean price of 4wd cars is: {mean_fwd[0]:.3f}")
# print(f"mean price of 4wd cars is: {mean_rwd[0]:.3f}")

# filling missing values with mean of 4wd,fwd, and rwd
for row in df.index:
    if pd.isna(df['price'][row]):
        if df["drive-wheels"][row] == "4wd":
            df["price"][row] = mean_4wd['price']
        elif df["drive-wheels"][row] == "fwd":
            df["price"][row] = mean_fwd['price']
        else:
            df["price"][row] = mean_rwd['price']

# print(df["price"])
# print(df.describe())
# *****************************************************************
# Question 2

df_price = pd.DataFrame({"price": df["price"]})

# Calculating z-score for price attribute:
for column in df_price.columns:
    df_price["z-score"] = (df_price[column] - df_price[column].mean())/df_price[column].std()

# Detecting outliers using z-score:
outlier_price = {"price": [], "z-score": []}

for row in df_price.index:
    if df_price["z-score"][row] > 3 or df_price["z-score"][row] < -3:
        outlier_price["price"].append(df_price["price"][row])
        outlier_price["z-score"].append(df_price["z-score"][row])
# print(f"detecting outliers by z-score: {outlier_price}")

# Detecting outliers using 1.5*IQR:
Q1 = df_price["price"].quantile(0.25)
Q3 = df_price["price"].quantile(0.75)
IQR = Q3 - Q1
IQR2 = 1.5 * IQR

outlier_price2 = []
for row in df_price.index:
    if df_price["price"][row] < Q1 - IQR2 or df_price["price"][row] > Q3 + IQR2:
        outlier_price2.append(df_price["price"][row])
# print(f"detecting outliers by IQR: {outlier_price2}")

# *********************************************************************************
# Question3

stat_length = {"min": [], "max": [], "mean": [], "range": []}
stat_compressionRatio = {"min": [], "max": [], "mean": [], "range": []}

# Calculating min,max, and mean of Length attribute:
statLength = df["length"].describe()
stat_length["min"].append(statLength[3])
stat_length["max"].append(statLength[7])
stat_length["mean"].append(statLength[1])
stat_length["range"].append(statLength[7] - statLength[3])
# print("statistic for length attribute:", stat_length)

# Calculating min,max, and mean of compression-ratio attribute:
statCompression = df["compression-ratio"].describe()
stat_compressionRatio["min"].append(statCompression[3])
stat_compressionRatio["max"].append(statCompression[7])
stat_compressionRatio["mean"].append(statCompression[1])
stat_compressionRatio["range"].append(statCompression[7] - statCompression[3])
# print("statistic for compression-ratio attribute:", stat_compressionRatio)

# Min-max normalization for length attribute to [0, 1]:
min_max_Length = []
for row in df.index:
    min_max_Length.append((df["length"][row] - statLength[3]) / (statLength[7] - statLength[3]))
df["Min-max Length"] = min_max_Length
# print("Min-max Length:\n", df["Min-max Length"])

# z-score normalization for length attribute:
z_score_Length = []
for row in df.index:
    z_score_Length.append((df["length"][row] - statLength[1]) / statLength[2])
df["z-score Length"] = z_score_Length
# print("z-score Length:\n", df["z-score Length"])

# Min-max normalization for compression-ratio attribute to [0, 1]:
min_max_compression = []
for row in df.index:
    min_max_compression.append((df["compression-ratio"][row] - statCompression[3]) / (statCompression[7] - statCompression[3]))
df["Min-max compression-ratio"] = min_max_compression
# print("Min-max compression-ratio:\n", df["Min-max compression-ratio"])

# z-score normalization for compression-ratio attribute:
z_score_compression = []
for row in df.index:
    z_score_compression.append((df["compression-ratio"][row] - statCompression[1]) / statCompression[2])
df["z-score compression-ratio"] = z_score_compression
# print("z-score compression-ratio:\n", df["z-score compression-ratio"])

# print(df["Min-max Length"].describe())
# print(df["z-score Length"].describe())
# print(df["Min-max compression-ratio"].describe())
# print(df["z-score compression-ratio"].describe())
# ***********************************************************************************************
# Question 4

print(df.corrwith(df['price'], axis='index', method="pearson"))
