"""
CLI interface for batch zonal statistics processing
"""
import argparse
import sys
import logging
from utils.logger_config import setup_logger, logger
from core import validate_all_inputs, run_batch_processing

def create_argument_parser():
    """
    Create and configure argument parser for CLI
    Following argparse best practices for modular CLI design
    """
    parser = argparse.ArgumentParser(
        description='Batch Zonal Statistics Processor - Calculate zonal statistics for multiple vector files',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py -o ohm.tif -s slope.tif -i ./digitasi -out ./results
  python main.py --ohm-raster ohm.tif --slope-raster slope.tif --input-folder ./digitasi --output-folder ./results --verbose
        """
    )
    
    # Required arguments
    parser.add_argument(
        '-o', '--ohm-raster',
        required=True,
        help='Path to OHM raster file (.tif, .tiff)'
    )
    
    parser.add_argument(
        '-s', '--slope-raster',
        required=True,
        help='Path to slope raster file (.tif, .tiff)'
    )
    
    parser.add_argument(
        '-i', '--input-folder',
        required=True,
        help='Path to input folder containing vector files (DIGITASI folder)'
    )
    
    parser.add_argument(
        '-out', '--output-folder',
        required=True,
        help='Path to output folder for results'
    )
    
    # Optional arguments
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose logging'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='Zonal Stats CLI v1.0.0'
    )
    
    return parser

def configure_logging(verbose: bool):
    """Configure logging based on verbosity level"""
    level = logging.DEBUG if verbose else logging.INFO
    setup_logger('zonal_stats', level)
    
    if verbose:
        logger.info("Verbose logging enabled")

def main():
    """
    Main CLI entry point following Python CLI best practices
    """
    # Create argument parser
    parser = create_argument_parser()
    
    # Parse arguments
    args = parser.parse_args()
    
    # Setup logging
    configure_logging(args.verbose)
    
    # Log startup information
    logger.info("Starting Batch Zonal Statistics Processor")
    logger.info(f"OHM Raster: {args.ohm_raster}")
    logger.info(f"Slope Raster: {args.slope_raster}")
    logger.info(f"Input Folder: {args.input_folder}")
    logger.info(f"Output Folder: {args.output_folder}")
    
    # Validate inputs
    if not validate_all_inputs(args.ohm_raster, args.slope_raster, 
                              args.input_folder, args.output_folder):
        logger.error("Input validation failed. Please check your inputs.")
        sys.exit(1)
    
    # Process files
    try:
        successful_count, total_count = run_batch_processing(
            args.ohm_raster,
            args.slope_raster,
            args.input_folder,
            args.output_folder
        )
        
        if successful_count == total_count:
            logger.info("All files processed successfully!")
            sys.exit(0)
        elif successful_count > 0:
            logger.warning(f"Partial success: {successful_count}/{total_count} files processed")
            sys.exit(1)
        else:
            logger.error("No files were processed successfully")
            sys.exit(1)
            
    except KeyboardInterrupt:
        logger.info("Processing interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
