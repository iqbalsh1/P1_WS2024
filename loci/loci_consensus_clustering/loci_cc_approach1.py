# Step 1: Import necessary libraries
import sys
sys.path.append(r'C:\Users\User\Desktop\P1_WS2024\P1_WS2024_1.2\loci\causa\experiment\Consensus_Clustering')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from causa.loci import loci  
import os
# importing consensus clustering module
from consensusClustering import ConsensusCluster

file_path = "data/datapairs/pair0107.txt"
res_folder = "results/loci_cc1"

def create_results_folder(folder_path):

    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Step 2: Load the dataset
def load_data(file_path):
   
    try:
        data = pd.read_csv(file_path, sep=r'\s+', header=None, names=['X', 'Y'])
        print("Data loaded successfully!")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        exit()

# Step 3: Find the optimal number of clusters using silhouette score
def find_optimal_clusters(data, max_clusters=4):

    silhouette_scores = []
    for k in range(2, max_clusters + 1):  
        kmeans = KMeans(n_clusters=k, random_state=42)
        labels = kmeans.fit_predict(data)
        score = silhouette_score(data, labels)
        silhouette_scores.append(score)
    
    return np.argmax(silhouette_scores) + 2  # Return the best k

# Step 4: Perform consensus clustering on best k (max(k_x, k_y) in this case)
def perform_consensus_clustering(data, k_final):

    consensus_clustering = ConsensusCluster(
        cluster=lambda n_clusters: KMeans(n_clusters=n_clusters, random_state=42),
        L=k_final,  # Use k_final for the range of clusters
        K=k_final,  # Fixed to k_final
        H=30,  # Number of resampling iterations
        resample_proportion=0.5  # Proportion of data to sample
    ) 

    # Fit consensus clustering on the full dataset
    consensus_clustering.fit(data.values, verbose=True)

    # Get final cluster labels
    final_labels = consensus_clustering.predict_data(data.values)
    
    return final_labels

# Step 5: Apply LOCI for causal inference on clustered data
def loci_on_clusters(data):
    directions = []  
    scores = []      

    for cluster_label in np.unique(data['Cluster']):
        cluster_data = data[data['Cluster'] == cluster_label]
        clustered_X = cluster_data['X'].values
        clustered_Y = cluster_data['Y'].values

        # Compute LOCI score for the cluster
        score = loci(clustered_Y, clustered_X)
        scores.append(score)

        # Determine direction based on the score
        if score > 0:
            inferred_direction = "X → Y"
        elif score < 0:
            inferred_direction = "Y → X"
        else:
            inferred_direction = "Undecided"

        directions.append(inferred_direction)

    # Aggregate scores
    overall_score = np.mean(scores)

    # Determine overall direction based on cluster directions
    if directions.count("X → Y") > directions.count("Y → X"):
        final_direction = "X → Y"
    elif directions.count("Y → X") > directions.count("X → Y"):
        final_direction = "Y → X"
    else:
        final_direction = "Undecided"

    return final_direction, directions, overall_score


def save_results(score, inferred_direction, res_folder, cluster_directions):
    create_results_folder(res_folder)
    results_path = os.path.join(res_folder, "result_loci_cc.txt")
    
    # Save the aggregated direction
    with open(results_path, "a", encoding="utf-8") as f:
        f.write(f"LOCI: {inferred_direction}\n")
        f.write(f"LOCI Score: {score}\n")
        f.write(f"Cluster Directions: {', '.join(cluster_directions)}\n")
        f.write("Ground Truth: X → Y\n")
    
    print(f"Results saved to {results_path}")

def main():
    # Step 1: Load data
    data = load_data(file_path)

    # Step 2: Find optimal clusters for X and Y dimensions
    k_X = find_optimal_clusters(data[['X']].values, max_clusters=4)
    k_Y = find_optimal_clusters(data[['Y']].values, max_clusters=4)

    k_final = min(k_X, k_Y)
    print(f"Optimal clusters: k_X={k_X}, k_Y={k_Y}, k_final={k_final}")

    # Step 3: Perform consensus clustering
    data['Cluster'] = perform_consensus_clustering(data, k_final)

    # Step 4: Apply LOCI on clustered data
    final_direction, cluster_directions, overall_score = loci_on_clusters(data)

    # Step 5: Save results
    save_results(overall_score, final_direction, res_folder, cluster_directions)

if __name__ == "__main__":
    main()