# Insurance Risk Analytics
  
Welcome to the Insurance Risk Analytics project! This repository contains code and data pipelines for analyzing insurance risk data, developed for AlphaCare Insurance Solutions. The project leverages Exploratory Data Analysis (EDA) and Data Version Control (DVC) to ensure reproducibility and compliance with regulatory standards.

## Table of Contents

Project Overview
Getting Started
Prerequisites
Installation


## Usage
Directory Structure
Tasks Completed
Contributing
License
Contact

## Project Overview
This project aims to analyze insurance data to identify risk patterns, optimize pricing, and ensure auditable workflows. Key features include:

Conversion of large datasets to Parquet format for efficiency.
Comprehensive EDA with visualizations (e.g., loss ratios, claim trends).
DVC integration for data versioning and reproducibility.


## Getting Started

Prerequisites

Python: 3.11.9
Git: For version control.
DVC: 3.51.0 for data versioning.
VSCode: With PowerShell terminal recommended.

Installation

Clone the repository:git clone https://github.com/yankee998/Insurance-Risk-Analytics.git
cd Insurance-Risk-Analytics


Create and activate a virtual environment:

python -m venv venv
.\venv\Scripts\Activate.ps1


Install dependencies:

pip install --upgrade pip
pip install -r requirements.txt


Initialize DVC and set up remote storage:

dvc init
mkdir C:\DVC_Storage
dvc remote add -d localstorage C:/DVC_Storage
dvc pull


Usage

Run EDA scripts from src/scripts/:python src/scripts/eda_analysis.py


Explore visualizations in C:\Users\Skyline\Insurance Risk Analytics\visualization.

Directory Structure
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


# Contributing

Fork the repository.
Create a feature branch (git checkout -b feature-branch).
Commit changes (git commit -m "Add feature").
Push to the branch (git push origin feature-branch).
Open a Pull Request.

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Contact

Repository: https://github.com/yankee998/Insurance-Risk-Analytics
Issues: Report bugs or suggestions here.(yaredgenanaw99@gmail.com)

