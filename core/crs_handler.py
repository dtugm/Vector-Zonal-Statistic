"""
Coordinate Reference System (CRS) handling functions
"""
import geopandas as gpd
import rasterio
from pathlib import Path
from utils.logger_config import logger

def get_raster_crs(raster_path: str):
    """
    Get CRS from raster file
    
    Args:
        raster_path: Path to raster file
    
    Returns:
        CRS object or None if error
    """
    try:
        with rasterio.open(raster_path) as src:
            return src.crs
    except Exception as e:
        logger.error(f"Cannot read CRS from raster {raster_path}: {e}")
        return None

def load_and_reproject_vector(vector_file: Path, target_crs) -> gpd.GeoDataFrame:
    """
    Load vector file and reproject to target CRS if necessary
    
    Args:
        vector_file: Path to vector file
        target_crs: Target CRS for reprojection
    
    Returns:
        GeoDataFrame with aligned CRS
    """
    try:
        # Read vector data
        gdf = gpd.read_file(vector_file)
        
        if gdf.empty:
            logger.warning(f"Empty vector file: {vector_file.name}")
            return gdf
        
        # Check if reprojection is needed
        if gdf.crs is None:
            logger.warning(f"No CRS defined for {vector_file.name}, assuming target CRS")
            gdf.crs = target_crs
        elif gdf.crs != target_crs:
            logger.info(f"Reprojecting {vector_file.name} from {gdf.crs} to {target_crs}")
            gdf = gdf.to_crs(target_crs)
        else:
            logger.debug(f"CRS already matches for {vector_file.name}")
        
        return gdf
        
    except Exception as e:
        logger.error(f"Error loading/reprojecting {vector_file.name}: {e}")
        return gpd.GeoDataFrame()

def check_crs_compatibility(vector_file: Path, raster_file: str) -> gpd.GeoDataFrame:
    """
    Check and align CRS between vector and raster data
    
    Args:
        vector_file: Path to vector file
        raster_file: Path to raster file
    
    Returns:
        GeoDataFrame with aligned CRS
    """
    # Get raster CRS
    raster_crs = get_raster_crs(raster_file)
    if raster_crs is None:
        logger.error(f"Cannot determine raster CRS for {raster_file}")
        return gpd.GeoDataFrame()
    
    # Load and reproject vector
    return load_and_reproject_vector(vector_file, raster_crs)
