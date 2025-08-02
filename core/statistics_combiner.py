"""
Functions for combining statistics from multiple rasters
"""
from typing import List, Dict, Any
from utils.logger_config import logger

def combine_feature_statistics(ohm_feature: Dict[str, Any], 
                             slope_feature: Dict[str, Any]) -> Dict[str, Any]:
    """
    Combine statistics from OHM and slope features
    
    Args:
        ohm_feature: Feature with OHM statistics
        slope_feature: Feature with slope statistics
    
    Returns:
        Combined feature dictionary
    """
    # Start with original properties from OHM feature
    combined_props = {}
    
    # Add original properties (non-statistical)
    for key, value in ohm_feature['properties'].items():
        if not key.startswith('ohm_'):
            combined_props[key] = value
    
    # Add OHM statistics
    for key, value in ohm_feature['properties'].items():
        if key.startswith('ohm_'):
            combined_props[key] = value
    
    # Add slope statistics
    for key, value in slope_feature['properties'].items():
        if key.startswith('slope_'):
            combined_props[key] = value
    
    # Create combined feature
    combined_feature = {
        'type': 'Feature',
        'geometry': ohm_feature['geometry'],
        'properties': combined_props
    }
    
    return combined_feature

def combine_statistics_lists(ohm_stats: List[Dict[str, Any]], 
                           slope_stats: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Combine OHM and slope statistics into single features
    
    Args:
        ohm_stats: List of OHM zonal statistics
        slope_stats: List of slope zonal statistics
    
    Returns:
        List of combined feature dictionaries
    """
    if len(ohm_stats) != len(slope_stats):
        logger.error(f"Mismatch in feature counts: OHM={len(ohm_stats)}, Slope={len(slope_stats)}")
        return []
    
    combined_features = []
    
    for i, (ohm_feat, slope_feat) in enumerate(zip(ohm_stats, slope_stats)):
        try:
            combined_feature = combine_feature_statistics(ohm_feat, slope_feat)
            combined_features.append(combined_feature)
        except Exception as e:
            logger.error(f"Error combining statistics for feature {i}: {e}")
            continue
    
    logger.info(f"Successfully combined statistics for {len(combined_features)} features")
    return combined_features

def validate_statistics_data(stats_list: List[Dict[str, Any]], 
                           data_type: str) -> bool:
    """
    Validate statistics data before combining
    
    Args:
        stats_list: List of statistics dictionaries
        data_type: Type of data for logging (e.g., 'OHM', 'Slope')
    
    Returns:
        bool: True if data is valid
    """
    if not stats_list:
        logger.error(f"Empty {data_type} statistics list")
        return False
    
    # Check if all features have required structure
    for i, feature in enumerate(stats_list):
        if 'properties' not in feature:
            logger.error(f"{data_type} feature {i} missing 'properties'")
            return False
        if 'geometry' not in feature:
            logger.error(f"{data_type} feature {i} missing 'geometry'")
            return False
    
    logger.debug(f"{data_type} statistics data validated")
    return True
