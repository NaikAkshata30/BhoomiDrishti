"""
Synthetic Data Generator for Land Acquisition System

This module generates realistic synthetic test data for the land acquisition
prediction system. The data is representative but NOT real government data.

Each project is marked as SYNTHETIC/DEMO and includes:
- Varying risk profiles (HIGH, MEDIUM, LOW, NO_RISK)
- Realistic project characteristics
- Plausible relationships between factors
- Geographic distribution across Indian states
"""

def generate_synthetic_projects():
    """
    Generate synthetic project data with varying risk profiles.
    
    Returns:
        list: List of project dictionaries with all related data
    """
    
    projects = [
        # PROJECT 1: HIGH RISK - Multiple delays and issues
        {
            'project': {
                'project_id': 'DEMO_HIGHRISE_001',
                'project_name': 'Delhi-Mathura National Highway Expansion',
                'project_type': 'Highway',
                'agency': 'MoRTH',
                'state': 'Uttar Pradesh',
                'district': 'Mathura',
                'village': 'Bhuteshwar',
                'land_required_ha': 250.5,
                'affected_families': 425,
                'current_stage': 'Award',
                'status': 'Active',
            },
            'location': {
                'latitude': 27.5089,
                'longitude': 77.6121,
                'location_source': '[SYNTHETIC/DEMO] Estimated coordinates',
                'accuracy_level': 'village-level',
            },
            'acquisition': {
                'current_stage': 'Award',
                'notification_status': 'Completed',
                'survey_status': 'Completed',
                'award_status': 'Pending',
                'possession_status': 'Pending',
                'overall_progress_percentage': 28.0,
                'possession_percentage': 15.0,
                'days_in_current_stage': 385,
            },
            'compensation': {
                'total_compensation_amount': 75000000,  # 7.5 crore
                'amount_disbursed': 18750000,  # 1.875 crore (25%)
                'compensation_percentage': 25.0,
                'families_eligible': 425,
                'families_paid': 95,
                'pending_cases': 45,
                'average_payment_delay_days': 120,
            },
            'legal': {
                'active_disputes': 8,
                'dispute_count': 12,
                'court_cases': 3,
                'legal_status': 'In Court',
                'average_case_age_days': 240,
            },
            'social_impact': {
                'affected_families': 425,
                'rehabilitation_progress_percentage': 30.0,
                'resettlement_progress_percentage': 25.0,
                'relocation_completed_percentage': 12.0,
                'grievances_pending': 18,
                'stakeholder_responsiveness': 35.0,
            },
            'approvals': {
                'environmental_approval_status': 'Approved',
                'administrative_approval_status': 'Pending',
                'financial_approval_status': 'Approved',
                'other_approval_status': 'Pending',
                'pending_approvals': 2,
                'average_approval_delay_days': 95,
            },
            'prediction': {
                'delay_probability': 0.82,
                'risk_level': 'HIGH',
                'risk_color': 'RED',
                'model_version': 'v1.0',
                'prediction_confidence': 0.88,
            },
            'recommendations': [
                {
                    'factor': 'Compensation delay',
                    'priority': 'HIGH',
                    'text': 'Prioritize pending compensation verification and disbursement. Only 25% compensation completed.'
                },
                {
                    'factor': 'Active legal disputes',
                    'priority': 'HIGH',
                    'text': 'Prioritize unresolved legal cases and initiate legal review. 8 active disputes in court.'
                },
                {
                    'factor': 'Approval delay',
                    'priority': 'MEDIUM',
                    'text': 'Escalate pending administrative approvals. Average delay: 95 days.'
                },
                {
                    'factor': 'Rehabilitation & Resettlement delay',
                    'priority': 'HIGH',
                    'text': 'Prioritize rehabilitation and resettlement activities. Only 30% rehabilitation progress.'
                },
            ]
        },
        
        # PROJECT 2: MEDIUM RISK - Some delays
        {
            'project': {
                'project_id': 'DEMO_MEDIUMRISK_001',
                'project_name': 'Maharashtra Water Supply Infrastructure Project',
                'project_type': 'Water Supply',
                'agency': 'Water Resources Department',
                'state': 'Maharashtra',
                'district': 'Nashik',
                'village': 'Tryambakeshwar',
                'land_required_ha': 85.3,
                'affected_families': 156,
                'current_stage': 'Possession',
                'status': 'Active',
            },
            'location': {
                'latitude': 19.9262,
                'longitude': 73.2646,
                'location_source': '[SYNTHETIC/DEMO] Project coordinates',
                'accuracy_level': 'project-level',
            },
            'acquisition': {
                'current_stage': 'Possession',
                'notification_status': 'Completed',
                'survey_status': 'Completed',
                'award_status': 'Completed',
                'possession_status': 'In Progress',
                'overall_progress_percentage': 65.0,
                'possession_percentage': 52.0,
                'days_in_current_stage': 145,
            },
            'compensation': {
                'total_compensation_amount': 28500000,  # 2.85 crore
                'amount_disbursed': 20475000,  # 2.0475 crore (71.8%)
                'compensation_percentage': 71.8,
                'families_eligible': 156,
                'families_paid': 135,
                'pending_cases': 8,
                'average_payment_delay_days': 35,
            },
            'legal': {
                'active_disputes': 2,
                'dispute_count': 3,
                'court_cases': 1,
                'legal_status': 'Pending',
                'average_case_age_days': 110,
            },
            'social_impact': {
                'affected_families': 156,
                'rehabilitation_progress_percentage': 58.0,
                'resettlement_progress_percentage': 62.0,
                'relocation_completed_percentage': 45.0,
                'grievances_pending': 5,
                'stakeholder_responsiveness': 68.0,
            },
            'approvals': {
                'environmental_approval_status': 'Approved',
                'administrative_approval_status': 'Approved',
                'financial_approval_status': 'Approved',
                'other_approval_status': 'Approved',
                'pending_approvals': 0,
                'average_approval_delay_days': 28,
            },
            'prediction': {
                'delay_probability': 0.56,
                'risk_level': 'MEDIUM',
                'risk_color': 'ORANGE',
                'model_version': 'v1.0',
                'prediction_confidence': 0.82,
            },
            'recommendations': [
                {
                    'factor': 'Compensation delay',
                    'priority': 'MEDIUM',
                    'text': 'Accelerate compensation processing. 72% completed, focus on remaining 8 pending cases.'
                },
                {
                    'factor': 'Active legal disputes',
                    'priority': 'MEDIUM',
                    'text': 'Monitor and expedite resolution of 2 active disputes.'
                },
            ]
        },
        
        # PROJECT 3: LOW RISK - Good progress
        {
            'project': {
                'project_id': 'DEMO_LOWRISK_001',
                'project_name': 'Kerala Coastal Road Development Project',
                'project_type': 'Coastal Road',
                'agency': 'PWD Kerala',
                'state': 'Kerala',
                'district': 'Ernakulam',
                'village': 'Kumbalangi',
                'land_required_ha': 45.8,
                'affected_families': 78,
                'current_stage': 'Possession',
                'status': 'Active',
            },
            'location': {
                'latitude': 9.5088,
                'longitude': 76.3277,
                'location_source': '[SYNTHETIC/DEMO] Government project records',
                'accuracy_level': 'project-level',
            },
            'acquisition': {
                'current_stage': 'Possession',
                'notification_status': 'Completed',
                'survey_status': 'Completed',
                'award_status': 'Completed',
                'possession_status': 'Completed',
                'overall_progress_percentage': 92.0,
                'possession_percentage': 87.0,
                'days_in_current_stage': 75,
            },
            'compensation': {
                'total_compensation_amount': 16200000,  # 1.62 crore
                'amount_disbursed': 15390000,  # 1.539 crore (95%)
                'compensation_percentage': 95.0,
                'families_eligible': 78,
                'families_paid': 75,
                'pending_cases': 1,
                'average_payment_delay_days': 8,
            },
            'legal': {
                'active_disputes': 0,
                'dispute_count': 1,
                'court_cases': 0,
                'legal_status': 'Resolved',
                'average_case_age_days': 0,
            },
            'social_impact': {
                'affected_families': 78,
                'rehabilitation_progress_percentage': 88.0,
                'resettlement_progress_percentage': 92.0,
                'relocation_completed_percentage': 85.0,
                'grievances_pending': 1,
                'stakeholder_responsiveness': 89.0,
            },
            'approvals': {
                'environmental_approval_status': 'Approved',
                'administrative_approval_status': 'Approved',
                'financial_approval_status': 'Approved',
                'other_approval_status': 'Approved',
                'pending_approvals': 0,
                'average_approval_delay_days': 15,
            },
            'prediction': {
                'delay_probability': 0.25,
                'risk_level': 'LOW',
                'risk_color': 'YELLOW',
                'model_version': 'v1.0',
                'prediction_confidence': 0.91,
            },
            'recommendations': [
                {
                    'factor': 'Final compensation',
                    'priority': 'LOW',
                    'text': 'Complete final compensation payment for 1 pending case.'
                },
            ]
        },
        
        # PROJECT 4: NO RISK - Completed
        {
            'project': {
                'project_id': 'DEMO_NORISK_001',
                'project_name': 'Tamil Nadu Railway Station Development',
                'project_type': 'Railway',
                'agency': 'Indian Railways',
                'state': 'Tamil Nadu',
                'district': 'Chennai',
                'village': 'Tambaram',
                'land_required_ha': 32.5,
                'affected_families': 45,
                'current_stage': 'Possession',
                'status': 'Active',
            },
            'location': {
                'latitude': 12.9250,
                'longitude': 79.9274,
                'location_source': '[SYNTHETIC/DEMO] Railway ministry records',
                'accuracy_level': 'project-level',
            },
            'acquisition': {
                'current_stage': 'Possession',
                'notification_status': 'Completed',
                'survey_status': 'Completed',
                'award_status': 'Completed',
                'possession_status': 'Completed',
                'overall_progress_percentage': 98.0,
                'possession_percentage': 98.0,
                'days_in_current_stage': 28,
            },
            'compensation': {
                'total_compensation_amount': 12000000,  # 1.2 crore
                'amount_disbursed': 12000000,  # 1.2 crore (100%)
                'compensation_percentage': 100.0,
                'families_eligible': 45,
                'families_paid': 45,
                'pending_cases': 0,
                'average_payment_delay_days': 0,
            },
            'legal': {
                'active_disputes': 0,
                'dispute_count': 0,
                'court_cases': 0,
                'legal_status': 'Resolved',
                'average_case_age_days': 0,
            },
            'social_impact': {
                'affected_families': 45,
                'rehabilitation_progress_percentage': 100.0,
                'resettlement_progress_percentage': 100.0,
                'relocation_completed_percentage': 100.0,
                'grievances_pending': 0,
                'stakeholder_responsiveness': 95.0,
            },
            'approvals': {
                'environmental_approval_status': 'Approved',
                'administrative_approval_status': 'Approved',
                'financial_approval_status': 'Approved',
                'other_approval_status': 'Approved',
                'pending_approvals': 0,
                'average_approval_delay_days': 0,
            },
            'prediction': {
                'delay_probability': 0.08,
                'risk_level': 'NO_RISK',
                'risk_color': 'GREEN',
                'model_version': 'v1.0',
                'prediction_confidence': 0.95,
            },
            'recommendations': [
                {
                    'factor': 'Project completion',
                    'priority': 'LOW',
                    'text': 'Project is nearly complete. Monitor final handover process.'
                },
            ]
        },
        
        # PROJECT 5: HIGH RISK - Different issues
        {
            'project': {
                'project_id': 'DEMO_HIGHRISE_002',
                'project_name': 'Rajasthan Irrigation Project - Phase 2',
                'project_type': 'Irrigation',
                'agency': 'Irrigation Department Rajasthan',
                'state': 'Rajasthan',
                'district': 'Jodhpur',
                'village': 'Bilara',
                'land_required_ha': 180.2,
                'affected_families': 340,
                'current_stage': 'Survey',
                'status': 'Active',
            },
            'location': {
                'latitude': 26.1925,
                'longitude': 73.3338,
                'location_source': '[SYNTHETIC/DEMO] Irrigation ministry documents',
                'accuracy_level': 'village-level',
            },
            'acquisition': {
                'current_stage': 'Survey',
                'notification_status': 'Completed',
                'survey_status': 'In Progress',
                'award_status': 'Pending',
                'possession_status': 'Pending',
                'overall_progress_percentage': 22.0,
                'possession_percentage': 5.0,
                'days_in_current_stage': 520,
            },
            'compensation': {
                'total_compensation_amount': 68000000,  # 6.8 crore
                'amount_disbursed': 4080000,  # 0.408 crore (6%)
                'compensation_percentage': 6.0,
                'families_eligible': 340,
                'families_paid': 15,
                'pending_cases': 125,
                'average_payment_delay_days': 240,
            },
            'legal': {
                'active_disputes': 12,
                'dispute_count': 18,
                'court_cases': 5,
                'legal_status': 'In Court',
                'average_case_age_days': 310,
            },
            'social_impact': {
                'affected_families': 340,
                'rehabilitation_progress_percentage': 15.0,
                'resettlement_progress_percentage': 12.0,
                'relocation_completed_percentage': 5.0,
                'grievances_pending': 42,
                'stakeholder_responsiveness': 28.0,
            },
            'approvals': {
                'environmental_approval_status': 'Pending',
                'administrative_approval_status': 'Pending',
                'financial_approval_status': 'Approved',
                'other_approval_status': 'Pending',
                'pending_approvals': 3,
                'average_approval_delay_days': 145,
            },
            'prediction': {
                'delay_probability': 0.88,
                'risk_level': 'HIGH',
                'risk_color': 'RED',
                'model_version': 'v1.0',
                'prediction_confidence': 0.86,
            },
            'recommendations': [
                {
                    'factor': 'Survey delay',
                    'priority': 'HIGH',
                    'text': 'Accelerate survey process. Currently stalled for 520 days.'
                },
                {
                    'factor': 'Compensation crisis',
                    'priority': 'HIGH',
                    'text': 'Only 6% compensation disbursed with 125 pending cases. Urgent action required.'
                },
                {
                    'factor': 'Multiple legal disputes',
                    'priority': 'HIGH',
                    'text': '12 active disputes involving 5 court cases. Legal review recommended.'
                },
                {
                    'factor': 'Poor stakeholder engagement',
                    'priority': 'MEDIUM',
                    'text': '42 pending grievances and low stakeholder responsiveness (28%). Improve communication.'
                },
            ]
        },
        
        # PROJECT 6: MEDIUM RISK - Good location data
        {
            'project': {
                'project_id': 'DEMO_MEDIUMRISK_002',
                'project_name': 'Andhra Pradesh Metro Rail Corridor',
                'project_type': 'Metro Rail',
                'agency': 'Metro Rail Authority',
                'state': 'Andhra Pradesh',
                'district': 'Visakhapatnam',
                'village': 'Duvvada',
                'land_required_ha': 120.0,
                'affected_families': 220,
                'current_stage': 'Award',
                'status': 'Active',
            },
            'location': {
                'latitude': 17.7789,
                'longitude': 83.2997,
                'location_source': '[SYNTHETIC/DEMO] Metro Authority GIS',
                'accuracy_level': 'project-level',
            },
            'acquisition': {
                'current_stage': 'Award',
                'notification_status': 'Completed',
                'survey_status': 'Completed',
                'award_status': 'In Progress',
                'possession_status': 'Pending',
                'overall_progress_percentage': 45.0,
                'possession_percentage': 28.0,
                'days_in_current_stage': 210,
            },
            'compensation': {
                'total_compensation_amount': 45000000,  # 4.5 crore
                'amount_disbursed': 27000000,  # 2.7 crore (60%)
                'compensation_percentage': 60.0,
                'families_eligible': 220,
                'families_paid': 155,
                'pending_cases': 18,
                'average_payment_delay_days': 48,
            },
            'legal': {
                'active_disputes': 3,
                'dispute_count': 5,
                'court_cases': 1,
                'legal_status': 'Pending',
                'average_case_age_days': 95,
            },
            'social_impact': {
                'affected_families': 220,
                'rehabilitation_progress_percentage': 52.0,
                'resettlement_progress_percentage': 55.0,
                'relocation_completed_percentage': 38.0,
                'grievances_pending': 12,
                'stakeholder_responsiveness': 62.0,
            },
            'approvals': {
                'environmental_approval_status': 'Approved',
                'administrative_approval_status': 'In Progress',
                'financial_approval_status': 'Approved',
                'other_approval_status': 'Approved',
                'pending_approvals': 1,
                'average_approval_delay_days': 52,
            },
            'prediction': {
                'delay_probability': 0.52,
                'risk_level': 'MEDIUM',
                'risk_color': 'ORANGE',
                'model_version': 'v1.0',
                'prediction_confidence': 0.79,
            },
            'recommendations': [
                {
                    'factor': 'Award process delay',
                    'priority': 'MEDIUM',
                    'text': 'Expedite award process. Currently in progress for 210 days.'
                },
                {
                    'factor': 'Compensation gap',
                    'priority': 'MEDIUM',
                    'text': 'Focus on 60% compensation completion. 18 pending cases remain.'
                },
            ]
        },
    ]
    
    return projects


if __name__ == '__main__':
    import json
    projects = generate_synthetic_projects()
    print(f"Generated {len(projects)} synthetic projects")
    for proj in projects:
        print(f"  - {proj['project']['project_id']}: {proj['project']['project_name']} ({proj['prediction']['risk_level']})")
