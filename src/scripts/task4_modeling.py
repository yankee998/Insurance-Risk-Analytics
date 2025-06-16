import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from xgboost import XGBRegressor, XGBClassifier
from sklearn.metrics import mean_squared_error, r2_score, accuracy_score, precision_score, recall_score, f1_score
import pickle
import os

# Set random seed
np.random.seed(42)

# Load processed data
data_dir = 'data/processed/'
X_sev_train = pd.read_parquet(os.path.join(data_dir, 'X_sev_train.parquet'))
X_sev_test = pd.read_parquet(os.path.join(data_dir, 'X_sev_test.parquet'))
y_sev_train = pd.read_parquet(os.path.join(data_dir, 'y_sev_train.parquet'))
y_sev_test = pd.read_parquet(os.path.join(data_dir, 'y_sev_test.parquet'))
X_prob_train = pd.read_parquet(os.path.join(data_dir, 'X_prob_train.parquet'))
X_prob_test = pd.read_parquet(os.path.join(data_dir, 'X_prob_test.parquet'))
y_prob_train = pd.read_parquet(os.path.join(data_dir, 'y_prob_train.parquet'))
y_prob_test = pd.read_parquet(os.path.join(data_dir, 'y_prob_test.parquet'))

# Initialize models
severity_models = {
    'Linear Regression': LinearRegression(),
    'Random Forest': RandomForestRegressor(n_estimators=100, random_state=42),
    'XGBoost': XGBRegressor(n_estimators=100, random_state=42)
}
probability_models = {
    'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42),
    'XGBoost': XGBClassifier(n_estimators=100, random_state=42)
}

# Train and evaluate severity models
severity_results = []
for name, model in severity_models.items():
    model.fit(X_sev_train, y_sev_train)
    y_pred = model.predict(X_sev_test)
    rmse = np.sqrt(mean_squared_error(y_sev_test, y_pred))
    r2 = r2_score(y_sev_test, y_pred)
    severity_results.append({'Model': name, 'RMSE': rmse, 'R2': r2})
    pickle.dump(model, open(f'models/{name.lower().replace(" ", "_")}_severity.pkl', 'wb'))

# Train and evaluate probability models
probability_results = []
for name, model in probability_models.items():
    model.fit(X_prob_train, y_prob_train)
    y_pred = model.predict(X_prob_test)
    accuracy = accuracy_score(y_prob_test, y_pred)
    precision = precision_score(y_prob_test, y_pred)
    recall = recall_score(y_prob_test, y_pred)
    f1 = f1_score(y_prob_test, y_pred)
    probability_results.append({
        'Model': name, 'Accuracy': accuracy, 'Precision': precision,
        'Recall': recall, 'F1': f1
    })
    pickle.dump(model, open(f'models/{name.lower().replace(" ", "_")}_probability.pkl', 'wb'))

# Save results
results_df_sev = pd.DataFrame(severity_results)
results_df_prob = pd.DataFrame(probability_results)
results_df_sev.to_csv('models/severity_results.csv')
results_df_prob.to_csv('models/probability_results.csv')

print("Severity Model Results:\n", results_df_sev)
print("\nProbability Model Results:\n", results_df_prob)