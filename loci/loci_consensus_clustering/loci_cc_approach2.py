import sys
sys.path.append(r'C:\Users\User\Desktop\P1_WS2024\P1_WS2024_1.2\loci\causa\experiment\Consensus_Clustering')
import pandas as pd
import numpy as np
import os
from sklearn.cluster import KMeans
from causa.loci import loci
from consensusClustering import ConsensusCluster

file_path = "data/datapairs/pair0005.txt"
res_folder = "results/results_loci_cc"

# Create results folder if it doesn't exist
def create_results_folder(folder_path):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

# Load the dataset
def load_data(file_path):
    try:
        data = pd.read_csv(file_path, sep=r'\s+', header=None, names=['X', 'Y'])
        print("Data loaded successfully!")
        return data
    except Exception as e:
        print(f"Error loading data: {e}")
        exit()

# Perform consensus clustering and find the best number of clusters
def perform_consensus_clustering(data, L=2, K=5, H=30, resample_proportion=0.5):
    consensus_clustering = ConsensusCluster(
        cluster=lambda n_clusters: KMeans(n_clusters=n_clusters, random_state=42),
        L=L,  # Start with a smaller number of clusters
        K=K,  # Try up to K clusters
        H=H,  # Number of resamplings
        resample_proportion=resample_proportion  # Proportion of data to sample
    )

    # Fit consensus clustering on the dataset
    consensus_clustering.fit(data.values, verbose=True)

    # Get the best number of clusters
    best_k = consensus_clustering.bestK
    print(f"Best number of clusters determined by consensus clustering: {best_k}")

    # Get final cluster labels
    final_labels = consensus_clustering.predict_data(data.values)
    return best_k, final_labels

# Apply LOCI for causal inference on clustered data
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

# Save the results
def save_results(score, inferred_direction, res_folder, cluster_directions):
    create_results_folder(res_folder)
    results_path = os.path.join(res_folder, "loci_cc2.txt")

    with open(results_path, "a", encoding="utf-8") as f:
        f.write(f"LOCI: {inferred_direction}\n")
        f.write(f"LOCI Score: {score}\n")
        f.write(f"Cluster Directions: {', '.join(cluster_directions)}\n")
        f.write("Ground Truth: X → Y\n")

    print(f"Results saved to {results_path}")


def main():
    # Step 1: Load data
    data = load_data(file_path)

    # Step 2: Perform consensus clustering to determine best k and cluster data
    best_k, final_labels = perform_consensus_clustering(data)

    # Step 3: Add the cluster labels to the dataset
    data['Cluster'] = final_labels

    # Step 4: Apply LOCI on the clustered data
    final_direction, cluster_directions, overall_score = loci_on_clusters(data)

    # Step 5: Save the results
    save_results(overall_score, final_direction, res_folder, cluster_directions)

if __name__ == "__main__":
    main()
