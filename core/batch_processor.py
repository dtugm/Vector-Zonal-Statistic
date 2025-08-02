"""
Main batch processing functions
"""
from pathlib import Path
from typing import Tuple
from utils.logger_config import logger

# Import all processing functions
from .file_finder import find_vector_files, filter_files_by_size
from .crs_handler import check_crs_compatibility
from .zonal_calculator import calculate_ohm_statistics, calculate_slope_statistics
from .statistics_combiner import combine_statistics_lists, validate_statistics_data
from .result_saver import save_processing_results, create_processing_summary

def process_single_file(vector_file: Path, ohm_raster: str, slope_raster: str, 
                       output_folder: str) -> bool:
    """
    Process a single vector file for zonal statistics
    
    Args:
        vector_file: Path to vector file
        ohm_raster: Path to OHM raster
        slope_raster: Path to slope raster
        output_folder: Path to output folder
    
    Returns:
        bool: Success status
    """
    try:
        logger.info(f"Processing: {vector_file.name}")
        
        # Check CRS compatibility and load data
        gdf = check_crs_compatibility(vector_file, ohm_raster)
        
        if gdf.empty:
            logger.warning(f"Empty or invalid vector file: {vector_file.name}")
            return False
        
        # Calculate zonal statistics for OHM
        ohm_stats = calculate_ohm_statistics(gdf, ohm_raster)
        if not validate_statistics_data(ohm_stats, "OHM"):
            return False
        
        # Calculate zonal statistics for Slope
        slope_stats = calculate_slope_statistics(gdf, slope_raster)
        if not validate_statistics_data(slope_stats, "Slope"):
            return False
        
        # Combine results
        combined_features = combine_statistics_lists(ohm_stats, slope_stats)
        if not combined_features:
            logger.error(f"Failed to combine statistics for {vector_file.name}")
            return False
        
        # Save results
        success = save_processing_results(combined_features, vector_file, output_folder)
        
        if success:
            logger.info(f"Successfully processed: {vector_file.name}")
        
        return success
        
    except Exception as e:
        logger.error(f"Error processing {vector_file.name}: {e}")
        return False

def run_batch_processing(ohm_raster: str, slope_raster: str, input_folder: str, 
                        output_folder: str) -> Tuple[int, int]:
    """
    Process all vector files in batch
    
    Args:
        ohm_raster: Path to OHM raster file
        slope_raster: Path to slope raster file
        input_folder: Path to input folder
        output_folder: Path to output folder
    
    Returns:
        Tuple of (successful_count, total_count)
    """
    logger.info("Starting batch processing")
    
    # Find all vector files
    vector_files = find_vector_files(input_folder)
    
    if not vector_files:
        logger.warning("No vector files found in input folder")
        return 0, 0
    
    # Filter files by size
    vector_files = filter_files_by_size(vector_files)
    
    # Process each file
    successful_count = 0
    total_count = len(vector_files)
    
    for i, vector_file in enumerate(vector_files, 1):
        logger.info(f"Processing file {i}/{total_count}: {vector_file.name}")
        
        success = process_single_file(vector_file, ohm_raster, slope_raster, output_folder)
        if success:
            successful_count += 1
    
    # Create processing summary
    create_processing_summary(successful_count, total_count, output_folder)
    
    logger.info(f"Batch processing completed: {successful_count}/{total_count} files processed successfully")
    return successful_count, total_count
