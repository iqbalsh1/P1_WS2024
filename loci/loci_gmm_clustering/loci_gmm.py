"""
This script applies Gaussian Mixture Model (GMM) clustering, 
performs causal inference using LOCI on clusters, aggregates the results of clusters.
Dip Test has already been performed on these pairs, and they have been identified 
as X and Y both multimodal/bimodal. 

"""

import pandas as pd
import matplotlib.pyplot as plt
from causa.loci import loci
from sklearn.mixture import GaussianMixture
import os

# Manually specify the dataspairs and corresponding results folder
# 0005, 0006, 0007, 0008, 0016, 0017, 0019, 0033, 0036, 0040, 0043, 0044, 0045, 0046, 0047, 
# 0065, 0066, 0067, 0068, 0069, 0070, 0086, 0087, 0094, 0099, 0101, 0107

file_path = "data/datapairs/pair0107.txt" 
res_folder = "results/pair0107"

# Step 1: Load dataset
try:
    data = pd.read_csv(file_path, sep=r'\s+', header=None, names=['X', 'Y'])

    print("Data loaded successfully!")

except Exception as e:
    print(f"Error loading or processing data: {e}")
    exit()

# Step 2: Create results folder if it doesn't exist
os.makedirs(res_folder, exist_ok=True)

# Step 3: Scatter plot
scatterplot_path = os.path.join(res_folder, "scatterplot.png")
plt.scatter(data['X'], data['Y'], alpha=0.5)
plt.xlabel("X")
plt.ylabel("Y")
plt.savefig(scatterplot_path)
plt.close()

# Step 4: Clustering using Gaussian Mixture Model (GMM)
gmm = GaussianMixture(n_components=2, random_state=42)  
data['Cluster'] = gmm.fit_predict(data[['Y']])

# Step 5: Plot clusters
clusterplot_path = os.path.join(res_folder, "clusters_pairs.png")
plt.scatter(data['X'], data['Y'], c=data['Cluster'], cmap='viridis', alpha=0.5)
plt.title("Scatterplot with Clusters")
plt.xlabel("X")
plt.ylabel("Y")
plt.savefig(clusterplot_path)
plt.close()

# Step 6: Perform causal inference method LOCI on clusters
directions = []
for cluster in data['Cluster'].unique():
    subset = data[data['Cluster'] == cluster]
    score = loci(subset['Y'].values, subset['X'].values)
    if score > 0:
        directions.append("X → Y")
    elif score < 0:
        directions.append("Y → X")
    else:
        directions.append("Undecided")

# Step 7: Aggregate results from all clusters
if len(set(directions)) == 1:  # If all clusters agree
    final_direction = directions[0]
else:
    final_direction = "Undecided"

# Step 8: Save results to a file
results_path = os.path.join(res_folder, "results.txt")
with open(results_path, "w", encoding="utf-8") as f:
    f.write("Results Summary:\n")
    f.write(f"Clusters causal inference results: {directions}\n")
    f.write(f"Inferred Causal Direction: {final_direction}\n")
    f.write("Ground Truth: X → Y\n")

print(f"Results saved to {results_path}")
print(f"Scatterplot saved to {scatterplot_path}")
print(f"Clustered scatterplot saved to {clusterplot_path}")
