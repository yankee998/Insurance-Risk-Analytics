import pytest
import pandas as pd
import numpy as np
from src.scripts.task3_hypothesis_testing import calc_claim_frequency, calc_claim_severity, calc_margin

# Mock data
data = pd.DataFrame({
    'Province': ['A', 'A', 'B', 'B'],
    'TotalClaims': [0, 1000, 2000, 0],
    'TotalPremium': [500, 600, 700, 800],
    'ClaimOccurred': [False, True, True, False],
    'Gender': ['Female', 'Male', 'Female', 'Male'],
    'PostalCode': ['1234', '1234', '5678', '5678'],
    'RegistrationYear': [2010, 2010, 2011, 2011],
    'Margin': [500, -400, -1300, 800]  # Margin = TotalPremium - TotalClaims
})

def test_calc_claim_frequency():
    freq = calc_claim_frequency(data[data['Province'] == 'A'])
    assert freq == 0.5, "Claim frequency calculation incorrect"

def test_calc_claim_severity():
    sev = calc_claim_severity(data[data['Province'] == 'A'])
    assert sev == 1000, "Claim severity calculation incorrect"

def test_calc_margin():
    margin = calc_margin(data[data['Province'] == 'B'])
    assert margin == -250, "Margin calculation incorrect"  # (-1300 + 800) / 2 = -250