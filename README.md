# Vector Zonal Statistics Processor CLI

A command-line interface for calculating zonal statistics from raster data across multiple vector files in batch processing mode.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [API Reference](#api-reference)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Batch Zonal Statistics Processor is a Python CLI tool designed to efficiently calculate zonal statistics from OHM (Organic Hazard Model) and slope raster data across multiple vector files. This tool is particularly useful for environmental analysis, risk assessment, and spatial data processing workflows [1].

### Key Capabilities

- **Batch Processing**: Process multiple vector files automatically
- **Multi-Raster Support**: Calculate statistics from both OHM and slope rasters
- **Format Flexibility**: Supports various vector formats (GeoJSON, Shapefile, GPKG, KML, GML)
- **CRS Handling**: Automatic coordinate reference system alignment
- **Error Recovery**: Robust error handling with detailed logging
- **Modular Design**: Clean, maintainable codebase with separated concerns

## Features

### Core Functionality
- ✅ Batch processing of vector files
- ✅ Zonal statistics calculation (mean, min, max, std, count)
- ✅ Automatic CRS reprojection
- ✅ Multiple input format support
- ✅ GeoJSON output format
- ✅ Comprehensive logging system
- ✅ Processing summary reports

### Supported File Formats

**Input Vector Formats:**
- GeoJSON (`.geojson`, `.json`)
- Geopackage (`.gpkg`)
- Shapefile (`.shp`)
- KML (`.kml`)
- GML (`.gml`)

**Input Raster Formats:**
- GeoTIFF (`.tif`, `.tiff`)
- IMG (`.img`)
- NetCDF (`.nc`)

**Output Format:**
- GeoJSON (`.geojson`)

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Install Dependencies

```bash
# Clone the repository
git clone <repository-url>
cd zonal_stats_cli

# Install required packages
pip install -r requirements.txt
```

### Dependencies

```txt
geopandas>=0.12.0
rasterstats>=0.15.0
rasterio>=1.3.0
shapely>=2.0.0
fiona>=1.8.0
```

### Verify Installation

```bash
python main.py --version
```

## Quick Start

### Basic Usage

```bash
python main.py -o ohm_raster.tif -s slope_raster.tif -i ./input_vectors -out ./results
```

### With Verbose Logging

```bash
python main.py -o ohm.tif -s slope.tif -i ./digitasi -out ./output --verbose
```

## Usage

### Command Line Interface

The CLI follows Python best practices for command-line tool design, providing clear argument structure and helpful error messages [2].

```bash
python main.py [OPTIONS]
```

### Required Arguments

| Argument | Short | Description |
|----------|-------|-------------|
| `--ohm-raster` | `-o` | Path to OHM raster file |
| `--slope-raster` | `-s` | Path to slope raster file |
| `--input-folder` | `-i` | Path to folder containing vector files |
| `--output-folder` | `-out` | Path to output folder for results |

### Optional Arguments

| Argument | Description |
|----------|-------------|
| `--verbose` | Enable verbose logging output |
| `--version` | Show version information |
| `--help` | Show help message and exit |

### Exit Codes

Following CLI best practices for exit code handling [3]:

- `0`: Success - All files processed successfully
- `1`: Partial failure or error occurred
- `2`: Invalid arguments or input validation failed

## Project Structure

The project follows Python packaging best practices with a modular structure that separates concerns and improves maintainability [1]:

```
zonal_stats_cli/
├── main.py                 # CLI entry point
├── requirements.txt        # Project dependencies
├── README.md              # This documentation
├── core/                  # Core processing modules
│   ├── __init__.py
│   ├── validation.py      # Input validation functions
│   ├── file_finder.py     # Vector file discovery
│   ├── crs_handler.py     # CRS management
│   ├── zonal_calculator.py # Statistics calculation
│   ├── statistics_combiner.py # Data combination
│   ├── result_saver.py    # Output file handling
│   └── batch_processor.py # Main processing logic
└── utils/                 # Utility modules
    ├── __init__.py
    └── logger_config.py   # Logging configuration
```

### Module Responsibilities

Each module has a single, well-defined responsibility following the Single Responsibility Principle [4]:

- **validation.py**: Validates input files and folders
- **file_finder.py**: Discovers and filters vector files
- **crs_handler.py**: Manages coordinate reference systems
- **zonal_calculator.py**: Calculates zonal statistics
- **statistics_combiner.py**: Combines results from multiple rasters
- **result_saver.py**: Saves results to output files
- **batch_processor.py**: Orchestrates the entire processing workflow

## API Reference

### Core Functions

#### `validate_all_inputs(ohm_raster, slope_raster, input_folder, output_folder)`

Validates all input parameters before processing.

**Parameters:**
- `ohm_raster` (str): Path to OHM raster file
- `slope_raster` (str): Path to slope raster file
- `input_folder` (str): Path to input folder
- `output_folder` (str): Path to output folder

**Returns:**
- `bool`: True if all inputs are valid

#### `run_batch_processing(ohm_raster, slope_raster, input_folder, output_folder)`

Executes batch processing of all vector files.

**Parameters:**
- `ohm_raster` (str): Path to OHM raster file
- `slope_raster` (str): Path to slope raster file
- `input_folder` (str): Path to input folder
- `output_folder` (str): Path to output folder

**Returns:**
- `tuple`: (successful_count, total_count)

### Utility Functions

#### `setup_logger(name, level)`

Configures logging with consistent formatting.

**Parameters:**
- `name` (str): Logger name
- `level` (int): Logging level

**Returns:**
- `logging.Logger`: Configured logger instance

#### `find_vector_files(input_folder, recursive=True)`

Discovers vector files in the input directory.

**Parameters:**
- `input_folder` (str): Path to search directory
- `recursive` (bool): Whether to search subdirectories

**Returns:**
- `List[Path]`: List of discovered vector files

## Examples

### Example 1: Basic Processing

Process all vector files in a folder with OHM and slope rasters:

```bash
python main.py \
  --ohm-raster /data/rasters/ohm_model.tif \
  --slope-raster /data/rasters/slope_degrees.tif \
  --input-folder /data/vectors/study_areas \
  --output-folder /results/zonal_stats
```

### Example 2: Verbose Processing

Enable detailed logging for debugging:

```bash
python main.py \
  -o ohm.tif \
  -s slope.tif \
  -i ./digitasi \
  -out ./results \
  --verbose
```

### Example 3: Processing with Different CRS

The tool automatically handles CRS differences:

```bash
# Vector files in UTM, rasters in WGS84 - automatically handled
python main.py -o wgs84_ohm.tif -s wgs84_slope.tif -i ./utm_vectors -out ./results
```

### Output Structure

Each processed vector file generates a corresponding GeoJSON output:

```
results/
├── area1_zonal_stats.geojson
├── area2_zonal_stats.geojson
├── area3_zonal_stats.geojson
└── processing_summary.json
```

### Sample Output Feature

```json
{
  "type": "Feature",
  "geometry": { ... },
  "properties": {
    "original_id": 1,
    "area_name": "Study Area 1",
    "ohm_mean": 0.75,
    "ohm_min": 0.12,
    "ohm_max": 1.0,
    "ohm_std": 0.23,
    "ohm_count": 1250,
    "slope_mean": 15.6,
    "slope_min": 0.0,
    "slope_max": 45.2,
    "slope_std": 8.9,
    "slope_count": 1250
  }
}
```

## Troubleshooting

### Common Issues

#### 1. "No vector files found"

**Problem**: The tool cannot find vector files in the input folder.

**Solutions:**
- Verify the input folder path exists
- Check that files have supported extensions (.geojson, .shp, .gpkg, .kml, .gml)
- Ensure files are not empty or corrupted
- Use `--verbose` flag to see detailed file discovery logs

#### 2. "CRS reprojection failed"

**Problem**: Coordinate reference system alignment issues.

**Solutions:**
- Verify both raster and vector files have defined CRS
- Check that input files are not corrupted
- Ensure raster files have proper geospatial metadata

#### 3. "Empty statistics results"

**Problem**: Zonal statistics calculation returns empty results.

**Solutions:**
- Verify vector geometries overlap with raster extent
- Check that raster files contain valid data (not all NoData)
- Ensure vector geometries are valid (not self-intersecting)

#### 4. Memory issues with large files

**Problem**: Out of memory errors with large datasets.

**Solutions:**
- Process files in smaller batches
- Ensure sufficient system RAM
- Consider simplifying complex geometries

### Logging and Debugging

Enable verbose logging for detailed troubleshooting:

```bash
python main.py [args] --verbose
```

Log levels:
- **INFO**: General processing information
- **DEBUG**: Detailed step-by-step processing (verbose mode)
- **WARNING**: Non-fatal issues that may affect results
- **ERROR**: Fatal errors that prevent processing

### Getting Help

For additional help:

```bash
python main.py --help
```

## Performance Considerations

### Optimization Tips

1. **File Organization**: Group related vector files in the same folder
2. **CRS Alignment**: Pre-align CRS when possible to avoid reprojection overhead
3. **File Formats**: GeoJSON typically processes faster than Shapefiles
4. **System Resources**: Ensure adequate RAM for large raster files

### Expected Processing Times

Processing time depends on:
- Number and size of vector files
- Raster resolution and extent
- System specifications
- Complexity of vector geometries

Typical performance: 10-50 vector files per minute on standard hardware.

## Contributing

### Development Setup

1. Fork the repository
2. Create a virtual environment
3. Install development dependencies
4. Make your changes
5. Run tests
6. Submit a pull request

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Include docstrings for all functions
- Maintain modular structure

### Testing

Run tests before submitting changes:

```bash
python -m pytest tests/
```

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---

## Support

For issues, questions, or contributions, please:
1. Check the troubleshooting section
2. Search existing issues
3. Create a new issue with detailed information
4. Include log output when reporting bugs

**Version**: 1.0.0  
**Python Compatibility**: 3.10+  
**Last Updated**: 2025