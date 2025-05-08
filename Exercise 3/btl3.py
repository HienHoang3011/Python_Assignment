import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

df = pd.read_csv('Exercise 1/result.csv', na_values= ['N/a'])
columns_to_drop = ['Player', 'Nation', 'Position', 'Team', 'GA90', 'Save%','CS%','Penalty_Save%']
df = df.drop(columns= columns_to_drop)
df = df.fillna(df.mean(numeric_only= True))
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

wcss = []
for i in range(1, 11):
    kmeans = KMeans(n_clusters= i, init = 'k-means++', max_iter= 400, n_init= 20, random_state= 42)
    kmeans.fit(X_scaled)
    wcss.append(kmeans.inertia_)
    
plt.plot(range(1,11), wcss)
plt.title("Elbow Method to optimize KMeans Algorithm")
plt.xlabel("Numbers of Clusters")
plt.ylabel("WCSS")
plt.savefig('Exercise 3/elbow_method.png')
print("The result has been saved to elbow_method.png")

kmeans = KMeans(n_clusters= 3, init = 'k-means++', max_iter= 400, n_init=20, random_state= 42)
kmeans.fit(X_scaled)
labels = kmeans.labels_
score = silhouette_score(X_scaled, labels)
print('Silhouette Score: ', score)

pca = PCA(n_components= 2)
X_pca = pca.fit_transform(X_scaled)

plt.figure(figsize= (10, 6))
plt.scatter(X_pca[:, 0], X_pca[:, 1], c=labels, cmap='viridis', s=50, alpha=0.7)
plt.title('2D Cluster Plot using PCA')
plt.xlabel('PCA Component 1')
plt.ylabel('PCA Component 2')
plt.colorbar(label='Cluster Label')
plt.savefig('Exercise 3/Cluster_plot_2D.png')
print("Results have been saved to Cluster_plot_2D.png")