"""
Functions for saving processing results
"""
import json
from pathlib import Path
from typing import List, Dict, Any
from utils.logger_config import logger

def create_geojson_structure(features: List[Dict[str, Any]], epsg_code: int = 32748) -> Dict[str, Any]:
    """
    Create GeoJSON structure from features with dynamic CRS
    
    Args:
        features: List of feature dictionaries
        epsg_code: EPSG code for coordinate reference system (default: 4326)
    
    Returns:
        GeoJSON dictionary with specified CRS
    """
    return {
        'type': 'FeatureCollection',
        'crs': {
            'type': 'name',
            'properties': {'name': f'urn:ogc:def:crs:EPSG::{epsg_code}'}
        },
        'features': features
    }

def generate_output_filename(original_file: Path, suffix: str = "_zonal_stats") -> str:
    """
    Generate output filename based on original file
    
    Args:
        original_file: Original vector file path
        suffix: Suffix to add to filename
    
    Returns:
        Output filename with extension
    """
    return f"{original_file.stem}{suffix}.geojson"

def save_geojson_results(features: List[Dict[str, Any]], 
                        output_file: Path,
                        epsg_code: int) -> bool:
    """
    Save features as GeoJSON file
    
    Args:
        features: List of feature dictionaries
        output_file: Output file path
    
    Returns:
        bool: Success status
    """
    try:
        # Create GeoJSON structure
        output_geojson = create_geojson_structure(features, epsg_code)
        
        # Ensure output directory exists
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        # Save to file with proper encoding
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(output_geojson, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Results saved to: {output_file}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving results to {output_file}: {e}")
        return False

def save_processing_results(features: List[Dict[str, Any]], 
                          original_file: Path, 
                          output_folder: str,
                          epsg_code: int = 32748) -> bool:
    """
    Save combined processing results to output file
    
    Args:
        features: List of feature dictionaries
        original_file: Original vector file path
        output_folder: Output folder path
    
    Returns:
        bool: Success status
    """
    if not features:
        logger.warning(f"No features to save for {original_file.name}")
        return False
    
    # Generate output file path
    output_filename = generate_output_filename(original_file)
    output_file = Path(output_folder) / output_filename
    
    # Save results
    return save_geojson_results(features, output_file, epsg_code)

def create_processing_summary(successful_count: int, total_count: int, 
                            output_folder: str) -> bool:
    """
    Create a summary file of processing results
    
    Args:
        successful_count: Number of successfully processed files
        total_count: Total number of files processed
        output_folder: Output folder path
    
    Returns:
        bool: Success status
    """
    try:
        summary = {
            'processing_summary': {
                'total_files': total_count,
                'successful_files': successful_count,
                'failed_files': total_count - successful_count,
                'success_rate': f"{(successful_count/total_count)*100:.1f}%" if total_count > 0 else "0%"
            }
        }
        
        summary_file = Path(output_folder) / "processing_summary.json"
        
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)
        
        logger.info(f"Processing summary saved to: {summary_file}")
        return True
        
    except Exception as e:
        logger.error(f"Error saving processing summary: {e}")
        return False
