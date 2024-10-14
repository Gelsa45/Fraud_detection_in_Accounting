# Import necessary libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.neighbors import LocalOutlierFactor
from sklearn.metrics import confusion_matrix, accuracy_score

# Load the dataset
data = pd.read_csv('fraud_0.1origbase.csv')

# Step 1: Data Preprocessing
# Check for missing values
print("Missing values in each column:\n", data.isnull().sum())

# Selecting relevant features for clustering
features = data[['amount', 'oldbalanceOrg', 'newbalanceOrig']]

# Step 2: Standardize the features
scaler = StandardScaler()
scaled_features = scaler.fit_transform(features)

# Step 3: Apply k-Means clustering (with k=2)
kmeans = KMeans(n_clusters=2, random_state=0)
kmeans.fit(scaled_features)

# Add cluster labels to the dataset
data['Cluster'] = kmeans.labels_

# Step 4: Visualize the clusters
plt.scatter(data['amount'], data['oldbalanceOrg'], c=data['Cluster'], cmap='viridis')
plt.xlabel('Amount')
plt.ylabel('Old Balance (Origin)')
plt.title('Clustering of Transactions')
plt.show()

# Step 5: Evaluate the Model
# Compare predicted clusters with actual fraud labels (isFraud)
cm = confusion_matrix(data['isFraud'], data['Cluster'])
print("Confusion Matrix:\n", cm)

# Calculate the accuracy
accuracy = accuracy_score(data['isFraud'], data['Cluster'])
print(f'Model Accuracy: {accuracy}')

# Step 6: Outlier Detection with LOF
lof = LocalOutlierFactor(n_neighbors=20)
outliers = lof.fit_predict(scaled_features)

# Add outliers to the dataset
data['Outlier'] = outliers

# Visualize outliers vs non-outliers
plt.scatter(data['amount'], data['oldbalanceOrg'], c=data['Outlier'], cmap='coolwarm')
plt.xlabel('Amount')
plt.ylabel('Old Balance (Origin)')
plt.title('Outliers Detected by LOF')
plt.show()

# Print summary of outliers
print(data[['amount', 'oldbalanceOrg', 'newbalanceOrig', 'Outlier']].head())

# Optional: Save the dataset with clusters and outliers for further analysis
data.to_csv('fraud_detection_results.csv', index=False)
