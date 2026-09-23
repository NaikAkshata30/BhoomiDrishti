"""
Risk Classification Service

Converts delay probability scores to risk levels and colors.
Thresholds are configurable for future tuning.
"""

class RiskClassifier:
    """
    Classifies risk level based on delay probability.
    
    Thresholds (configurable):
    - 0-15%: NO_RISK (GREEN)
    - 15-40%: LOW (YELLOW)
    - 40-70%: MEDIUM (ORANGE)
    - 70-100%: HIGH (RED)
    """
    
    # Risk thresholds (can be tuned based on validation results)
    THRESHOLDS = {
        'no_risk': 0.15,
        'low': 0.40,
        'medium': 0.70,
    }
    
    # Risk color mapping
    COLORS = {
        'NO_RISK': 'GREEN',
        'LOW': 'YELLOW',
        'MEDIUM': 'ORANGE',
        'HIGH': 'RED',
    }
    
    @classmethod
    def classify(cls, delay_probability):
        """
        Classify risk level based on delay probability.
        
        Args:
            delay_probability (float): Probability of delay (0.0 to 1.0)
            
        Returns:
            dict: {
                'risk_level': str,  # HIGH, MEDIUM, LOW, NO_RISK
                'risk_color': str,  # RED, ORANGE, YELLOW, GREEN
                'delay_probability': float
            }
        """
        if delay_probability is None:
            return {
                'risk_level': None,
                'risk_color': None,
                'delay_probability': None
            }
        
        # Ensure probability is between 0 and 1
        probability = max(0.0, min(1.0, float(delay_probability)))
        
        # Classify based on thresholds
        if probability <= cls.THRESHOLDS['no_risk']:
            risk_level = 'NO_RISK'
        elif probability <= cls.THRESHOLDS['low']:
            risk_level = 'LOW'
        elif probability <= cls.THRESHOLDS['medium']:
            risk_level = 'MEDIUM'
        else:
            risk_level = 'HIGH'
        
        return {
            'risk_level': risk_level,
            'risk_color': cls.COLORS.get(risk_level, 'GRAY'),
            'delay_probability': probability
        }
    
    @classmethod
    def update_thresholds(cls, no_risk=None, low=None, medium=None):
        """
        Update risk thresholds. Useful for tuning the classifier.
        
        Args:
            no_risk (float): Threshold for NO_RISK level (0-1)
            low (float): Threshold for LOW level (0-1)
            medium (float): Threshold for MEDIUM level (0-1)
        """
        if no_risk is not None:
            cls.THRESHOLDS['no_risk'] = no_risk
        if low is not None:
            cls.THRESHOLDS['low'] = low
        if medium is not None:
            cls.THRESHOLDS['medium'] = medium


def classify_risk(delay_probability):
    """
    Convenience function to classify risk.
    
    Args:
        delay_probability (float): Probability of delay (0.0 to 1.0)
        
    Returns:
        dict: Risk classification result
    """
    return RiskClassifier.classify(delay_probability)
