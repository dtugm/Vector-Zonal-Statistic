# Vector Zonal Statistics Processor

A comprehensive tool for calculating zonal statistics from raster data across multiple vector files with both command-line interface (CLI) and graphical user interface (GUI) support.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Usage](#usage)
  - [GUI Interface](#gui-interface)
  - [CLI Interface](#cli-interface)
- [Project Structure](#project-structure)
- [Configuration](#configuration)
- [Examples](#examples)
- [Troubleshooting](#troubleshooting)
- [API Reference](#api-reference)
- [Contributing](#contributing)
- [License](#license)

## Overview

The Vector Zonal Statistics Processor is a powerful geospatial analysis tool that calculates statistical summaries (mean, median, std, min, max, count) of raster values within vector polygon boundaries. It supports batch processing of multiple vector files and provides both user-friendly GUI and efficient CLI interfaces.

### Key Capabilities

- **Batch Processing**: Process multiple vector files simultaneously
- **Multiple Statistics**: Calculate mean, median, standard deviation, min, max, and count
- **Coordinate System Handling**: Support for EPSG coordinate reference systems
- **Cross-Platform**: Works on Windows, macOS, and Linux
- **Dual Interface**: Both GUI and CLI options available
- **Conda Environment Support**: Integrated conda environment activation

## Features

### Core Features
- ✅ Batch zonal statistics calculation
- ✅ Multiple raster input support (OHM and Slope rasters)
- ✅ Vector shapefile processing
- ✅ EPSG coordinate reference system specification
- ✅ Comprehensive statistical outputs
- ✅ Progress tracking and logging
- ✅ Error handling and validation

### Interface Features
- ✅ **GUI Interface**: User-friendly graphical interface
- ✅ **CLI Interface**: Command-line batch processing
- ✅ **Cross-platform launchers**: Windows (.bat), macOS (.command), Linux (.sh)
- ✅ **Conda environment integration**: Automatic environment activation
- ✅ **Real-time progress monitoring**
- ✅ **Detailed logging and error reporting**

## Installation

### Prerequisites

- Python 3.8+ (recommended: Python 3.10)
- Miniconda or Anaconda
- Required Python packages:
  - `geopandas`
  - `rasterio`
  - `rasterstats`
  - `tkinter` (for GUI)

### Setup Instructions

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd vector-zonal-stats
   ```

2. **Create conda environment**:
   ```bash
   conda create -n py310 python=3.10
   conda activate py310
   ```

3. **Install dependencies**:
   ```bash
   pip install geopandas rasterio rasterstats
   # For conda users:
   conda install -c conda-forge geopandas rasterio
   pip install rasterstats
   ```

4. **Configure launcher scripts** (if needed):
   Edit the environment name in launcher scripts:
   ```bash
   # In run_gui.bat, run_gui.command, or run_gui.sh
   CONDA_ENV_NAME="py310"  # Change to your environment name
   ```

## Quick Start

### GUI Interface (Recommended for beginners)

**Windows:**
```cmd
# Double-click run_gui.bat or run from command prompt:
bin\run_gui.bat
```

**macOS:**
```bash
# Double-click run_gui.command in Finder or run:
./bin/run_gui.command
```

**Linux:**
```bash
# Run the shell script:
./bin/run_gui.sh
```

### CLI Interface (Recommended for batch processing)

```bash
# Basic usage
python main.py -o ohm_raster.tif -s slope_raster.tif -i input_vectors/ -out results/

# With EPSG specification
python main.py -o ohm.tif -s slope.tif -i ./vectors -out ./output --epsg 4326

# Show help
python main.py --help
```

## Usage

### GUI Interface

The GUI provides an intuitive interface for configuring and running zonal statistics analysis.

#### Main Interface Components

1. **Input Configuration Panel**
   - **OHM Raster File**: Select the primary raster file for analysis
   - **Slope Raster File**: Select the secondary raster file
   - **Input Vector Directory**: Choose directory containing vector files (.shp)
   - **Output Directory**: Specify where results will be saved
   - **EPSG Code**: Set coordinate reference system (optional)

2. **Processing Controls**
   - **Validate Inputs**: Check all inputs before processing
   - **Start Processing**: Begin batch analysis
   - **Clear Log**: Clear the output log window

3. **Progress Monitoring**
   - Real-time progress bar
   - Detailed logging output
   - Processing status updates

#### GUI Workflow

1. **Launch the GUI**:
   - Double-click the appropriate launcher for your OS
   - Wait for conda environment activation

2. **Configure Inputs**:
   ```
   OHM Raster: /path/to/ohm_data.tif
   Slope Raster: /path/to/slope_data.tif
   Vector Directory: /path/to/shapefiles/
   Output Directory: /path/to/results/
   EPSG Code: 4326 (optional)
   ```

3. **Validate and Process**:
   - Click "Validate Inputs" to check configuration
   - Click "Start Processing" to begin analysis
   - Monitor progress in the log window

4. **Review Results**:
   - Check output directory for CSV files
   - Review processing logs for any issues

#### GUI Features

- **File Browser Integration**: Easy file and directory selection
- **Input Validation**: Real-time validation of file paths and formats
- **Progress Tracking**: Visual progress bar and detailed logs
- **Error Handling**: Clear error messages and recovery suggestions
- **Cross-Platform**: Consistent interface across operating systems

### CLI Interface

The command-line interface provides powerful batch processing capabilities with full scripting support.

#### Command Syntax

```bash
python main.py [OPTIONS]
```

#### Required Arguments

| Argument | Short | Description | Example |
|----------|-------|-------------|---------|
| `--ohm` | `-o` | Path to OHM raster file | `-o data/ohm.tif` |
| `--slope` | `-s` | Path to slope raster file | `-s data/slope.tif` |
| `--input` | `-i` | Input directory with vector files | `-i ./vectors/` |
| `--output` | `-out` | Output directory for results | `-out ./results/` |

#### Optional Arguments

| Argument | Short | Description | Default | Example |
|----------|-------|-------------|---------|---------|
| `--epsg` | | EPSG code for coordinate system | Auto-detect | `--epsg 4326` |
| `--help` | `-h` | Show help message | | `--help` |

#### CLI Examples

1. **Basic Processing**:
   ```bash
   python main.py \
     --ohm /data/ohm_raster.tif \
     --slope /data/slope_raster.tif \
     --input /data/vector_files/ \
     --output /results/
   ```

2. **With EPSG Specification**:
   ```bash
   python main.py \
     -o ohm.tif \
     -s slope.tif \
     -i ./input_vectors \
     -out ./output_results \
     --epsg 3857
   ```

3. **Processing with Relative Paths**:
   ```bash
   python main.py -o data/ohm.tif -s data/slope.tif -i vectors/ -out results/
   ```

4. **Batch Processing Script**:
   ```bash
   #!/bin/bash
   # Process multiple datasets
   for dataset in dataset1 dataset2 dataset3; do
     python main.py \
       -o "data/${dataset}/ohm.tif" \
       -s "data/${dataset}/slope.tif" \
       -i "vectors/${dataset}/" \
       -out "results/${dataset}/" \
       --epsg 4326
   done
   ```

#### CLI Output

The CLI provides detailed logging and progress information:

```
2025-08-02 23:14:22,164 - zonal_stats - INFO - Starting Batch Zonal Statistics Processor
2025-08-02 23:14:22,164 - zonal_stats - INFO - OHM Raster: data/test/rasters/SLOPE_DKI.tif
2025-08-02 23:14:22,164 - zonal_stats - INFO - Slope Raster: data/test/rasters/SLOPE_DKI.tif
2025-08-02 23:14:22,164 - zonal_stats - INFO - Input Folder: data/test/vectors/
2025-08-02 23:14:22,164 - zonal_stats - INFO - Output Folder: data/test/out
2025-08-02 23:14:22,164 - zonal_stats - INFO - CRS output: 32748
2025-08-02 23:14:22,164 - zonal_stats - INFO - OHM raster validated: data/test/rasters/SLOPE_DKI.tif
2025-08-02 23:14:22,164 - zonal_stats - INFO - Slope raster validated: data/test/rasters/SLOPE_DKI.tif
2025-08-02 23:14:22,164 - zonal_stats - INFO - Input folder validated: data/test/vectors/
2025-08-02 23:14:22,164 - zonal_stats - INFO - Output folder validated/created: data/test/out
2025-08-02 23:14:22,164 - zonal_stats - INFO - Starting batch processing
2025-08-02 23:14:22,166 - zonal_stats - INFO - Found 36 total vector files
2025-08-02 23:14:22,166 - zonal_stats - INFO - Filtered to 36 valid files
2025-08-02 23:14:22,166 - zonal_stats - INFO - Processing file 1/36: AG-09-A_BO_Caesar Yoga_BUFFER_Lengkap.geojson
2025-08-02 23:14:22,166 - zonal_stats - INFO - Processing: AG-09-A_BO_Caesar Yoga_BUFFER_Lengkap.geojson
2025-08-02 23:14:22,304 - zonal_stats - INFO - Calculating OHM zonal statistics
2025-08-02 23:14:22,653 - zonal_stats - INFO - Calculating slope zonal statistics
2025-08-02 23:14:22,946 - zonal_stats - INFO - Successfully combined statistics for 141 features
...
...
2025-08-02 23:16:11,184 - zonal_stats - INFO - Processing summary saved to: data/test/out/processing_summary.json
2025-08-02 23:16:11,184 - zonal_stats - INFO - Batch processing completed: 36/36 files processed successfully
2025-08-02 23:16:11,184 - zonal_stats - INFO - All files processed successfully!
```

## Project Structure

```
vector-zonal-stats/
├── bin/                         # Launcher scripts
│   ├── run_gui.bat              # Windows GUI launcher
│   ├── run_gui.command          # macOS GUI launcher (double-click)
│   ├── run_gui.sh               # Linux GUI launcher
├── core/                        # Core processing modules
│   ├── __init__.py
│   ├── processor.py             # Main processing logic
│   ├── validator.py             # Input validation
│   └── statistics.py            # Statistical calculations
├── ui/                          # User interface modules
│   ├── __init__.py
│   └── gui_main.py              # GUI implementation
├── utils/                       # Utility modules
│   ├── __init__.py
│   ├── logger_config.py         # Logging configuration
│   └── file_utils.py            # File handling utilities
├── main.py                      # CLI entry point
├── launcher.py                  # Cross-platform launcher
└── README.md                    # This documentation
```

## Configuration

### EPSG Coordinate Reference Systems

The application supports EPSG codes for coordinate reference system specification:

#### Common EPSG Codes
- **4326**: WGS 84 (Geographic, degrees)
- **3857**: Web Mercator (Projected, meters)
- **32748**: UTM Zone 48S (Projected, meters)
- **4269**: NAD83 (Geographic, degrees)

#### EPSG Usage
```bash
# CLI usage
python main.py -o ohm.tif -s slope.tif -i vectors/ -out results/ --epsg 4326

# GUI usage
# Enter EPSG code in the "EPSG Code" field (e.g., "4326")
```

### Environment Configuration

Edit launcher scripts to match your conda environment:

```bash
# In run_gui.bat, run_gui.command, run_gui.sh
CONDA_ENV_NAME="your_environment_name"
```

## Examples

### Example 1: Basic GUI Processing

1. Launch GUI: Double-click `run_gui.command` (macOS) or `run_gui.bat` (Windows)
2. Configure inputs:
   - OHM Raster: `data/elevation.tif`
   - Slope Raster: `data/slope.tif`
   - Vector Directory: `shapefiles/watersheds/`
   - Output Directory: `results/watersheds/`
3. Click "Validate Inputs" then "Start Processing"

### Example 2: CLI Batch Processing

```bash
# Activate conda environment
conda activate py310

# Run batch processing
python main.py \
  --ohm data/dem.tif \
  --slope data/slope.tif \
  --input shapefiles/study_areas/ \
  --output results/study_areas/ \
  --epsg 32633
```

### Example 3: Multiple Dataset Processing

```bash
#!/bin/bash
# Process multiple study regions
regions=("north" "south" "east" "west")

for region in "${regions[@]}"; do
  echo "Processing region: $region"
  python main.py \
    -o "data/${region}/ohm.tif" \
    -s "data/${region}/slope.tif" \
    -i "vectors/${region}/" \
    -out "results/${region}/" \
    --epsg 4326
done
```

## Troubleshooting

### Common Issues

#### 1. Conda Environment Not Found
```
ERROR: Conda environment 'py310' not found!
```
**Solution**:
```bash
conda create -n py310 python=3.10
conda activate py310
pip install geopandas rasterio rasterstats
```

#### 2. Missing Dependencies
```
ERROR: ModuleNotFoundError: No module named 'geopandas'
```
**Solution**:
```bash
conda activate py310
pip install geopandas rasterio rasterstats
```

#### 3. EPSG Code Issues
```
ERROR: Invalid EPSG code or coordinate system mismatch
```
**Solution**:
- Verify EPSG code is valid (e.g., 4326, 3857)
- Ensure all input files use compatible coordinate systems
- Check raster and vector CRS compatibility

#### 4. File Path Issues
```
ERROR: File not found or inaccessible
```
**Solution**:
- Use absolute paths when possible
- Check file permissions
- Verify file formats (.tif for rasters, .shp for vectors)

#### 5. GUI Won't Start
```
ERROR: tkinter is not available
```
**Solution**:
```bash
conda activate py310
conda install tk
```

### Performance Tips

1. **Use appropriate EPSG codes** for your region to minimize reprojection overhead
2. **Organize vector files** in separate directories for different processing batches
3. **Monitor memory usage** when processing large raster files
4. **Use SSD storage** for faster I/O operations

### Getting Help

1. **Check logs**: Review detailed logs in GUI or CLI output
2. **Validate inputs**: Use the validation function before processing
3. **Test with small datasets**: Verify setup with minimal data first
4. **Check file formats**: Ensure rasters are GeoTIFF and vectors are Shapefile format

## API Reference

### Core Functions

#### `validate_all_inputs(ohm_path, slope_path, input_dir, output_dir, epsg=None)`
Validates all input parameters and files.

**Parameters**:
- `ohm_path` (str): Path to OHM raster file
- `slope_path` (str): Path to slope raster file  
- `input_dir` (str): Directory containing vector files
- `output_dir` (str): Output directory for results
- `epsg` (int, optional): EPSG code for coordinate system

**Returns**: `bool` - True if all inputs are valid

#### `run_batch_processing(ohm_path, slope_path, input_dir, output_dir, epsg=None)`
Executes batch zonal statistics processing.

**Parameters**: Same as `validate_all_inputs`

**Returns**: `bool` - True if processing completed successfully

### GUI Classes

#### `ZonalStatsGUI(root)`
Main GUI application class.

**Methods**:
- `setup_ui()`: Initialize user interface components
- `validate_inputs()`: Validate user inputs
- `start_processing()`: Begin batch processing
- `update_progress(value, message)`: Update progress display

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request

### Development Setup

```bash
# Clone repository
git clone <repository-url>
cd vector-zonal-stats

# Create development environment
conda create -n zonal-stats-dev python=3.10
conda activate zonal-stats-dev
pip install -r requirements.txt

# Install development dependencies
pip install pytest black flake8
```

## License

This project is licensed under the MIT License. See LICENSE file for details.

---

**Version**: 1.0.0  
**Last Updated**: 2025  
**Compatibility**: Python 3.8+, Windows/macOS/Linux