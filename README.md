# Practical Examination of Causal Pair Databases

This repository focuses on testing the modality of each data pair from the causal effect database and indetifying the causal pair are **unimodal or multimodal**. The dataset can be found [here](https://webdav.tuebingen.mpg.de/cause-effect/).

### Ground Truth Causal Pairs

- **Ground Truth X → Y Pairs:** pair0001 to pair0046 
- **Ground Truth Y → X Pairs:** pair0047 to pair0050 

## Project Overview

### Objectives:
1. **Modality Testing**:
   - Test the modality of the distribution for each pair in both directions (X → Y and Y → X)
   - Modality refers to the number of peaks in the probability distribution.
   - We want to identify whether the data distribution is **unimodal** or **multimodal**.

2. **Identification of New Multimodal Causal Pairs**:
   - Example: Investigate the causal relationship between weight and BMI, across different populations such as men and women.

## Project Structure

### 1. Data Preparation
- Download the dataset of causal pairs.
- Load datasets for analysis.
- Each data pair consists of two variables (X, Y)
- both directions (X → Y and Y → X) will be analyzed.

### 2. Modality Testing
- For each causal pair, analyze the distribution in both directions:
  - **X → Y**: Analyze the distribution of Y given X is unimodal or multimodal.
  - **Y → X**: Analyze the distribution of X given Y is unimodal or multimodal.
  
#### Methods for Modality Testing:

1. **Kernel Density Estimation (KDE)**:
   - Visualize the distributions of both variables using histograms
   - It can help to identify the no. of peaks in data distribution.

2. **Dip Test**:
   - A statistical test that measures the deviation from unimodality.
   - A higher dip test values suggests multimodality, and the p-value determines the importance of the result.

3. **Bidirectional Testing**:
   - Perform testing in both directions: X → Y and Y → X
     
#### General Guidelines
   - Dip Statistic < 0.02 with p-value > 0.05: Likely unimodal.
   - Dip Statistic > 0.02 with p-value < 0.05: Likely multimodal.






  
