"""
Recommendation Service

Generates recommendations based on detected risk factors and project status.
"""

class RecommendationGenerator:
    """
    Generates actionable recommendations based on project data and risk factors.
    """
    
    # Recommendation templates
    RECOMMENDATIONS = {
        'compensation_delay': {
            'factor': 'Compensation delay',
            'priority': 'HIGH',
            'text': 'Prioritize pending compensation verification and disbursement.'
        },
        'legal_dispute': {
            'factor': 'Active legal disputes',
            'priority': 'HIGH',
            'text': 'Prioritize unresolved legal cases and initiate legal review.'
        },
        'approval_delay': {
            'factor': 'Approval delay',
            'priority': 'MEDIUM',
            'text': 'Escalate pending administrative approvals.'
        },
        'rr_delay': {
            'factor': 'Rehabilitation & Resettlement delay',
            'priority': 'MEDIUM',
            'text': 'Prioritize rehabilitation and resettlement activities.'
        },
        'possession_delay': {
            'factor': 'Possession delay',
            'priority': 'HIGH',
            'text': 'Accelerate land possession process.'
        },
        'stakeholder_engagement': {
            'factor': 'Low stakeholder responsiveness',
            'priority': 'MEDIUM',
            'text': 'Improve stakeholder engagement and communication.'
        },
    }
    
    @classmethod
    def generate_from_project(cls, project_data):
        """
        Generate recommendations from project data.
        
        Args:
            project_data (dict or Project): Project with all related data
            
        Returns:
            list: List of recommendation dictionaries
        """
        recommendations = []
        
        # Extract data (support both dict and object notation)
        compensation = project_data.get('compensation', {}) if isinstance(project_data, dict) else project_data.compensation
        legal = project_data.get('legal', {}) if isinstance(project_data, dict) else project_data.legal
        approvals = project_data.get('approvals', {}) if isinstance(project_data, dict) else project_data.approvals
        social = project_data.get('social_impact', {}) if isinstance(project_data, dict) else project_data.social_impact
        acquisition = project_data.get('acquisition', {}) if isinstance(project_data, dict) else project_data.acquisition
        
        # Check compensation progress
        comp_pct = compensation.get('compensation_percentage', 0) if isinstance(compensation, dict) else (compensation.compensation_percentage or 0)
        if comp_pct < 60:
            recommendations.append(cls.RECOMMENDATIONS['compensation_delay'])
        
        # Check legal status
        active_disputes = legal.get('active_disputes', 0) if isinstance(legal, dict) else (legal.active_disputes or 0)
        if active_disputes > 0:
            recommendations.append(cls.RECOMMENDATIONS['legal_dispute'])
        
        # Check approvals
        pending_approvals = approvals.get('pending_approvals', 0) if isinstance(approvals, dict) else (approvals.pending_approvals or 0)
        approval_delay = approvals.get('average_approval_delay_days', 0) if isinstance(approvals, dict) else (approvals.average_approval_delay_days or 0)
        if pending_approvals > 0 or (approval_delay and approval_delay > 30):
            recommendations.append(cls.RECOMMENDATIONS['approval_delay'])
        
        # Check R&R progress
        rr_pct = social.get('rehabilitation_progress_percentage', 0) if isinstance(social, dict) else (social.rehabilitation_progress_percentage or 0)
        if rr_pct < 60:
            recommendations.append(cls.RECOMMENDATIONS['rr_delay'])
        
        # Check possession progress
        possession_pct = acquisition.get('possession_percentage', 0) if isinstance(acquisition, dict) else (acquisition.possession_percentage or 0)
        if possession_pct < 60:
            recommendations.append(cls.RECOMMENDATIONS['possession_delay'])
        
        # Check stakeholder responsiveness
        stakeholder_resp = social.get('stakeholder_responsiveness', 50) if isinstance(social, dict) else (social.stakeholder_responsiveness or 50)
        if stakeholder_resp < 50:
            recommendations.append(cls.RECOMMENDATIONS['stakeholder_engagement'])
        
        # Avoid duplicates
        seen = set()
        unique_recommendations = []
        for rec in recommendations:
            if rec['factor'] not in seen:
                unique_recommendations.append(rec)
                seen.add(rec['factor'])
        
        return unique_recommendations


def generate_recommendations(project_data):
    """
    Convenience function to generate recommendations.
    
    Args:
        project_data: Project object or dictionary
        
    Returns:
        list: List of recommendations
    """
    return RecommendationGenerator.generate_from_project(project_data)
