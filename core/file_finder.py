"""
Vector file discovery and filtering functions
"""
from pathlib import Path
from typing import List
from utils.logger_config import logger

def get_supported_extensions() -> List[str]:
    """
    Get list of supported vector file extensions
    
    Returns:
        List of supported file extensions
    """
    return ['*.geojson', '*.gpkg', '*.shp', '*.kml', '*.gml', '*.json']

def find_vector_files(input_folder: str, recursive: bool = True) -> List[Path]:
    """
    Find all vector files in the input folder
    
    Args:
        input_folder: Path to search for vector files
        recursive: Whether to search recursively in subdirectories
    
    Returns:
        List of Path objects for found vector files
    """
    input_path = Path(input_folder)
    vector_files = []
    extensions = get_supported_extensions()
    
    search_method = input_path.rglob if recursive else input_path.glob
    
    for ext in extensions:
        found_files = list(search_method(ext))
        vector_files.extend(found_files)
        
        if found_files:
            logger.debug(f"Found {len(found_files)} {ext} files")
    
    # Remove duplicates and sort
    vector_files = sorted(list(set(vector_files)))
    
    logger.info(f"Found {len(vector_files)} total vector files")
    
    if not vector_files:
        logger.warning(f"No vector files found in: {input_folder}")
        logger.info(f"Supported formats: {', '.join(extensions)}")
    
    return vector_files

def filter_files_by_size(vector_files: List[Path], min_size_bytes: int = 100) -> List[Path]:
    """
    Filter out files that are too small (likely empty or corrupted)
    
    Args:
        vector_files: List of vector file paths
        min_size_bytes: Minimum file size in bytes
    
    Returns:
        List of filtered vector files
    """
    filtered_files = []
    
    for file_path in vector_files:
        try:
            if file_path.stat().st_size >= min_size_bytes:
                filtered_files.append(file_path)
            else:
                logger.warning(f"Skipping small file (likely empty): {file_path.name}")
        except OSError as e:
            logger.warning(f"Cannot access file {file_path.name}: {e}")
    
    logger.info(f"Filtered to {len(filtered_files)} valid files")
    return filtered_files
