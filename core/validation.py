"""
Input validation functions for zonal statistics processing
"""
import os
from pathlib import Path
from typing import List
from utils.logger_config import logger

def validate_raster_file(raster_path: str, raster_type: str) -> bool:
    """
    Validate a single raster file
    
    Args:
        raster_path: Path to raster file
        raster_type: Type description for logging (e.g., 'OHM', 'Slope')
    
    Returns:
        bool: True if valid
    """
    if not os.path.exists(raster_path):
        logger.error(f"{raster_type} raster file not found: {raster_path}")
        return False
    
    # Check file extension
    valid_extensions = ['.tif', '.tiff', '.img', '.nc']
    if not any(raster_path.lower().endswith(ext) for ext in valid_extensions):
        logger.warning(f"{raster_type} raster may not be a valid format: {raster_path}")
    
    logger.info(f"{raster_type} raster validated: {raster_path}")
    return True

def validate_input_folder(input_folder: str) -> bool:
    """
    Validate input folder exists and is accessible
    
    Args:
        input_folder: Path to input folder
    
    Returns:
        bool: True if valid
    """
    if not os.path.exists(input_folder):
        logger.error(f"Input folder not found: {input_folder}")
        return False
    
    if not os.path.isdir(input_folder):
        logger.error(f"Input path is not a directory: {input_folder}")
        return False
    
    logger.info(f"Input folder validated: {input_folder}")
    return True

def validate_output_folder(output_folder: str) -> bool:
    """
    Validate output folder can be created or accessed
    
    Args:
        output_folder: Path to output folder
    
    Returns:
        bool: True if valid
    """
    try:
        Path(output_folder).mkdir(parents=True, exist_ok=True)
        logger.info(f"Output folder validated/created: {output_folder}")
        return True
    except Exception as e:
        logger.error(f"Cannot create output folder: {e}")
        return False

def validate_all_inputs(ohm_raster: str, slope_raster: str, 
                       input_folder: str, output_folder: str) -> bool:
    """
    Validate all input parameters
    
    Args:
        ohm_raster: Path to OHM raster file
        slope_raster: Path to slope raster file
        input_folder: Path to input folder containing vector files
        output_folder: Path to output folder
    
    Returns:
        bool: True if all inputs are valid
    """
    validations = [
        validate_raster_file(ohm_raster, "OHM"),
        validate_raster_file(slope_raster, "Slope"),
        validate_input_folder(input_folder),
        validate_output_folder(output_folder)
    ]
    
    return all(validations)
