import tkinter as tk
from tkinter import ttk
from applyZoningStorageFunc import applyZoningStorageFunc
import json

def string_to_json(config_str):
    try:
        # Try parsing as JSON first
        config_str = config_str.replace("'", '"')
        config_dict = json.loads(config_str)
        return config_dict
    except json.JSONDecodeError:
        # If JSON decoding fails, fall back to eval
        config_str = config_str.strip().strip('{}').rstrip(',')
        config_str = config_str.replace("'", '"')
        config_str = config_str.replace('\\n', '\\\\n')
        config_dict = eval(config_str)
        return config_dict

config = {}
with open('conf.txt') as conf:
    config = string_to_json(conf.read())



class ConfigWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Config Window")
        
        self.config_frame = tk.Frame(self.root)
        self.config_frame.pack(pady=20, padx=10)
        self.var_dict = {}

        # Dimensions File
        self.dimensions_label = tk.Label(self.config_frame, text="Dimensions File")
        self.dimensions_label.grid(row=0, column=0, columnspan=2)
        self.open_button = ttk.Button(self.config_frame, text="▼", command=self.open_dimensions_options)
        self.open_button.grid(row=0, column=2)
        self.dimensions_frame = tk.Frame(self.config_frame)
        self.dimensions_frame.grid(row=1, column=0, columnspan=3)

        # Sold File 1
        self.sold_file_1_label = tk.Label(self.config_frame, text="Sold File 1")
        self.sold_file_1_label.grid(row=2, column=0, columnspan=2)
        self.open_button_1 = ttk.Button(self.config_frame, text="▼", command=self.open_sold_file_options_1)
        self.open_button_1.grid(row=2, column=2)
        self.sold_file_1_frame = tk.Frame(self.config_frame)
        self.sold_file_1_frame.grid(row=3, column=0, columnspan=3)

        # Sold File 2
        self.sold_file_2_label = tk.Label(self.config_frame, text="Sold File 2")
        self.sold_file_2_label.grid(row=4, column=0, columnspan=2)
        self.open_button_2 = ttk.Button(self.config_frame, text="▼", command=self.open_sold_file_options_2)
        self.open_button_2.grid(row=4, column=2)
        self.sold_file_2_frame = tk.Frame(self.config_frame)
        self.sold_file_2_frame.grid(row=5, column=0, columnspan=3)

        # Inventory File
        self.inventory_label = tk.Label(self.config_frame, text="Inventory File")
        self.inventory_label.grid(row=6, column=0, columnspan=2)
        self.open_button_inventory = ttk.Button(self.config_frame, text="▼", command=self.open_inventory_options)
        self.open_button_inventory.grid(row=6, column=2)
        self.inventory_frame = tk.Frame(self.config_frame)
        self.inventory_frame.grid(row=7, column=0, columnspan=3)

        # Drop 0 Dimension Parts
        self.drop_0_label = tk.Label(self.config_frame, text="Drop 0 Dimension Parts")
        self.drop_0_label.grid(row=8, column=0, columnspan=2)
        self.drop_0_var = tk.BooleanVar(value=False)
        self.drop_0_checkbox = ttk.Checkbutton(self.config_frame, variable=self.drop_0_var)
        self.drop_0_checkbox.grid(row=8, column=2)

        self.show_options("Dimensions",1 , "Path", "Vendor Column", "Width Column", "Height Column", "Depth Column", "Part# Column", "Desc. Column")
        self.show_options("Sold File 1",3 , "Path", "Vendor Column", "Sold Column", "Part# Column")
        self.show_options("Sold File 2",5 , "Path", "Vendor Column", "Sold Column", "Part# Column")
        self.show_options("Inventory",7 , "Path", "Vendor Column", "Inventory Column", "Bin Column", "Part# Column")

        
        tk.Button(self.config_frame, text="Apply Changes", command=self.apply_changes).grid(row=100, column=0, columnspan=2)

    def apply_changes(self):
        config = {'Dimensions Config': {
                        'File Path': self.var_dict["Dimensions"]["Path"].get(),
                        'Columns': {
                            'Part# Column': self.var_dict["Dimensions"]['Part# Column'].get(),
                            'Vendor Column': self.var_dict["Dimensions"]["Vendor Column"].get(),
                            'Width Column': self.var_dict["Dimensions"]["Width Column"].get(),
                            'Height Column': self.var_dict["Dimensions"]["Height Column"].get(),
                            'Depth Column': self.var_dict["Dimensions"]["Depth Column"].get()
                        }
                        },
                 'Sold File 1 Config': {
                        'File Path': self.var_dict["Sold File 1"]["Path"].get(),
                        'Columns': {
                            'Part# Column': self.var_dict["Sold File 1"]['Part# Column'].get(),
                            'Vendor Column': self.var_dict["Sold File 1"]["Vendor Column"].get(),
                            'Sold Column': self.var_dict["Sold File 1"]["Sold Column"].get()
                        }
                        },
                 'Sold File 2 Config': {
                        'File Path': self.var_dict["Sold File 2"]["Path"].get(),
                        'Columns': {
                            'Part# Column': self.var_dict["Sold File 2"]['Part# Column'].get(),
                            'Vendor Column': self.var_dict["Sold File 2"]["Vendor Column"].get(),
                            'Sold Column': self.var_dict["Sold File 2"]["Sold Column"].get()
                        }
                        },
                 'Inventory Config': {
                        'File Path': self.var_dict["Inventory"]["Path"].get(),
                        'Columns': {
                            'Part# Column': self.var_dict["Inventory"]['Part# Column'].get(),
                            'Vendor Column': self.var_dict["Inventory"]["Vendor Column"].get(),
                            'Inventory Column': self.var_dict["Inventory"]["Inventory Column"].get(),
                            'Bin Column': self.var_dict["Inventory"]["Bin Column"].get(),
                        }
                        },
                 'Drop 0 Dimensions': self.drop_0_var.get()
                 }
        with open('conf.txt', 'w') as conf:
            conf.write(str(config))
        

    def open_dimensions_options(self):
        self.show_options("Dimensions",1 , "Path", "Vendor Column", "Width Column", "Height Column", "Depth Column", "Part# Column", "Desc. Column")

    def open_sold_file_options_1(self):
        self.show_options("Sold File 1",3 , "Path", "Vendor Column", "Sold Column", "Part# Column")

    def open_sold_file_options_2(self):
        self.show_options("Sold File 2",5 , "Path", "Vendor Column", "Sold Column", "Part# Column")

    def open_inventory_options(self):
        self.show_options("Inventory",7 , "Path", "Vendor Column", "Inventory Column", "Bin Column", "Part# Column")

    def show_options(self, title, row, *options):
        options_frame = tk.Frame(self.config_frame)
        options_frame.grid(row=row, column=0, columnspan=3)

        if title not in self.var_dict:
            self.var_dict[title] = {}

        tk.Label(options_frame, text=title).grid(row=0, column=0, columnspan=len(options))

        for i, option in enumerate(options):
            var = tk.StringVar()
            label = tk.Label(options_frame, text=option)
            label.grid(row=i+1, column=0)
            entry = ttk.Entry(options_frame, textvariable=var)
            entry.grid(row=i+1, column=1)
            self.var_dict[title][option] = entry

    def run(self):
        self.root.mainloop()




class MainGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Main Window")
        
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        self.open_button = tk.Button(self.button_frame, text="Open Config Window", command=self.open_config_window)
        self.open_button.pack(side=tk.LEFT, padx=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)

        self.open_button = tk.Button(self.button_frame, text="Apply Zone and Storage", command=applyZoningStorageFunc(config))
        self.open_button.pack(side=tk.LEFT, padx=10)

        self.log_label = tk.Label(self.root, text="Log:")
        self.log_label.pack(pady=20)

        self.log_text = tk.Text(self.root, height=10)
        self.log_text.pack()

    def open_config_window(self):
        ConfigWindow()

    def log_message(self, message):
        self.log_text.insert(tk.END, message + '\n')
        self.log_text.see(tk.END)
        self.root.after(100)  # Scroll to bottom after adding new log


    def run(self):
        self.root.mainloop()



if __name__ == "__main__":
    main_gui = MainGUI()
    main_gui.run()