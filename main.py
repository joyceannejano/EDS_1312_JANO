import pandas as pd

try:
    df = pd.read_csv(
        "data/20210703_greenhouse_data.csv",
        sep=";"
    )

    print("DATASET LOADED SUCCESSFULLY!\n")

    display(df.head())

    print("\nCOLUMN NAMES:")
    print(df.columns)

except Exception as e:
    print("ERROR:")
    print(e)

# %%
import numpy as np

# Convert columns with comma decimals into float
columns_to_convert = [
    'greenhous_temperature_celsius',
    'greenhouse_humidity_percentage',
    'online_temperature_celsius',
    'online_humidity_percentage',
    'greenhouse_equivalent_co2_ppm'
]

for col in columns_to_convert:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(',', '.', regex=False)
    )

    df[col] = pd.to_numeric(df[col], errors='coerce')

# Convert created column into datetime
df['created'] = pd.to_datetime(df['created'])

# Remove duplicates
df.drop_duplicates(inplace=True)

# Remove missing values
df.dropna(inplace=True)

print("DATA CLEANING COMPLETE!\n")

print(df.dtypes)

display(df.head())

# %%
# Convert remaining object columns into numeric

remaining_columns = [
    'greenhouse_illuminance_lux',
    'greenhouse_total_volatile_organic_compounds_ppb'
]

for col in remaining_columns:
    df[col] = (
        df[col]
        .astype(str)
        .str.replace(',', '.', regex=False)
    )

    df[col] = pd.to_numeric(df[col], errors='coerce')

# Remove possible null values after conversion
df.dropna(inplace=True)

print(df.dtypes)

# %%
filtered_df = df[
    (df['greenhous_temperature_celsius'] > 13) &
    (df['greenhouse_humidity_percentage'] < 70) &
    (df['created'].dt.hour >= 12) &
    (df['created'].dt.hour <= 17)
]

print("FILTERED DATASET SHAPE:")
print(filtered_df.shape)

display(filtered_df.head())

# %%
filtered_df.to_csv(
    "data/dataset_cleaned.csv",
    index=False
)

print("CLEANED DATASET SAVED!")

# %%
import numpy as np

temperature = filtered_df['greenhous_temperature_celsius']

mean_temp = np.mean(temperature)
median_temp = np.median(temperature)
std_temp = np.std(temperature)
variance_temp = np.var(temperature)

print("TEMPERATURE STATISTICS\n")

print(f"Mean: {mean_temp}")
print(f"Median: {median_temp}")
print(f"Standard Deviation: {std_temp}")
print(f"Variance: {variance_temp}")

# %%
import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))

plt.hist(
    filtered_df['greenhous_temperature_celsius'],
    bins=15
)

plt.title("Temperature Distribution")
plt.xlabel("Temperature (°C)")
plt.ylabel("Frequency")

plt.savefig("outputs/temperature_histogram.png")

plt.show()

# %%
import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))

plt.boxplot(
    filtered_df['greenhous_temperature_celsius']
)

plt.title("Temperature Boxplot")

plt.ylabel("Temperature (°C)")

plt.savefig("outputs/temperature_boxplot.png")

plt.show()

# %%
import matplotlib.pyplot as plt

plt.figure(figsize=(8,5))

plt.scatter(
    filtered_df['greenhous_temperature_celsius'],
    filtered_df['greenhouse_humidity_percentage']
)

plt.title("Temperature vs Humidity")

plt.xlabel("Temperature (°C)")
plt.ylabel("Humidity (%)")

plt.savefig("outputs/temperature_vs_humidity.png")

plt.show()

# %%
correlation = filtered_df[
    [
        'greenhous_temperature_celsius',
        'greenhouse_humidity_percentage'
    ]
].corr()

print(correlation)

# %%
import seaborn as sns
import matplotlib.pyplot as plt

correlation_matrix = filtered_df.corr(numeric_only=True)

plt.figure(figsize=(10,6))

sns.heatmap(
    correlation_matrix,
    annot=True
)

plt.title("Correlation Heatmap")

plt.savefig("outputs/correlation_heatmap.png")

plt.show()

# %%
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8,5))

x = []
y = []

def animate(i):

    x.append(i)

    y.append(
        filtered_df[
            'greenhous_temperature_celsius'
        ].iloc[i]
    )

    ax.clear()

    ax.plot(x, y)

    ax.set_title("Temperature Trend Over Time")
    ax.set_xlabel("Time Index")
    ax.set_ylabel("Temperature (°C)")

animation = FuncAnimation(
    fig,
    animate,
    frames=len(filtered_df),
    interval=50
)

animation.save(
    "outputs/temperature_animation.gif",
    writer='pillow'
)

plt.show()


# %%
from matplotlib.animation import FuncAnimation
import matplotlib.pyplot as plt

fig, ax = plt.subplots(figsize=(8,5))

x = []
y = []

def animate(i):

    x.append(i)

    y.append(
        filtered_df[
            'greenhouse_humidity_percentage'
        ].iloc[i]
    )

    ax.clear()

    ax.plot(x, y)

    ax.set_title("Humidity Trend Over Time")
    ax.set_xlabel("Time Index")
    ax.set_ylabel("Humidity (%)")

animation = FuncAnimation(
    fig,
    animate,
    frames=100,
    interval=50
)

animation.save(
    "outputs/humidity_animation.gif",
    writer='pillow'
)

plt.show()


