import pandas as pd
import numpy as np
import shap
import matplotlib.pyplot as plt
import pickle
import os

# Load data
data_dir = 'data/processed/'
X_sev_test = pd.read_parquet(os.path.join(data_dir, 'X_sev_test.parquet'))
X_prob_test = pd.read_parquet(os.path.join(data_dir, 'X_prob_test.parquet'))

# Load best models
xgb_sev = pickle.load(open('models/xgboost_severity.pkl', 'rb'))
xgb_prob = pickle.load(open('models/xgboost_probability.pkl', 'rb'))

# SHAP for severity model
explainer_sev = shap.TreeExplainer(xgb_sev)
shap_values_sev = explainer_sev.shap_values(X_sev_test)
shap.summary_plot(shap_values_sev, X_sev_test, show=False)
plt.savefig('plots/shap_summary_severity.png')
plt.close()

# SHAP for probability model
explainer_prob = shap.TreeExplainer(xgb_prob)
shap_values_prob = explainer_prob.shap_values(X_prob_test)
shap.summary_plot(shap_values_prob, X_prob_test, show=False)
plt.savefig('plots/shap_summary_probability.png')
plt.close()

# Top features
shap_sev_df = pd.DataFrame({'Feature': X_sev_test.columns, 'Mean_SHAP': np.abs(shap_values_sev).mean(axis=0)})
shap_prob_df = pd.DataFrame({'Feature': X_prob_test.columns, 'Mean_SHAP': np.abs(shap_values_prob).mean(axis=0)})
top_sev_features = shap_sev_df.sort_values('Mean_SHAP', ascending=False).head(10)
top_prob_features = shap_prob_df.sort_values('Mean_SHAP', ascending=False).head(10)

# Save SHAP results
top_sev_features.to_csv('models/shap_severity_features.csv')
top_prob_features.to_csv('models/shap_probability_features.csv')

print("Top 10 Features for Severity Model:\n", top_sev_features)
print("\nTop 10 Features for Probability Model:\n", top_prob_features)