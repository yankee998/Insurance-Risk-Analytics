# Insurance Risk Analytics 🚗💸

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python 3.11.9](https://img.shields.io/badge/Python-3.11.9-green.svg)](https://www.python.org/downloads/release/python-3119/)
[![DVC 3.51.0](https://img.shields.io/badge/DVC-3.51.0-orange.svg)](https://dvc.org/)
[![GitHub Issues](https://img.shields.io/github/issues/yankee998/Insurance-Risk-Analytics.svg)](https://github.com/yankee998/Insurance-Risk-Analytics/issues)
[![CI Pipeline](https://github.com/yankee998/Insurance-Risk-Analytics/actions/workflows/ci.yml/badge.svg)](https://github.com/yankee998/Insurance-Risk-Analytics/actions)

Welcome to the **Insurance Risk Analytics** project! 🌟 This repository powers data-driven insights for **AlphaCare Insurance Solutions**, optimizing risk assessment and pricing strategies. Built with **Python**, **DVC**, and advanced machine learning, it delivers auditable, reproducible, and scalable analytics pipelines.

---

## 📋 Table of Contents
- [🎯 Project Overview](#project-overview)
- [🚀 Getting Started](#getting-started)
  - [🛠 Prerequisites](#prerequisites)
  - [📦 Installation](#installation)
- [📊 Usage](#usage)
- [📂 Directory Structure](#directory-structure)
- [✅ Tasks Completed](#tasks-completed)
- [🤝 Contributing](#contributing)
- [📜 License](#license)
- [📬 Contact](#contact)

---

## 🎯 Project Overview
This project transforms raw insurance data into actionable insights for risk-based pricing and marketing. Key highlights include:
- **Efficient Data Handling**: Converts large datasets to Parquet for performance. 📈
- **Exploratory Data Analysis (EDA)**: Uncovers patterns in claims, premiums, and loss ratios. 🔍
- **Hypothesis Testing**: Validates risk factors across provinces, zip codes, and demographics. ⚖️
- **Predictive Modeling**: Builds models for claim severity and probability using XGBoost, Random Forest, and Linear Regression. 🤖
- **Interpretability**: Uses SHAP to explain model predictions, guiding business decisions. 📊

<details>
<summary>🔍 Click to View Key Insights</summary>

### EDA Highlights
- **Dataset**: 1,000,098 records with features like `TotalClaims`, `TotalPremium`, `Province`, and `VehicleType`.
- **Findings**:
  - **Gauteng** has the highest loss ratio (0.85). 🏙️
  - **Mercedes-Benz** and **Toyota** show wide claim variability. 🚘
  - Seasonal spikes in claims from **March–July 2015**. 📅
- **Challenges**: Missing data in `CustomValueEstimate` (78%) and memory constraints required 10% sampling.

### Hypothesis Testing Results
- **Provinces**: Higher claim severity in KwaZulu-Natal and Western Cape (p < 0.0001). 📍
- **Zip Codes**: Significant severity differences between 2000 and 4001 (p = 0.0443). 🗺️
- **Gender**: No significant claim differences (p > 0.05). 👥

### Predictive Modeling
- **Claim Severity**: XGBoost outperformed with lowest RMSE. 💰
- **Claim Probability**: XGBoost classifier achieved high F1-score. ✅
- **SHAP Insights**: `PolicyAge` increases claim severity by ~X Rand per year, informing age-based pricing. 📈

[See Final Report for Details](final_report.md)
</details>

---

## 🚀 Getting Started

### 🛠 Prerequisites
- **Python**: 3.11.9 🐍
- **Git**: For version control. 📚
- **DVC**: 3.51.0 for data versioning. 📁
- **VSCode**: With PowerShell terminal (recommended). 💻

### 📦 Installation
1. **Clone the Repository**:
   ```powershell
   git clone https://github.com/yankee998/Insurance-Risk-Analytics.git
   cd Insurance-Risk-Analytics
   ```

2. **Set Up Virtual Environment**:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install Dependencies**:
   ```powershell
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. **Initialize DVC**:
   ```powershell
   dvc init
   mkdir C:\DVC_Storage
   dvc remote add -d localstorage C:/DVC_Storage
   dvc pull
   ```

---

## 📊 Usage
- **Run EDA**:
  ```powershell
  python src/scripts/eda_analysis.py
  ```
- **Run Hypothesis Testing**:
  ```powershell
  python src/scripts/task3_hypothesis_testing.py
  ```
- **Run Predictive Modeling**:
  ```powershell
  python src/scripts/task4_data_preparation.py
  python src/scripts/task4_modeling.py
  python src/scripts/task4_evaluation.py
  ```
- **View Outputs**:
  - Visualizations: `plots/`
  - Models: `models/`
  - Reports: `src/scripts/hypothesis_testing_report.txt`, `final_report.md`

---

## 📂 Directory Structure
```
Insurance-Risk-Analytics/
├── data/                    # Raw and processed data (e.g., insurance_data.parquet)
│   └── processed/           # Train-test splits for modeling
├── src/                     # Source code
│   └── scripts/             # Scripts for EDA, hypothesis testing, and modeling
├── models/                  # Trained models and SHAP results
├── plots/                   # Visualizations (e.g., SHAP plots, claim trends)
├── tests/                   # Unit tests
├── .dvc/                    # DVC configuration
├── .github/                 # CI/CD workflows
├── venv/                    # Virtual environment (gitignored)
├── requirements.txt         # Dependencies
├── final_report.md          # Final submission report
├── README.md                # Project overview
└── LICENSE                  # MIT License
```

---

## ✅ Tasks Completed
- **Task 1: EDA & Git Setup** 🗂️
  - Converted data to Parquet, performed EDA, and visualized insights.
  - Set up GitHub repository with CI/CD.
- **Task 2: Data Version Control** 📁
  - Integrated DVC for data and output versioning.
  - Configured local storage at `C:\DVC_Storage`.
- **Task 3: A/B Hypothesis Testing** ⚖️
  - Tested hypotheses on provinces, zip codes, and gender.
  - Generated plots and report (`src/scripts/hypothesis_testing_report.txt`).
- **Task 4: Predictive Modeling** 🤖
  - Built models for claim severity (Linear Regression, Random Forest, XGBoost) and claim probability (Random Forest, XGBoost).
  - Evaluated with RMSE, R2, accuracy, precision, recall, and F1-score.
  - Used SHAP for feature importance (e.g., `PolicyAge`, `Province`).

---

## 🤝 Contributing
We welcome contributions! 🙌 Follow these steps:
1. Fork the repository. 🍴
2. Create a feature branch: `git checkout -b feature/awesome-feature`.
3. Commit changes: `git commit -m "Add awesome feature"`.
4. Push to the branch: `git push origin feature/awesome-feature`.
5. Open a Pull Request. 📬

---

## 📜 License
This project is licensed under the **MIT License**. See [LICENSE](LICENSE) for details.

---

## 📬 Contact
- **Repository**: [https://github.com/yankee998/Insurance-Risk-Analytics](https://github.com/yankee998/Insurance-Risk-Analytics)
- **Issues**: [Report bugs or suggest features](https://github.com/yankee998/Insurance-Risk-Analytics/issues)
- **Email**: [yaredgenanaw99@gmail.com](mailto:yaredgenanaw99@gmail.com)

---

**Built with 💻 and ☕ by [yankee998](https://github.com/yankee998)**