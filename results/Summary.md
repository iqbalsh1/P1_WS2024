## Results Summary

### Case: Both X and Y multimodal

- **Total Pairs:** 27
- **LOCI on whole sets of X and Y:** 10/27 = 37.03%
- **LOCI on GMM Clusters:** 14/27 = 52.85%
- **LOCI on Consensus Clusters Approach 1:** 9/27 = 33.33%
- **LOCI on Consensus Clusters Approach 2:** 

- **ROCHE on whole sets of X and Y:** 20/27 = 74.07%
- **ROCHE on Consensus Clusters:** Pending




### GMM Clustering 

- **Initialize GMM:**:  with `n_components=2` (two clusters) 
- **Fit and Predict:**: GMM applied to the `Y` column (`data[['Y']]`) using `fit_predict()`
- **Store Results:**: Cluster labels (0 or 1) saved in the `Cluster` column of the dataset.

### Consensus Clustering 

### Approach 1: 
- **Cluster Determination:** Optimal clusters identified using silhouette scores.
- **Consensus Clustering:** Utilizes `max(K_X, K_Y)` from silhouette scores for X and Y dimensions.

### Approach 2: 
- **Consensus Clustering Implementation:** 
  - Uses KMeans with resampling to find the best number of clusters.
  - Key focus:
    - Resample data proportionally (`resample_proportion`).
    - Identify clusters via repeated trials (`H` resamplings).
  - **Outputs:**
    - Optimal number of clusters (`best_k`).
    - Cluster labels for the dataset.
