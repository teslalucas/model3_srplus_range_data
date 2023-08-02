from cProfile import label
import pandas as pd
import matplotlib.pyplot as plt
import json
import numpy as np

# Load data from JSON file
with open('data.json') as f:
    data = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(data)

# Group by 'batt_lvl' and calculate the mean and variance
grouped_mean = df.groupby('batt_lvl').mean()[['est_batt_range_km', 'rated_batt_range_km']]
grouped_var = df.groupby('batt_lvl').var()[['est_batt_range_km', 'rated_batt_range_km']]

# Reverse the DataFrame
grouped_mean = grouped_mean.sort_index(ascending=False)
grouped_var = grouped_var.sort_index(ascending=False)

# Plot mean with variance as error bars
plt.figure(figsize=(10,6))
for column in grouped_mean.columns:
    plt.plot(grouped_mean.index, grouped_mean[column], label=column)
plt.plot([100, 0], [300, 0], linestyle="--", color="green", label="Realworld range on Highway")  
plt.legend()
plt.xlabel('Battery Level')
plt.ylabel('Average Range (km)')
plt.title('Average Ranges by Battery Level with Variance')
plt.xlim(100, 0)  # Flip the x-axis
plt.savefig("average_range_at_bat_precentage.png")
plt.xlim(60, 40)
plt.savefig("average_range_at_bat_precentage_60_40.png")


plt.figure(figsize=(20,6))
plt.bar(grouped_mean.index, grouped_mean["est_batt_range_km"]/(grouped_mean.index*3), label="")
plt.plot([100, 0], [1, 1], linestyle="--", color="green", label="Perfect prediction")  
plt.legend()
plt.xlabel('Battery Level')
plt.ylabel('Factor')
plt.title('range overreporting at battery level')
plt.xlim(100, 0)  # Flip the x-axis
plt.savefig("range_overreporting_vs_bat_prec.png")
plt.xlim(60, 40)
plt.savefig("range_overreporting_vs_bat_prec_60_40.png")