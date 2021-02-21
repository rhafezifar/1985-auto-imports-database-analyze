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
print(f"detecting outliers by z-score: {outlier_price}")

# Detecting outliers using 1.5*IQR:
Q1 = df_price["price"].quantile(0.25)
Q3 = df_price["price"].quantile(0.75)
IQR = Q3 - Q1
IQR2 = 1.5 * IQR

outlier_price2 = []
for row in df_price.index:
    if df_price["price"][row] < Q1 - IQR2 or df_price["price"][row] > Q3 + IQR2:
        outlier_price2.append(df_price["price"][row])
print(f"detecting outliers by IQR: {outlier_price2}")

# *********************************************************************************
# Question3
