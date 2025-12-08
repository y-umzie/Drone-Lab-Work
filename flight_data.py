import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv
from datetime import datetime
import os
from pathlib import Path

class FlightLogGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Log Entry System")
        self.root.geometry("900x750")
        
        # Create main frame with scrollbar
        main_frame = ttk.Frame(root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(main_frame)
        scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Set default save location to Desktop
        self.desktop_path = Path.home() / "Desktop"
        self.csv_file = self.desktop_path / "flight_logs.csv"
        
        # Create form
        self.create_form()
        
        # Create buttons
        button_frame = ttk.Frame(self.scrollable_frame)
        button_frame.grid(row=20, column=0, columnspan=4, pady=20)
        
        ttk.Button(button_frame, text="Save Entry", command=self.save_entry).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear Form", command=self.clear_form).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Export to CSV", command=self.export_to_csv).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Open CSV File", command=self.open_csv).pack(side=tk.LEFT, padx=5)
        
        # Initialize CSV file if it doesn't exist
        self.init_csv_file()
        
    def create_form(self):
        # Title
        title_label = ttk.Label(self.scrollable_frame, text="FLIGHT LOG", font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=4, pady=(0, 20))
        
        # GENERAL section
        general_frame = ttk.LabelFrame(self.scrollable_frame, text="GENERAL", padding="10")
        general_frame.grid(row=1, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        
        ttk.Label(general_frame, text="FLIGHT #:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.flight_number = ttk.Entry(general_frame, width=15)
        self.flight_number.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(general_frame, text="DATE:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.date = ttk.Entry(general_frame, width=15)
        self.date.grid(row=0, column=3, sticky="w", padx=5, pady=2)
        # Insert current date as default
        self.date.insert(0, datetime.now().strftime("%d/%m/%Y"))
        
        ttk.Label(general_frame, text="WIND:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.wind = ttk.Entry(general_frame, width=15)
        self.wind.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        ttk.Label(general_frame, text="m/s").grid(row=1, column=2, sticky="w", pady=2)
        
        ttk.Label(general_frame, text="WEATHER:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.weather = ttk.Entry(general_frame, width=15)
        self.weather.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(general_frame, text="TEMP:").grid(row=2, column=2, sticky="w", padx=5, pady=2)
        self.temperature = ttk.Entry(general_frame, width=15)
        self.temperature.grid(row=2, column=3, sticky="w", padx=5, pady=2)
        ttk.Label(general_frame, text="°C").grid(row=2, column=4, sticky="w", pady=2)
        
        # PRE-FLIGHT section
        pre_flight_frame = ttk.LabelFrame(self.scrollable_frame, text="PRE-FLIGHT", padding="10")
        pre_flight_frame.grid(row=2, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        
        ttk.Label(pre_flight_frame, text="BATT No:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.batt_number = ttk.Entry(pre_flight_frame, width=15)
        self.batt_number.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(pre_flight_frame, text="BATT:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.batt_percentage = ttk.Entry(pre_flight_frame, width=5)
        self.batt_percentage.grid(row=0, column=3, sticky="w", pady=2)
        ttk.Label(pre_flight_frame, text="%").grid(row=0, column=4, sticky="w", pady=2)
        
        self.batt_volts = ttk.Entry(pre_flight_frame, width=5)
        self.batt_volts.grid(row=0, column=5, sticky="w", padx=(10, 0), pady=2)
        ttk.Label(pre_flight_frame, text="Volts").grid(row=0, column=6, sticky="w", pady=2)
        
        # Flight Time section
        time_frame = ttk.LabelFrame(self.scrollable_frame, text="FLIGHT TIME", padding="10")
        time_frame.grid(row=3, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        
        ttk.Label(time_frame, text="START TIME:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.start_time = ttk.Entry(time_frame, width=15)
        self.start_time.grid(row=0, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(time_frame, text="END TIME:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.end_time = ttk.Entry(time_frame, width=15)
        self.end_time.grid(row=0, column=3, sticky="w", padx=5, pady=2)
        
        ttk.Label(time_frame, text="DURATION:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.duration = ttk.Entry(time_frame, width=15)
        self.duration.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        # POST-FLIGHT section
        post_flight_frame = ttk.LabelFrame(self.scrollable_frame, text="POST-FLIGHT", padding="10")
        post_flight_frame.grid(row=4, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        
        ttk.Label(post_flight_frame, text="SAFE LANDING").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.safe_landing = tk.StringVar(value="YES")
        ttk.Radiobutton(post_flight_frame, text="YES", variable=self.safe_landing, value="YES").grid(row=0, column=1, sticky="w", padx=5, pady=2)
        ttk.Radiobutton(post_flight_frame, text="NO", variable=self.safe_landing, value="NO").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        
        # TRAINING section
        training_frame = ttk.LabelFrame(self.scrollable_frame, text="TRAINING", padding="10")
        training_frame.grid(row=5, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        
        ttk.Label(training_frame, text="EXERCISE:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.exercise = ttk.Entry(training_frame, width=30)
        self.exercise.grid(row=0, column=1, columnspan=3, sticky="w", padx=5, pady=2)
        
        ttk.Label(training_frame, text="PILOT 1 NAME:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.pilot1_name = ttk.Entry(training_frame, width=30)
        self.pilot1_name.grid(row=1, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(training_frame, text="PILOT 2 NAME:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.pilot2_name = ttk.Entry(training_frame, width=30)
        self.pilot2_name.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(training_frame, text="SIGN:").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        self.pilot1_sign = ttk.Entry(training_frame, width=20)
        self.pilot1_sign.grid(row=1, column=3, sticky="w", padx=5, pady=2)
        
        ttk.Label(training_frame, text="SIGN 2:").grid(row=2, column=2, sticky="w", padx=5, pady=2)
        self.pilot2_sign = ttk.Entry(training_frame, width=20)
        self.pilot2_sign.grid(row=2, column=3, sticky="w", padx=5, pady=2)
        
        # DEFECTS section
        defects_frame = ttk.LabelFrame(self.scrollable_frame, text="DEFECTS", padding="10")
        defects_frame.grid(row=6, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        
        ttk.Label(defects_frame, text="DEFECTS:").grid(row=0, column=0, sticky="nw", padx=5, pady=2)
        self.defects = tk.Text(defects_frame, width=40, height=4)
        self.defects.grid(row=0, column=1, columnspan=3, sticky="w", padx=5, pady=2)
        
        ttk.Label(defects_frame, text="RECTIFICATION:").grid(row=1, column=0, sticky="nw", padx=5, pady=2)
        self.rectification = tk.Text(defects_frame, width=40, height=4)
        self.rectification.grid(row=1, column=1, columnspan=3, sticky="w", padx=5, pady=2)
        
        ttk.Label(defects_frame, text="TIME:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.defects_time = ttk.Entry(defects_frame, width=15)
        self.defects_time.grid(row=2, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(defects_frame, text="SIGN:").grid(row=2, column=2, sticky="w", padx=5, pady=2)
        self.defects_sign = ttk.Entry(defects_frame, width=15)
        self.defects_sign.grid(row=2, column=3, sticky="w", padx=5, pady=2)
        
        ttk.Label(defects_frame, text="TIME:").grid(row=3, column=0, sticky="w", padx=5, pady=2)
        self.rectification_time = ttk.Entry(defects_frame, width=15)
        self.rectification_time.grid(row=3, column=1, sticky="w", padx=5, pady=2)
        
        ttk.Label(defects_frame, text="SIGN:").grid(row=3, column=2, sticky="w", padx=5, pady=2)
        self.rectification_sign = ttk.Entry(defects_frame, width=15)
        self.rectification_sign.grid(row=3, column=3, sticky="w", padx=5, pady=2)
        
        # REMARKS section
        remarks_frame = ttk.LabelFrame(self.scrollable_frame, text="REMARKS", padding="10")
        remarks_frame.grid(row=7, column=0, columnspan=4, sticky="ew", padx=5, pady=5)
        
        self.remarks = tk.Text(remarks_frame, width=80, height=4)
        self.remarks.pack(padx=5, pady=2)
        
        # Configure column weights to make form responsive
        for i in range(4):
            self.scrollable_frame.columnconfigure(i, weight=1)
            
    def init_csv_file(self):
        # Create CSV file with headers if it doesn't exist
        if not self.csv_file.exists():
            with open(self.csv_file, 'w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "Flight Number", "Date", "Wind (m/s)", "Weather", "Temperature (°C)",
                    "Battery Number", "Battery Percentage", "Battery Volts",
                    "Start Time", "End Time", "Duration", "Safe Landing",
                    "Exercise", "Pilot 1 Name", "Pilot 2 Name", "Pilot 1 Sign", "Pilot 2 Sign",
                    "Defects", "Rectification", "Defects Time", "Defects Sign", 
                    "Rectification Time", "Rectification Sign", "Remarks"
                ])
                
    def save_entry(self):
        # Validate required fields
        if not self.flight_number.get():
            messagebox.showerror("Error", "Flight Number is required!")
            return
            
        # Get all values from form
        entry_data = {
            "Flight Number": self.flight_number.get(),
            "Date": self.date.get(),
            "Wind (m/s)": self.wind.get(),
            "Weather": self.weather.get(),
            "Temperature (°C)": self.temperature.get(),
            "Battery Number": self.batt_number.get(),
            "Battery Percentage": self.batt_percentage.get(),
            "Battery Volts": self.batt_volts.get(),
            "Start Time": self.start_time.get(),
            "End Time": self.end_time.get(),
            "Duration": self.duration.get(),
            "Safe Landing": self.safe_landing.get(),
            "Exercise": self.exercise.get(),
            "Pilot 1 Name": self.pilot1_name.get(),
            "Pilot 2 Name": self.pilot2_name.get(),
            "Pilot 1 Sign": self.pilot1_sign.get(),
            "Pilot 2 Sign": self.pilot2_sign.get(),
            "Defects": self.defects.get("1.0", tk.END).strip(),
            "Rectification": self.rectification.get("1.0", tk.END).strip(),
            "Defects Time": self.defects_time.get(),
            "Defects Sign": self.defects_sign.get(),
            "Rectification Time": self.rectification_time.get(),
            "Rectification Sign": self.rectification_sign.get(),
            "Remarks": self.remarks.get("1.0", tk.END).strip()
        }
        
        # Save to CSV
        with open(self.csv_file, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(entry_data.values())
            
        messagebox.showinfo("Success", f"Flight log entry saved successfully to:\n{self.csv_file}")
        
    def clear_form(self):
        # Clear all fields
        self.flight_number.delete(0, tk.END)
        self.date.delete(0, tk.END)
        self.date.insert(0, datetime.now().strftime("%d/%m/%Y"))
        self.wind.delete(0, tk.END)
        self.weather.delete(0, tk.END)
        self.temperature.delete(0, tk.END)
        self.batt_number.delete(0, tk.END)
        self.batt_percentage.delete(0, tk.END)
        self.batt_volts.delete(0, tk.END)
        self.start_time.delete(0, tk.END)
        self.end_time.delete(0, tk.END)
        self.duration.delete(0, tk.END)
        self.safe_landing.set("YES")
        self.exercise.delete(0, tk.END)
        self.pilot1_name.delete(0, tk.END)
        self.pilot2_name.delete(0, tk.END)
        self.pilot1_sign.delete(0, tk.END)
        self.pilot2_sign.delete(0, tk.END)
        self.defects.delete("1.0", tk.END)
        self.rectification.delete("1.0", tk.END)
        self.defects_time.delete(0, tk.END)
        self.defects_sign.delete(0, tk.END)
        self.rectification_time.delete(0, tk.END)
        self.rectification_sign.delete(0, tk.END)
        self.remarks.delete("1.0", tk.END)
        
    def export_to_csv(self):
        # Allow user to save to a different location
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            initialdir=self.desktop_path,
            title="Save Flight Logs As"
        )
        
        if file_path:
            # Copy the existing CSV to the new location
            import shutil
            shutil.copy2(self.csv_file, file_path)
            messagebox.showinfo("Success", f"Flight logs exported to:\n{file_path}")
            
    def open_csv(self):
        # Open the CSV file with the default application
        try:
            os.startfile(self.csv_file)  # Windows
        except AttributeError:
            try:
                # macOS and Linux
                import subprocess
                subprocess.call(['open', str(self.csv_file)])
            except:
                messagebox.showinfo("Open CSV", f"CSV file location:\n{self.csv_file}")

if __name__ == "__main__":
    root = tk.Tk()
    app = FlightLogGUI(root)
    root.mainloop()