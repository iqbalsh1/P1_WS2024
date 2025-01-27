"""
This script applies LOCI on Unimodal data pairs (X and Y)
without splitting the data. It infers the causal direction between the variables based 
on the calculated LOCI score. The results include the inferred direction and score.

"""
import pandas as pd
import os
from causa.loci import loci

# Step 1: Define file paths and specify the dataspairs
# 0001, 0002, 0003, 0004, 0015, 018, 0020, 0021, 0048, 0049, 0050, 0051, 0056, 0057, 0058, 0059, 0060, 0062, 0063, 0064, 0072, 0073, 
# 0075, 0076, 0078, 0079, 0080, 0081, 0082, 0083, 0084, 0088, 0089, 0090, 0093

file_path = "data/datapairs/pair0001.txt"
res_folder = "results/unimodal/loci_unimodal"

# Step 2: Create results folder if it doesn't exist
os.makedirs(res_folder, exist_ok=True)

# Step 3: Load dataset 
try:
    data = pd.read_csv(file_path, sep=r'\s+', header=None, names=['X', 'Y'])
    print("Data loaded successfully!")

except Exception as e:
    print(f"Error loading or processing data: {e}")
    exit()

# Step 4: Perform LOCI causal inference on whole sets of X and Y
score = loci(data['Y'].values, data['X'].values)

# Step 5: Determine inferred causal direction
inferred_direction = "X → Y" if score > 0 else "Y → X"
print(f"LOCI score: {score}")
print(f"Inferred Causal Direction: {inferred_direction}")

# Step 6: Save results to a text file
results_path = os.path.join(res_folder, "result_loci_unimodal.txt")
with open(results_path, "a", encoding="utf-8") as f:
    f.write(f"Inferred Causal Direction using LOCI: {inferred_direction}\n")
    f.write(f"LOCI Score: {score}\n")
    f.write("Ground Truth: X → Y\n")

print(f"Results saved to {results_path}")
