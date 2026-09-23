"""
Synthetic Data Overview

This document describes the synthetic test data generated for the
Land Acquisition Predictive Analytics System.

IMPORTANT: This is DEMO/SYNTHETIC data for development and testing.
It is NOT real government data.
"""

# SYNTHETIC PROJECTS OVERVIEW

PROJECTS = {
    "DEMO_HIGHRISE_001": {
        "name": "Delhi-Mathura National Highway Expansion",
        "type": "Highway",
        "state": "Uttar Pradesh",
        "district": "Mathura",
        "risk_profile": "HIGH (0.82)",
        "reasons": [
            "Very low compensation (25%)",
            "Multiple legal disputes (8 active)",
            "Delays in possession (15%)",
            "Low R&R progress (30%)",
            "Long days in award stage (385 days)",
        ],
        "affected_families": 425,
        "land_required_ha": 250.5,
    },
    
    "DEMO_MEDIUMRISK_001": {
        "name": "Maharashtra Water Supply Infrastructure Project",
        "type": "Water Supply",
        "state": "Maharashtra",
        "district": "Nashik",
        "risk_profile": "MEDIUM (0.56)",
        "reasons": [
            "Decent compensation progress (72%)",
            "Some legal disputes (2 active)",
            "Good R&R progress (58-62%)",
            "Moderate delays (35 days average)",
        ],
        "affected_families": 156,
        "land_required_ha": 85.3,
    },
    
    "DEMO_LOWRISK_001": {
        "name": "Kerala Coastal Road Development Project",
        "type": "Coastal Road",
        "state": "Kerala",
        "district": "Ernakulam",
        "risk_profile": "LOW (0.25)",
        "reasons": [
            "High compensation (95%)",
            "No active legal disputes",
            "Good R&R progress (88-92%)",
            "Minimal delays (8 days average)",
            "High stakeholder responsiveness (89%)",
        ],
        "affected_families": 78,
        "land_required_ha": 45.8,
    },
    
    "DEMO_NORISK_001": {
        "name": "Tamil Nadu Railway Station Development",
        "type": "Railway",
        "state": "Tamil Nadu",
        "district": "Chennai",
        "risk_profile": "NO_RISK (0.08)",
        "reasons": [
            "100% compensation completed",
            "No legal disputes",
            "100% R&R complete",
            "Nearly complete project (98%)",
            "All approvals obtained",
        ],
        "affected_families": 45,
        "land_required_ha": 32.5,
    },
    
    "DEMO_HIGHRISE_002": {
        "name": "Rajasthan Irrigation Project - Phase 2",
        "type": "Irrigation",
        "state": "Rajasthan",
        "district": "Jodhpur",
        "risk_profile": "HIGH (0.88)",
        "reasons": [
            "Critical compensation delay (6%)",
            "Multiple legal disputes (12 active, 5 court cases)",
            "Very poor R&R progress (12-15%)",
            "Stalled in survey stage (520 days)",
            "Many pending grievances (42)",
        ],
        "affected_families": 340,
        "land_required_ha": 180.2,
    },
    
    "DEMO_MEDIUMRISK_002": {
        "name": "Andhra Pradesh Metro Rail Corridor",
        "type": "Metro Rail",
        "state": "Andhra Pradesh",
        "district": "Visakhapatnam",
        "risk_profile": "MEDIUM (0.52)",
        "reasons": [
            "Moderate compensation (60%)",
            "Some legal disputes (3 active)",
            "Moderate R&R progress (52-55%)",
            "Award stage delay (210 days)",
            "Pending approvals (1)",
        ],
        "affected_families": 220,
        "land_required_ha": 120.0,
    },
}

# RISK DISTRIBUTION
RISK_DISTRIBUTION = {
    "HIGH": 2,      # DEMO_HIGHRISE_001, DEMO_HIGHRISE_002
    "MEDIUM": 2,    # DEMO_MEDIUMRISK_001, DEMO_MEDIUMRISK_002
    "LOW": 1,       # DEMO_LOWRISK_001
    "NO_RISK": 1,   # DEMO_NORISK_001
    "TOTAL": 6,
}

# GEOGRAPHIC DISTRIBUTION
STATES = {
    "Uttar Pradesh": 1,
    "Maharashtra": 1,
    "Kerala": 1,
    "Tamil Nadu": 1,
    "Rajasthan": 1,
    "Andhra Pradesh": 1,
}

# KEY METRICS
STATISTICS = {
    "total_projects": 6,
    "total_affected_families": sum([p["affected_families"] for p in PROJECTS.values()]),
    "total_land_ha": sum([p["land_required_ha"] for p in PROJECTS.values()]),
    "avg_compensation_percentage": 46.3,  # Average across all projects
    "avg_legal_disputes": 4.2,
    "avg_days_in_stage": 223.5,
}

# FEATURE RANGES (for ML model understanding)
FEATURE_RANGES = {
    "land_required_ha": {
        "min": 32.5,
        "max": 250.5,
        "avg": STATISTICS["total_land_ha"] / 6,
    },
    "affected_families": {
        "min": 45,
        "max": 425,
        "avg": STATISTICS["total_affected_families"] / 6,
    },
    "compensation_percentage": {
        "min": 6.0,
        "max": 100.0,
        "avg": 46.3,
    },
    "active_disputes": {
        "min": 0,
        "max": 12,
        "avg": 4.2,
    },
    "delay_probability": {
        "min": 0.08,
        "max": 0.88,
        "avg": 0.52,
    },
    "overall_progress_percentage": {
        "min": 22.0,
        "max": 98.0,
        "avg": 58.3,
    },
}

if __name__ == '__main__':
    print("Synthetic Data Overview")
    print("=" * 70)
    print(f"\nTotal Projects: {RISK_DISTRIBUTION['TOTAL']}")
    print(f"Total Affected Families: {STATISTICS['total_affected_families']}")
    print(f"Total Land Area: {STATISTICS['total_land_ha']:.1f} hectares")
    print(f"\nRisk Distribution:")
    for risk, count in RISK_DISTRIBUTION.items():
        if risk != "TOTAL":
            print(f"  {risk}: {count} projects")
