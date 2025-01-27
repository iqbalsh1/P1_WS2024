"""
This script applies LOCI on mix data pairs (X and Y)
without splitting the data. It infers the causal direction between the variables based 
on the calculated LOCI score. The results include the inferred direction and score.

"""
import pandas as pd
import os
from causa.loci import loci

# Step 1: Define file paths and specify the dataspairs
# 0022, 0023, 0042, 0074, 0009, 0013, 0014, 0025, 0026, 0027, 0028, 0032, 0034, 0035, 0038, 0039, 0041, 0077, 0085, 
# 0091, 0095, 0096, 0097,0098, 0100

file_path = "data/datapairs/pair0100.txt"
res_folder = "results/mixpairs/loci_mixpairs"

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
results_path = os.path.join(res_folder, "result_loci_mixpairs.txt")
with open(results_path, "a", encoding="utf-8") as f:
    f.write(f"Inferred Causal Direction using LOCI: {inferred_direction}\n")
    f.write(f"LOCI Score: {score}\n")
    f.write("Ground Truth: X → Y\n")

print(f"Results saved to {results_path}")
