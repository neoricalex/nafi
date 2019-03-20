import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import sklearn
from sklearn.preprocessing import scale
from sklearn.cluster import KMeans
from sklearn import metrics

iris = pd.read_csv('./dados/historico_EURUSD.csv')
X = iris.iloc[:, 0:1].values
scale(X)

kmeans = KMeans(n_clusters = 3, init = 'random')
kmeans.fit(X)

'''
Neste momento já temos os dados agrupados e vamos verificar os centroides gerados através do atributo cluster_centers_.

kmeans.cluster_centers_
'''
distance = kmeans.fit_transform(X)
#distance
labels = kmeans.labels_
#labels

wcss = []
 
for i in range(1, 21):
    kmeans = KMeans(n_clusters = i, init = 'random')
    kmeans.fit(X)
    print(i,kmeans.inertia_)
    wcss.append(kmeans.inertia_) 

plt.plot(range(1, 21), wcss)
plt.title('O Metodo Elbow')
plt.xlabel('Numero de Clusters')
plt.ylabel('WSS') #within cluster sum of squares
plt.show()

plt.scatter(X[:, 0], X[:,1], s = 100, c = kmeans.labels_)
plt.scatter(kmeans.cluster_centers_[:, 0], kmeans.cluster_centers_[:, 1], s = 300, c = 'red',label = 'Centroids')
plt.title('Iris Clusters and Centroids')
plt.xlabel('SepalLength')
plt.ylabel('SepalWidth')
plt.legend()

plt.show()

#def bench_k_means(estimator, name, data):
#    estimator.fit(data)
#    print('%-9s\t%i\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f\t%.3f'
#          % (name, estimator.inertia_,
#             metrics.homogeneity_score(y, estimator.labels_),
#             metrics.completeness_score(y, estimator.labels_),
#             metrics.v_measure_score(y, estimator.labels_),
#             metrics.adjusted_rand_score(y, estimator.labels_),
#             metrics.adjusted_mutual_info_score(y,  estimator.labels_),
#             metrics.silhouette_score(data, estimator.labels_,
#                                      metric='euclidean')))
#
#clf = KMeans(n_clusters=k, init="random", n_init=1)
#bench_k_means(clf, "1", data)