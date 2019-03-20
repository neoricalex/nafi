import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import scale

df = pd.DataFrame({
    'x': [1,2,3,4,5,6,7,8,9],
    'y': [1,2,3,4,5,6,7,8,9]
})
df = scale(df)

kmeans = KMeans(n_clusters = 3)
kmeans.fit(df)

labels = kmeans.predict(df)
centroids = kmeans.cluster_centers_

print(centroids)