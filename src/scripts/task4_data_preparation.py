import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
import os
import pickle

# Set random seed for reproducibility
np.random.seed(42)

# Load data
data_path = r'C:\Users\Skyline\Insurance Risk Analytics\data\insurance_data.parquet'
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Data file not found at {data_path}")
data = pd.read_parquet(data_path, engine='pyarrow')

# Handle missing data
missing_summary = data.isnull().sum()
print("Missing Values:\n", missing_summary[missing_summary > 0])

# Drop columns with >90% missing values
threshold = 0.9 * len(data)
columns_to_drop = missing_summary[missing_summary > threshold].index
data = data.drop(columns=columns_to_drop)
print(f"Dropped columns with >90% missing: {list(columns_to_drop)}")

# Handle datetime columns
datetime_cols = data.select_dtypes(include=['datetime64']).columns
for col in datetime_cols:
    if col == 'VehicleIntroDate':
        data['VehicleIntroYear'] = data[col].dt.year.fillna(0).astype(int)
        data = data.drop(columns=[col])
    else:
        data = data.drop(columns=[col])
print(f"Processed datetime columns: {list(datetime_cols)}")

# Impute numerical columns with median
numerical_cols = data.select_dtypes(include=['int64', 'float64']).columns
for col in numerical_cols:
    if data[col].notnull().sum() > 0:
        data[col] = data[col].fillna(data[col].median())
    else:
        data[col] = data[col].fillna(0)

# Impute categorical columns with mode
categorical_cols = data.select_dtypes(include=['object']).columns
for col in categorical_cols:
    if data[col].notnull().sum() > 0:
        data[col] = data[col].fillna(data[col].mode()[0])
    else:
        data[col] = data[col].fillna('Unknown')

# Feature engineering
if 'RegistrationYear' in data.columns:
    data['PolicyAge'] = 2025 - data['RegistrationYear']
else:
    print("Warning: RegistrationYear not found, skipping PolicyAge feature")

# Calculate claim occurrence
data['ClaimOccurred'] = data['TotalClaims'] > 0

# Calculate loss ratio
data['LossRatio'] = data['TotalClaims'] / data['TotalPremium'].replace(0, np.nan)
data['LossRatio'] = data['LossRatio'].fillna(0)

# Encode categorical variables
label_encoders = {}
for col in categorical_cols:
    le = LabelEncoder()
    data[col] = le.fit_transform(data[col])
    label_encoders[col] = le

# Save encoders
os.makedirs('models', exist_ok=True)
with open('models/label_encoders.pkl', 'wb') as f:
    pickle.dump(label_encoders, f)

# Define features for claim severity model
features = [col for col in data.columns if col not in ['TotalClaims', 'ClaimOccurred', 'TotalPremium', 'CalculatedPremiumPerTerm']]
severity_data = data[data['ClaimOccurred']][features + ['TotalClaims']]

# Train-test split for claim severity
X_sev = severity_data[features]
y_sev = severity_data['TotalClaims']
X_sev_train, X_sev_test, y_sev_train, y_sev_test = train_test_split(X_sev, y_sev, test_size=0.2, random_state=42)

# Save processed data
os.makedirs('data/processed', exist_ok=True)
X_sev_train.to_parquet('data/processed/X_sev_train.parquet')
X_sev_test.to_parquet('data/processed/X_sev_test.parquet')
pd.DataFrame(y_sev_train, columns=['TotalClaims']).to_parquet('data/processed/y_sev_train.parquet')
pd.DataFrame(y_sev_test, columns=['TotalClaims']).to_parquet('data/processed/y_sev_test.parquet')

# Define features for claim probability model
X_prob = data[features]
y_prob = data['ClaimOccurred']
X_prob_train, X_prob_test, y_prob_train, y_prob_test = train_test_split(X_prob, y_prob, test_size=0.2, random_state=42)

# Save processed data
X_prob_train.to_parquet('data/processed/X_prob_train.parquet')
X_prob_test.to_parquet('data/processed/X_prob_test.parquet')
pd.DataFrame(y_prob_train, columns=['ClaimOccurred']).to_parquet('data/processed/y_prob_train.parquet')
pd.DataFrame(y_prob_test, columns=['ClaimOccurred']).to_parquet('data/processed/y_prob_test.parquet')

print("Data preparation complete. Processed data saved to data/processed/")