import pandas as pd
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

# filling missing values with mean(for numeric values) and mode(for nominal values)
for column in df.columns:
    if df[column].dtypes != object:
        df[column].fillna(df[column].mean(), inplace=True)
        print(column, " mode is: ", df[column].mode())
    else:
        df[column].fillna(df[column].mode()[0], inplace=True)

print(df.describe())
# *****************************************************
# Question 2:
# print boxplot for numeric data
plt.clf()
fig, axs = plt.subplots(6, 3, figsize=(3 * 5, 6 * 5))
i = 0

for column in df.columns:
    if df[column].dtypes != object:
        try:
            axs[i // 3, i % 3].boxplot(df[column])
            axs[i // 3, i % 3].set_title(column, y=-0.15)
            i += 1
        except:
            print("cannot do boxplot for ", column)

plt.savefig(fname="q2")
# ******************************************************
# Question 3:
plt.clf()
df.boxplot(column="price", by="body-style")
plt.savefig(fname="q3")
# ******************************************************
# Question 4:
plt.clf()
hp_category = []
min_hp = 48
max_hp = 288
interval_l = (max_hp - min_hp) / 3
for hp in df["horsepower"]:
    if hp < min_hp + interval_l:
        hp_category.append("Low")
    elif hp < max_hp - interval_l:
        hp_category.append("Medium")
    else:
        hp_category.append("High")
df["hp-category"] = hp_category
df["hp-category"].value_counts().plot.bar(rot=0)
plt.savefig(fname="q4")

# ******************************************************
# Question 5:
plt.clf()
fig, axs = plt.subplots(1, 3, figsize=(20, 6))
ax0 = df.plot.scatter(x="engine-size", y="price", c="DarkBlue", ax=axs[0])
ax1 = df.plot.scatter(x="highway-mpg", y="price", c="DarkRed", ax=axs[1])
ax2 = df.plot.scatter(x="peak-rpm", y="price", c="DarkGreen", ax=axs[2])

plt.savefig(fname="q5")
# ******************************************************
# Question 6:
plt.clf()
wheel_dc = {"4wd": 1, "fwd": 2, "rwd": 3}
style_dc = {"hardtop": 1, "wagon": 2, "sedan": 3, "hatchback": 4, "convertible": 5}
dc = {}
for i in range(len(df)):
    style = df["body-style"][i]
    wheel = df["drive-wheels"][i]
    price = df["price"][i]

    style_numeric = style_dc[style]
    wheel_numeric = wheel_dc[wheel]
    dc_key = (style_numeric, wheel_numeric)
    if dc_key in dc:
        dc[dc_key][0] += 1
        dc[dc_key][1] += price
    else:
        dc[dc_key] = [1, price]

style_list = []
wheel_list = []
mean_price = []
for j in dc:
    style_list.append(j[0])
    wheel_list.append(j[1])
    mean_price.append(dc[j][1]/dc[j][0])

df1 = pd.DataFrame(
    {
        "drive-wheel": wheel_list,
        "body-style": style_list,
        "mean-price": mean_price,
    }
)

# print(df.describe())
ax = df1.plot.scatter(x="body-style", y="drive-wheel", s=df1["mean-price"]/5 - 1000, c="purple", xticks=range(7), yticks=range(5))
ax.set_yticklabels(["", "4WD", "FWD", "RWD", ""])
ax.set_xticklabels(["", "hardtop", "wagon", "sedan", "hatchback", "convertible", ""])
ax.legend(['mean price'], markerscale=0.25)
plt.savefig(fname="q6")
