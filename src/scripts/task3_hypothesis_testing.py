import pandas as pd
import numpy as np
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.stats.multicomp import pairwise_tukeyhsd
import os

# Set random seed for reproducibility
np.random.seed(42)

# Load Parquet data
data_path = r'C:\Users\Skyline\Insurance Risk Analytics\data\insurance_data.parquet'
if not os.path.exists(data_path):
    raise FileNotFoundError(f"Data file not found at {data_path}")
data = pd.read_parquet(data_path, engine='pyarrow')

# Data quality check
required_cols = ['Province', 'PostalCode', 'Gender', 'TotalClaims', 'TotalPremium']
missing_cols = [col for col in required_cols if col not in data.columns]
if missing_cols:
    raise ValueError(f"Missing required columns: {missing_cols}")

# Define metrics
data['ClaimOccurred'] = data['TotalClaims'] > 0
data['Margin'] = data['TotalPremium'] - data['TotalClaims']

# Function to calculate Claim Frequency
def calc_claim_frequency(group):
    return group['ClaimOccurred'].mean()

# Function to calculate Claim Severity
def calc_claim_severity(group):
    claims = group[group['ClaimOccurred']]['TotalClaims']
    return claims.mean() if len(claims) > 0 else 0

# Function to calculate Margin
def calc_margin(group):
    return group['Margin'].mean()

# Function to perform chi-squared test for Claim Frequency
def chi_squared_test(data, group_col, group1, group2):
    subset = data[data[group_col].isin([group1, group2])]
    contingency = pd.crosstab(subset[group_col], subset['ClaimOccurred'])
    if contingency.shape[0] < 2 or contingency.shape[1] < 2 or contingency.min().min() < 5:
        print(f"Warning: Invalid contingency table for {group_col} (shape: {contingency.shape}, min cell: {contingency.min().min()})")
        return np.nan, np.nan
    chi2, p, _, _ = stats.chi2_contingency(contingency)
    return chi2, p

# Function to perform t-test for Claim Severity or Margin
def t_test(data, group_col, group1, group2, metric):
    group1_data = data[data[group_col] == group1][metric].dropna()
    group2_data = data[data[group_col] == group2][metric].dropna()
    if len(group1_data) < 2 or len(group2_data) < 2:
        print(f"Warning: Insufficient data for t-test on {metric} in {group_col} (sizes: {len(group1_data)}, {len(group2_data)})")
        return np.nan, np.nan
    t_stat, p = stats.ttest_ind(group1_data, group2_data, equal_var=False)  # Welch's t-test
    return t_stat, p

# Function to perform ANOVA for multiple groups
def anova_test(data, group_col, metric):
    groups = [group[metric].dropna() for _, group in data.groupby(group_col) if len(group[metric].dropna()) > 0]
    if len(groups) < 2:
        print(f"Warning: Fewer than 2 groups with valid data for {metric} in {group_col}")
        return np.nan, np.nan
    f_stat, p = stats.f_oneway(*groups)
    return f_stat, p

# Function to check group equivalence
def check_group_equivalence(data, group_col, group1, group2, check_cols=['RegistrationYear']):
    print(f"Checking equivalence for {group_col} between {group1} and {group2}")
    subset = data[data[group_col].isin([group1, group2])]
    for col in check_cols:
        if col not in data.columns:
            print(f"Warning: {col} not in dataset, skipping equivalence check")
            continue
        if data[col].dtype == 'object':
            chi2, p = chi_squared_test(subset, col, group1, group2)
            print(f"Equivalence check for {col}: Chi-squared = {chi2:.2f}, p-value = {p:.4f}")
        else:
            t_stat, p = t_test(subset, group_col, group1, group2, col)
            print(f"Equivalence check for {col}: t-stat = {t_stat:.2f}, p-value = {p:.4f}")
        if p < 0.05 and not np.isnan(p):
            print(f"Warning: Groups differ significantly on {col}")

# Function to select equivalent zip codes
def select_equivalent_zips(data, col='PostalCode', metric='RegistrationYear', p_threshold=0.05):
    zip_counts = data[col].value_counts()
    valid_zips = zip_counts[zip_counts >= 30].index  # Ensure sufficient sample size
    selected_zips = []
    for i, zip1 in enumerate(valid_zips):
        for zip2 in valid_zips[i+1:]:
            subset = data[data[col].isin([zip1, zip2])]
            if metric not in data.columns:
                continue
            t_stat, p = t_test(subset, col, zip1, zip2, metric)
            if p >= p_threshold and not np.isnan(p):
                selected_zips = [zip1, zip2]
                break
        if selected_zips:
            break
    return selected_zips

# Create output directory for plots
os.makedirs('plots', exist_ok=True)

# Initialize report
report_lines = ["Hypothesis Testing Results\n", "="*50 + "\n"]

# Hypothesis 1: No risk differences across provinces
print("Hypothesis 1: No risk differences across provinces")
report_lines.append("Hypothesis 1: No risk differences across provinces\n")
provinces = data['Province'].dropna().unique()
if len(provinces) > 1:
    contingency_prov = pd.crosstab(data['Province'], data['ClaimOccurred'])
    if contingency_prov.shape[0] < 2 or contingency_prov.shape[1] < 2 or contingency_prov.min().min() < 5:
        print(f"Warning: Invalid contingency table for Province (shape: {contingency_prov.shape}, min cell: {contingency_prov.min().min()})")
        chi2_prov, p_prov_freq = np.nan, np.nan
    else:
        chi2_prov, p_prov_freq, _, _ = stats.chi2_contingency(contingency_prov)
    print(f"Claim Frequency - Chi-squared: {chi2_prov:.2f}, p-value: {p_prov_freq:.4f}")
    report_lines.append(f"Claim Frequency - Chi-squared: {chi2_prov:.2f}, p-value: {p_prov_freq:.4f}\n")

    claims_data = data[data['ClaimOccurred']]
    f_stat_prov, p_prov_sev = anova_test(claims_data, 'Province', 'TotalClaims')
    print(f"Claim Severity - ANOVA F-stat: {f_stat_prov:.2f}, p-value: {p_prov_sev:.4f}")
    report_lines.append(f"Claim Severity - ANOVA F-stat: {f_stat_prov:.2f}, p-value: {p_prov_sev:.4f}\n")

    if (p_prov_freq < 0.05 or p_prov_sev < 0.05) and not np.isnan(p_prov_freq) and not np.isnan(p_prov_sev):
        print("Reject H0: Significant risk differences across provinces.")
        report_lines.append("Reject H0: Significant risk differences across provinces.\n")
        if not np.isnan(f_stat_prov):
            tukey = pairwise_tukeyhsd(claims_data['TotalClaims'].dropna(), claims_data['Province'].dropna())
            print(tukey)
            report_lines.append(str(tukey) + "\n")
        print("Business Recommendation: Increase premiums by 10-15% in high-risk provinces (e.g., KwaZulu-Natal, Western Cape) to cover higher claim severity. Offer 5-10% discounts in low-risk provinces (e.g., Mpumalanga, North West) to attract clients.")
        report_lines.append("Business Recommendation: Increase premiums by 10-15% in high-risk provinces (e.g., KwaZulu-Natal, Western Cape) to cover higher claim severity. Offer 5-10% discounts in low-risk provinces (e.g., Mpumalanga, North West) to attract clients.\n")
    else:
        print("Fail to reject H0: No significant risk differences across provinces.")
        report_lines.append("Fail to reject H0: No significant risk differences across provinces.\n")
else:
    print("Insufficient unique provinces for testing.")
    report_lines.append("Insufficient unique provinces for testing.\n")

# Hypothesis 2: No risk differences between zip codes
print("\nHypothesis 2: No risk differences between zip codes")
report_lines.append("\nHypothesis 2: No risk differences between zip codes\n")
top_zips = select_equivalent_zips(data, 'PostalCode', 'RegistrationYear')
if len(top_zips) == 2:
    subset_zip = data[data['PostalCode'].isin(top_zips)]
    check_group_equivalence(subset_zip, 'PostalCode', top_zips[0], top_zips[1])
    chi2_zip, p_zip_freq = chi_squared_test(subset_zip, 'PostalCode', top_zips[0], top_zips[1])
    print(f"Claim Frequency - Chi-squared: {chi2_zip:.2f}, p-value: {p_zip_freq:.4f}")
    report_lines.append(f"Claim Frequency - Chi-squared: {chi2_zip:.2f}, p-value: {p_zip_freq:.4f}\n")

    claims_zip = subset_zip[subset_zip['ClaimOccurred']]
    t_stat_zip, p_zip_sev = t_test(claims_zip, 'PostalCode', top_zips[0], top_zips[1], 'TotalClaims')
    print(f"Claim Severity - t-stat: {t_stat_zip:.2f}, p-value: {p_zip_sev:.4f}")
    report_lines.append(f"Claim Severity - t-stat: {t_stat_zip:.2f}, p-value: {p_zip_sev:.4f}\n")

    if (p_zip_freq < 0.05 or p_zip_sev < 0.05) and not np.isnan(p_zip_freq) and not np.isnan(p_zip_sev):
        print(f"Reject H0: Significant risk differences between zip codes {top_zips[0]} and {top_zips[1]}.")
        report_lines.append(f"Reject H0: Significant risk differences between zip codes {top_zips[0]} and {top_zips[1]}.\n")
        print("Business Recommendation: Offer lower premiums (5-10% discount) in the low-risk zip code to attract new policyholders. Increase premiums by 5% in the high-risk zip code to mitigate losses.")
        report_lines.append("Business Recommendation: Offer lower premiums (5-10% discount) in the low-risk zip code to attract new policyholders. Increase premiums by 5% in the high-risk zip code to mitigate losses.\n")
    else:
        print("Fail to reject H0: No significant risk differences between zip codes.")
        report_lines.append("Fail to reject H0: No significant risk differences between zip codes.\n")
else:
    print("Insufficient equivalent zip codes for testing.")
    report_lines.append("Insufficient equivalent zip codes for testing.\n")

# Hypothesis 3: No significant margin difference between zip codes
print("\nHypothesis 3: No significant margin difference between zip codes")
report_lines.append("\nHypothesis 3: No significant margin difference between zip codes\n")
if len(top_zips) == 2:
    t_stat_margin, p_margin = t_test(subset_zip, 'PostalCode', top_zips[0], top_zips[1], 'Margin')
    print(f"Margin - t-stat: {t_stat_margin:.2f}, p-value: {p_margin:.4f}")
    report_lines.append(f"Margin - t-stat: {t_stat_margin:.2f}, p-value: {p_margin:.4f}\n")
    if p_margin < 0.05 and not np.isnan(p_margin):
        print(f"Reject H0: Significant margin differences between zip codes {top_zips[0]} and {top_zips[1]}.")
        report_lines.append(f"Reject H0: Significant margin differences between zip codes {top_zips[0]} and {top_zips[1]}.\n")
        print("Business Recommendation: Prioritize marketing in the high-margin zip code to maximize profitability.")
        report_lines.append("Business Recommendation: Prioritize marketing in the high-margin zip code to maximize profitability.\n")
    else:
        print("Fail to reject H0: No significant margin differences between zip codes.")
        report_lines.append("Fail to reject H0: No significant margin differences between zip codes.\n")
        print("Business Recommendation: Maintain consistent pricing across these zip codes until further data analysis.")
        report_lines.append("Business Recommendation: Maintain consistent pricing across these zip codes until further data analysis.\n")
else:
    print("Insufficient equivalent zip codes for testing.")
    report_lines.append("Insufficient equivalent zip codes for testing.\n")

# Hypothesis 4: No risk difference between Women and Men
print("\nHypothesis 4: No risk difference between Women and Men")
report_lines.append("\nHypothesis 4: No risk difference between Women and Men\n")
genders = data['Gender'].dropna().unique()
if 'Female' in genders and 'Male' in genders:
    check_group_equivalence(data, 'Gender', 'Female', 'Male')
    chi2_gender, p_gender_freq = chi_squared_test(data, 'Gender', 'Female', 'Male')
    print(f"Claim Frequency - Chi-squared: {chi2_gender:.2f}, p-value: {p_gender_freq:.4f}")
    report_lines.append(f"Claim Frequency - Chi-squared: {chi2_gender:.2f}, p-value: {p_gender_freq:.4f}\n")

    claims_gender = data[data['ClaimOccurred']]
    t_stat_gender, p_gender_sev = t_test(claims_gender, 'Gender', 'Female', 'Male', 'TotalClaims')
    print(f"Claim Severity - t-stat: {t_stat_gender:.2f}, p-value: {p_gender_sev:.4f}")
    report_lines.append(f"Claim Severity - t-stat: {t_stat_gender:.2f}, p-value: {p_gender_sev:.4f}\n")

    if (p_gender_freq < 0.05 or p_gender_sev < 0.05) and not np.isnan(p_gender_freq) and not np.isnan(p_gender_sev):
        print("Reject H0: Significant risk differences between Women and Men.")
        report_lines.append("Reject H0: Significant risk differences between Women and Men.\n")
        print("Business Recommendation: Develop gender-specific premium adjustments based on risk profiles.")
        report_lines.append("Business Recommendation: Develop gender-specific premium adjustments based on risk profiles.\n")
    else:
        print("Fail to reject H0: No significant risk differences between Women and Men.")
        report_lines.append("Fail to reject H0: No significant risk differences between Women and Men.\n")
        print("Business Recommendation: Avoid gender-specific pricing due to lack of significant risk differences and equivalence issues in RegistrationYear. Clean data before further analysis.")
        report_lines.append("Business Recommendation: Avoid gender-specific pricing due to lack of significant risk differences and equivalence issues in RegistrationYear. Clean data before further analysis.\n")
else:
    print("Insufficient gender categories for testing.")
    report_lines.append("Insufficient gender categories for testing.\n")

# Visualizations
plt.figure(figsize=(10, 6))
sns.barplot(x='Province', y='ClaimOccurred', data=data, errorbar=None)
plt.title('Claim Frequency by Province')
plt.ylabel('Claim Frequency (Proportion)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('plots/claim_frequency_province.png')
plt.close()

plt.figure(figsize=(10, 6))
sns.boxplot(x='Province', y='TotalClaims', data=claims_data)
plt.title('Claim Severity by Province')
plt.ylabel('Total Claims (Rand)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('plots/claim_severity_province.png')
plt.close()

if len(top_zips) == 2:
    plt.figure(figsize=(10, 6))
    sns.boxplot(x='PostalCode', y='Margin', data=subset_zip)
    plt.title(f'Margin by Zip Code ({top_zips[0]} vs {top_zips[1]})')
    plt.ylabel('Margin (Rand)')
    plt.tight_layout()
    plt.savefig('plots/margin_zipcode.png')
    plt.close()

# Save report
with open('src/scripts/hypothesis_testing_report.txt', 'w') as f:
    f.writelines(report_lines)

print("Analysis complete. Results saved to src/scripts/hypothesis_testing_report.txt and plots saved to plots/ directory.")