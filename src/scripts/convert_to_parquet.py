import pandas as pd
import os

# Define file paths
input_file = "C:/Users/Skyline/Insurance Risk Analytics/MachineLearningRating_v3.txt"
output_file = "data/insurance_data.parquet"

# Create data directory if it doesn't exist
os.makedirs("data", exist_ok=True)

# Read the text file in chunks due to large size
chunk_size = 10000  # Adjust based on memory capacity
chunks = []
for chunk in pd.read_csv(input_file, delimiter='|', chunksize=chunk_size, on_bad_lines='skip'):
    # Convert TransactionMonth to datetime
    chunk['TransactionMonth'] = pd.to_datetime(chunk['TransactionMonth'], errors='coerce')
    
    # Convert CapitalOutstanding to numeric, coercing errors to NaN
    chunk['CapitalOutstanding'] = pd.to_numeric(chunk['CapitalOutstanding'], errors='coerce')
    
    # Handle other potential numeric columns with mixed types (add as needed based on data)
    for col in ['SumInsured', 'CalculatedPremiumPerTerm', 'TotalPremium', 'TotalClaims']:
        chunk[col] = pd.to_numeric(chunk[col], errors='coerce')
    
    chunks.append(chunk)

# Concatenate all chunks
df = pd.concat(chunks, ignore_index=True)

# Save to Parquet format
df.to_parquet(output_file, index=False)
print(f"Data converted and saved to {output_file}")