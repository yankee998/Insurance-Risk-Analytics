# Insurance Risk Analytics

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)  
[![Python 3.11.9](https://img.shields.io/badge/Python-3.11.9-green.svg)](https://www.python.org/downloads/release/python-3119/)  
[![DVC](https://img.shields.io/badge/DVC-3.51.0-orange.svg)](https://dvc.org/)  
[![GitHub Issues](https://img.shields.io/github/issues/yankee998/Insurance-Risk-Analytics.svg)](https://github.com/yankee998/Insurance-Risk-Analytics/issues)  

Welcome to the **Insurance Risk Analytics** project! This repository contains code and data pipelines for analyzing insurance risk data, developed for AlphaCare Insurance Solutions. The project leverages Exploratory Data Analysis (EDA) and Data Version Control (DVC) to ensure reproducibility and compliance with regulatory standards.

## Table of Contents
- [Project Overview](#project-overview)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Usage](#usage)
- [Directory Structure](#directory-structure)
- [Tasks Completed](#tasks-completed)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Project Overview
This project aims to analyze insurance data to identify risk patterns, optimize pricing, and ensure auditable workflows. Key features include:
- Conversion of large datasets to Parquet format for efficiency.
- Comprehensive EDA with visualizations (e.g., loss ratios, claim trends).
- DVC integration for data versioning and reproducibility.

<details>
<summary>Click to View EDA Insights</summary>

### EDA Highlights
- **Data Size**: 1,000,098 records.
- **Key Findings**:
  - Gauteng province shows the highest average loss ratio (0.85).
  - Mercedes-Benz and Toyota have the widest claim ranges.
  - Seasonal premium and claim increases from March to July 2015.
- **Challenges**: Memory constraints led to 10% sampling; missing data (e.g., 78% in `CustomValueEstimate`) needs handling.

[See Interim Report for Details](interim_report.md)
</details>

## Getting Started

### Prerequisites
- **Python**: 3.11.9
- **Git**: For version control.
- **DVC**: 3.51.0 for data versioning.
- **VSCode**: With PowerShell terminal recommended.

### Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/yankee998/Insurance-Risk-Analytics.git
   cd Insurance-Risk-Analytics
   ```
2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```
3. Install dependencies:
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
4. Initialize DVC and set up remote storage:
   ```bash
   dvc init
   mkdir C:\DVC_Storage
   dvc remote add -d localstorage C:/DVC_Storage
   dvc pull
   ```

## Usage
- Run EDA scripts from `src/scripts/`:
  ```bash
  python src/scripts/eda_analysis.py
  ```
- Explore visualizations in `C:\Users\Skyline\Insurance Risk Analytics\visualization`.

## Directory Structure
```
Insurance-Risk-Analytics/
├── data/                  # Data files (e.g., insurance_data.parquet)
├── src/                   # Source code
│   └── scripts/           # Python scripts for EDA
├── visualization/         # Output plots
├── .dvc/                  # DVC configuration
├── .github/               # GitHub workflows and gitignore
├── venv/                  # Virtual environment (gitignored)
├── requirements.txt       # Python dependencies
├── interim_report.md      # Project progress report
├── README.md              # This file
└── LICENSE                # Project license
```

## Tasks Completed
- **Task 1**: EDA setup with Parquet conversion, data quality assessment, and visualizations.
- **Task 2**: DVC integration with local remote storage and data versioning.

## Contributing
1. Fork the repository.
2. Create a feature branch (`git checkout -b feature-branch`).
3. Commit changes (`git commit -m "Add feature"`).
4. Push to the branch (`git push origin feature-branch`).
5. Open a Pull Request.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact
- **Repository**: [https://github.com/yankee998/Insurance-Risk-Analytics](https://github.com/yankee998/Insurance-Risk-Analytics)
- **Issues**: Report bugs or suggestions [here](https://github.com/yankee998/Insurance-Risk-Analytics/issues) or email [yaredgenanaw99@gmail.com](mailto:yaredgenanaw99@gmail.com).
