import MetaTrader5 as mt
from datetime import datetime
import pandas as pd
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
import mplfinance as mpf

mt.initialize()
login = "160386953"
password = "Demoac123"
server = "ForexTimeFXTM-Demo01"

mt.login(login, password, server)

# Set the symbol and timeframe
symbol = "EURUSD"
timeframe = mt.TIMEFRAME_D1  # D1 represents daily

# Define the date range
start_date = datetime(2023, 1, 1)
end_date = datetime.now()

rates = mt.copy_rates_range(symbol, timeframe, start_date, end_date)

mt.shutdown()

data = pd.DataFrame(rates)
data['time'] = pd.to_datetime(data['time'], unit='s')
data.set_index('time', inplace=True)

selected_features = ['open', 'high', 'low', 'close']
X = data[selected_features]


def rel_normalization(X):
    mid = (X['close'] + X['open']) / 2
    X['open'] -= mid
    X['high'] -= mid
    X['low'] -= mid
    X['close'] -= mid
    return X


# Normalize the data
normalized_data = rel_normalization(X)
print(normalized_data)

# Determine the optimal number of clusters using the Elbow method
wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters=i, init='k-means++', random_state=42)
    kmeans.fit(normalized_data)
    wcss.append(kmeans.inertia_)

# Plotting the Elbow method graph
plt.figure(figsize=(8, 6))
plt.plot(range(1, 11), wcss, marker='o', linestyle='--')
plt.title('Elbow Method')
plt.xlabel('Number of clusters')
plt.ylabel('WCSS')  # Within cluster sum of squares
plt.show()

# Based on the Elbow method, choose the optimal number of clusters and fit the KMeans model
num_clusters = 4  # Change this value based on the elbow method graph
kmeans = KMeans(n_clusters=num_clusters, init='k-means++', random_state=42)
kmeans.fit(normalized_data)

# Add cluster labels to the data
data['Cluster'] = kmeans.labels_

# Displaying the clusters
for cluster_id in range(num_clusters):
    cluster_data = data[data['Cluster'] == cluster_id]
    print(f"Cluster {cluster_id}: {len(cluster_data)} candles")

# Visualization (Plotting the clusters)
fig, ax = plt.subplots(figsize=(10, 6))
mpf.plot(X, type='candle', style='yahoo', title='EURUSD OHLC Candles', ylabel='Price')

for cluster_id in range(num_clusters):
    cluster_data = data[data['Cluster'] == cluster_id]
    ax.scatter(cluster_data.index, cluster_data['close'], label=f'Cluster {cluster_id}')

ax.set_title('Candle Clustering - EURUSD')
ax.set_xlabel('Date')
ax.set_ylabel('Close Price')
ax.legend()
plt.show()

print(data)
