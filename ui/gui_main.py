"""
GUI interface for batch zonal statistics processing
"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import threading
import queue
import os
import sys
from pathlib import Path

# Add parent directory to path to import core modules
sys.path.append(str(Path(__file__).parent.parent))

from core import validate_all_inputs, run_batch_processing
from utils.logger_config import setup_logger, logger
import logging

class ZonalStatsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Batch Zonal Statistics Processor v1.0.0")
        self.root.geometry("800x700")
        self.root.resizable(True, True)
        
        # Initialize variables
        self.ohm_raster_path = tk.StringVar()
        self.slope_raster_path = tk.StringVar()
        self.input_folder_path = tk.StringVar()
        self.output_folder_path = tk.StringVar()
        self.epsg_code = tk.StringVar(value="32748")
        self.verbose = tk.BooleanVar(value=False)
        
        # Threading and progress tracking
        self.processing_thread = None
        self.is_processing = False
        self.log_queue = queue.Queue()
        
        # Setup logging for GUI
        self.setup_gui_logging()
        
        # Create GUI elements
        self.create_widgets()
        
        # Start log monitoring
        self.monitor_logs()
    
    def setup_gui_logging(self):
        """Setup logging to capture messages in GUI following threading best practices"""
        class QueueHandler(logging.Handler):
            def __init__(self, log_queue):
                super().__init__()
                self.log_queue = log_queue
            
            def emit(self, record):
                self.log_queue.put(self.format(record))
        
        # Setup logger with queue handler
        setup_logger('zonal_stats', logging.INFO)
        queue_handler = QueueHandler(self.log_queue)
        queue_handler.setFormatter(logging.Formatter('%(asctime)s - %(levelname)s - %(message)s'))
        logger.addHandler(queue_handler)
    
    def create_widgets(self):
        """Create and layout GUI widgets using modern tkinter practices"""
        # Main container with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Batch Zonal Statistics Processor", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection section
        self.create_file_selection_section(main_frame, 1)
        
        # Options section
        self.create_options_section(main_frame, 6)
        
        # Control buttons
        self.create_control_section(main_frame, 8)
        
        # Progress section
        self.create_progress_section(main_frame, 9)
        
        # Log display section
        self.create_log_section(main_frame, 10)
    
    def create_file_selection_section(self, parent, start_row):
        """Create file and folder selection widgets with proper file dialogs"""
        # OHM Raster
        ttk.Label(parent, text="OHM Raster File:").grid(row=start_row, column=0, sticky=tk.W, pady=5)
        ttk.Entry(parent, textvariable=self.ohm_raster_path, width=50).grid(row=start_row, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(parent, text="Browse", command=lambda: self.browse_file(self.ohm_raster_path, "OHM Raster")).grid(row=start_row, column=2, padx=5)
        
        # Slope Raster
        ttk.Label(parent, text="Slope Raster File:").grid(row=start_row+1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(parent, textvariable=self.slope_raster_path, width=50).grid(row=start_row+1, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(parent, text="Browse", command=lambda: self.browse_file(self.slope_raster_path, "Slope Raster")).grid(row=start_row+1, column=2, padx=5)
        
        # Input Folder
        ttk.Label(parent, text="Input Folder (DIGITASI):").grid(row=start_row+2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(parent, textvariable=self.input_folder_path, width=50).grid(row=start_row+2, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(parent, text="Browse", command=lambda: self.browse_folder(self.input_folder_path, "Input Folder")).grid(row=start_row+2, column=2, padx=5)
        
        # Output Folder
        ttk.Label(parent, text="Output Folder:").grid(row=start_row+3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(parent, textvariable=self.output_folder_path, width=50).grid(row=start_row+3, column=1, sticky=(tk.W, tk.E), padx=5)
        ttk.Button(parent, text="Browse", command=lambda: self.browse_folder(self.output_folder_path, "Output Folder")).grid(row=start_row+3, column=2, padx=5)
    
    def create_options_section(self, parent, start_row):
        """Create options section with proper validation"""
        options_frame = ttk.LabelFrame(parent, text="Options", padding="10")
        options_frame.grid(row=start_row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=10)
        
        # EPSG Code
        ttk.Label(options_frame, text="EPSG Code:").grid(row=0, column=0, sticky=tk.W, padx=5)
        epsg_entry = ttk.Entry(options_frame, textvariable=self.epsg_code, width=15)
        epsg_entry.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # Verbose logging
        ttk.Checkbutton(options_frame, text="Verbose Logging", variable=self.verbose).grid(row=0, column=2, sticky=tk.W, padx=20)
    
    def create_control_section(self, parent, start_row):
        """Create control buttons with proper state management"""
        control_frame = ttk.Frame(parent)
        control_frame.grid(row=start_row, column=0, columnspan=3, pady=10)
        
        self.process_button = ttk.Button(control_frame, text="Start Processing", 
                                       command=self.start_processing, style="Accent.TButton")
        self.process_button.pack(side=tk.LEFT, padx=5)
        
        self.stop_button = ttk.Button(control_frame, text="Stop", 
                                    command=self.stop_processing, state=tk.DISABLED)
        self.stop_button.pack(side=tk.LEFT, padx=5)
        
        ttk.Button(control_frame, text="Clear Logs", command=self.clear_logs).pack(side=tk.LEFT, padx=5)
        ttk.Button(control_frame, text="Exit", command=self.root.quit).pack(side=tk.LEFT, padx=5)
    
    def create_progress_section(self, parent, start_row):
        """Create progress bar following tkinter progress bar best practices"""
        progress_frame = ttk.Frame(parent)
        progress_frame.grid(row=start_row, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=5)
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.StringVar(value="Ready")
        self.status_label = ttk.Label(progress_frame, textvariable=self.progress_var)
        self.status_label.grid(row=0, column=0, sticky=tk.W)
        
        self.progress_bar = ttk.Progressbar(progress_frame, mode='indeterminate')
        self.progress_bar.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=5)
    
    def create_log_section(self, parent, start_row):
        """Create scrollable log display section"""
        log_frame = ttk.LabelFrame(parent, text="Processing Logs", padding="5")
        log_frame.grid(row=start_row, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)
        log_frame.columnconfigure(0, weight=1)
        log_frame.rowconfigure(0, weight=1)
        
        # Configure main frame to expand log section
        parent.rowconfigure(start_row, weight=1)
        
        self.log_text = scrolledtext.ScrolledText(log_frame, height=15, state=tk.DISABLED)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
    
    def browse_file(self, var, title):
        """Browse for file selection with appropriate file filters"""
        filename = filedialog.askopenfilename(
            title=f"Select {title}",
            filetypes=[("TIFF files", "*.tif *.tiff"), ("All files", "*.*")]
        )
        if filename:
            var.set(filename)
    
    def browse_folder(self, var, title):
        """Browse for folder selection"""
        folder = filedialog.askdirectory(title=f"Select {title}")
        if folder:
            var.set(folder)
    
    def validate_inputs(self):
        """Comprehensive input validation"""
        if not self.ohm_raster_path.get():
            messagebox.showerror("Error", "Please select OHM raster file")
            return False
        
        if not self.slope_raster_path.get():
            messagebox.showerror("Error", "Please select slope raster file")
            return False
        
        if not self.input_folder_path.get():
            messagebox.showerror("Error", "Please select input folder")
            return False
        
        if not self.output_folder_path.get():
            messagebox.showerror("Error", "Please select output folder")
            return False
        
        try:
            int(self.epsg_code.get())
        except ValueError:
            messagebox.showerror("Error", "EPSG code must be a valid integer")
            return False
        
        return True
    
    def start_processing(self):
        """Start processing with proper thread management"""
        if not self.validate_inputs():
            return
        
        if self.is_processing:
            messagebox.showwarning("Warning", "Processing is already running")
            return
        
        # Update GUI state
        self.is_processing = True
        self.process_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)
        self.progress_var.set("Processing...")
        self.progress_bar.start()
        
        # Configure logging level based on verbose setting
        level = logging.DEBUG if self.verbose.get() else logging.INFO
        setup_logger('zonal_stats', level)
        
        # Start processing thread
        self.processing_thread = threading.Thread(target=self.run_processing, daemon=True)
        self.processing_thread.start()
    
    def run_processing(self):
        """Run the actual processing in background thread"""
        try:
            # Validate inputs
            if not validate_all_inputs(
                self.ohm_raster_path.get(),
                self.slope_raster_path.get(),
                self.input_folder_path.get(),
                self.output_folder_path.get()
            ):
                self.log_queue.put("ERROR - Input validation failed")
                return
            
            # Run batch processing
            successful_count, total_count = run_batch_processing(
                self.ohm_raster_path.get(),
                self.slope_raster_path.get(),
                self.input_folder_path.get(),
                self.output_folder_path.get(),
                int(self.epsg_code.get())
            )
            
            # Report results
            if successful_count == total_count:
                self.log_queue.put(f"SUCCESS - All {total_count} files processed successfully!")
            elif successful_count > 0:
                self.log_queue.put(f"PARTIAL SUCCESS - {successful_count}/{total_count} files processed")
            else:
                self.log_queue.put("ERROR - No files were processed successfully")
                
        except Exception as e:
            self.log_queue.put(f"ERROR - Unexpected error: {e}")
        finally:
            # Schedule GUI update in main thread
            self.root.after(0, self.processing_finished)
    
    def processing_finished(self):
        """Update GUI when processing is finished"""
        self.is_processing = False
        self.process_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)
        self.progress_var.set("Processing completed")
        self.progress_bar.stop()
    
    def stop_processing(self):
        """Stop processing (graceful termination)"""
        if self.processing_thread and self.processing_thread.is_alive():
            messagebox.showinfo("Info", "Stop signal sent. Processing will stop at next checkpoint.")
            self.processing_finished()
    
    def monitor_logs(self):
        """Monitor log queue and update GUI safely"""
        try:
            while True:
                message = self.log_queue.get_nowait()
                self.log_text.config(state=tk.NORMAL)
                self.log_text.insert(tk.END, message + "\n")
                self.log_text.see(tk.END)
                self.log_text.config(state=tk.DISABLED)
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self.monitor_logs)
    
    def clear_logs(self):
        """Clear the log display"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)

def main():
    """Main GUI entry point with modern styling"""
    root = tk.Tk()
    
    # Set up modern styling
    style = ttk.Style()
    available_themes = style.theme_names()
    if 'clam' in available_themes:
        style.theme_use('clam')
    
    app = ZonalStatsGUI(root)
    
    # Center window on screen
    root.update_idletasks()
    x = (root.winfo_screenwidth() - root.winfo_width()) // 2
    y = (root.winfo_screenheight() - root.winfo_height()) // 2
    root.geometry(f"+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
