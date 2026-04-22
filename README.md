# Practical Examination of Causal Pair Databases

This repository focuses on testing the modality of each data pair from the causal effect database and indetifying the causal pair are **unimodal or multimodal**.
- [Dataset](https://webdav.tuebingen.mpg.de/cause-effect/)  
- [Paper](https://jmlr.org/papers/v17/14-518.html)  

# Modality and Clustering Analysis 

## Overview
We aim to analyze modality and apply clustering methods to perform causal inference methods to infere causal directions using LOCI and ROCHE.

## Steps
1. **Modality Testing**:
   - Tested all pairs for modality.
   - Found cases where:
     - Both X and Y are unimodal.
     - Both X and Y are multimodal.
     - one variable is unimodal and other is multimodal.
   - Focused on **multimodal cases for X and Y** for further analysis.

2. **Clustering Methods**:
   - **GMM Clustering**.
   - **Consensus Clustering**:
     - **Approach 1**: Used silhouette score to find optimal clusters, then applied max(k_X, k_Y) for consensus clustering.
     - **Approach 2**: Let the consensus clustering algorithm determine the best `K`.

3. **Causal Inference**:
   - Applied LOCI causal inference on:
     - GMM clusters.
     - Consensus clusters (both approaches).
   - Used ROCHE to validate results.

## Results
- Detailed results for each step are provided in the `results/` folder.
