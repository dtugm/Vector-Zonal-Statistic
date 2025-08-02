"""
Zonal statistics calculation functions
"""
import geopandas as gpd
from typing import List, Dict, Any
from rasterstats import zonal_stats
from utils.logger_config import logger

def get_default_statistics() -> List[str]:
    """
    Get default list of statistics to calculate
    
    Returns:
        List of statistic names
    """
    return ['mean', 'min', 'max', 'std', 'count']

def calculate_zonal_statistics(gdf: gpd.GeoDataFrame, raster_path: str, 
                             stats: List[str] = None, 
                             prefix: str = "") -> List[Dict[str, Any]]:
    """
    Calculate zonal statistics for given vector and raster data
    
    Args:
        gdf: GeoDataFrame with vector geometries
        raster_path: Path to raster file
        stats: List of statistics to calculate
        prefix: Prefix for statistic names
    
    Returns:
        List of dictionaries with zonal statistics
    """
    if stats is None:
        stats = get_default_statistics()
    
    try:
        logger.debug(f"Calculating zonal statistics with {len(gdf)} features")
        
        zonal_results = zonal_stats(
            gdf, 
            raster_path, 
            stats=stats,
            geojson_out=True,
            copy_properties=True,
            nodata=-9999  # Handle nodata values
        )
        
        # Add prefix to statistics if provided
        if prefix and zonal_results:
            for feature in zonal_results:
                props = feature['properties']
                for stat in stats:
                    if stat in props:
                        props[f'{prefix}_{stat}'] = props.pop(stat)
        
        logger.debug(f"Successfully calculated statistics for {len(zonal_results)} features")
        return zonal_results
        
    except Exception as e:
        logger.error(f"Error calculating zonal statistics: {e}")
        return []

def calculate_ohm_statistics(gdf: gpd.GeoDataFrame, ohm_raster: str) -> List[Dict[str, Any]]:
    """
    Calculate zonal statistics for OHM raster
    
    Args:
        gdf: GeoDataFrame with vector geometries
        ohm_raster: Path to OHM raster file
    
    Returns:
        List of dictionaries with OHM zonal statistics
    """
    logger.info("Calculating OHM zonal statistics")
    return calculate_zonal_statistics(gdf, ohm_raster, prefix="ohm")

def calculate_slope_statistics(gdf: gpd.GeoDataFrame, slope_raster: str) -> List[Dict[str, Any]]:
    """
    Calculate zonal statistics for slope raster
    
    Args:
        gdf: GeoDataFrame with vector geometries
        slope_raster: Path to slope raster file
    
    Returns:
        List of dictionaries with slope zonal statistics
    """
    logger.info("Calculating slope zonal statistics")
    return calculate_zonal_statistics(gdf, slope_raster, prefix="slope")
