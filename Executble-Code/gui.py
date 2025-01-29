import tkinter as tk, json
from tkinter import ttk, filedialog
from applyZoningStorageFunc import applyZoningStorageFunc, actualBinAllocation
from threading import Thread


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





class ConfigWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("DataFile Config")
        self.root.geometry("500x450")
        self.root.wm_attributes('-topmost', True)
        
        self.config_frame = tk.Frame(self.root)#, width=200, height=200)
        self.config_frame.pack(pady=20, padx=10)
        self.var_dict = {}

        # Dimensions File
        self.dimensions_label = tk.Label(self.config_frame, text="Main Parts (GParts) File:", font=("Helvetica", 11, "bold"))
        self.dimensions_label.grid(row=0, column=0, sticky=tk.W)
        self.dimensions_frame = tk.Frame(self.config_frame)
        self.dimensions_frame.grid(row=1, column=0)

        # Sold File 1
        self.sold_file_1_label = tk.Label(self.config_frame, text="Wholesale File:", font=("Helvetica", 11, "bold"))
        self.sold_file_1_label.grid(row=2, column=0, sticky=tk.W, pady=(20,0))
        # self.open_button_1 = ttk.Label(self.config_frame, text="▼")
        # self.open_button_1.grid(row=2, column=2)
        self.sold_file_1_frame = tk.Frame(self.config_frame)
        self.sold_file_1_frame.grid(row=3, column=0)#, columnspan=3)

        # Sold File 2
        self.sold_file_2_label = tk.Label(self.config_frame, text="Service File:", font=("Helvetica", 11, "bold"))
        self.sold_file_2_label.grid(row=4, column=0, sticky=tk.W, pady=(20,0))
        self.sold_file_2_frame = tk.Frame(self.config_frame)
        self.sold_file_2_frame.grid(row=5, column=0)

        # Inventory File
        self.inventory_label = tk.Label(self.config_frame, text="Inventory (CounterPad) File:", font=("Helvetica", 11, "bold"))
        self.inventory_label.grid(row=6, column=0, sticky=tk.W, pady=(20,0))
        self.inventory_frame = tk.Frame(self.config_frame)
        self.inventory_frame.grid(row=7, column=0)

        # Drop 0 Dimension Parts
        # self.drop_0_label = tk.Label(self.config_frame, text="Drop 0 Dimension Parts")
        # self.drop_0_label.grid(row=8, column=0, columnspan=2)
        # self.drop_0_var = tk.BooleanVar(value=False)
        # self.drop_0_checkbox = ttk.Checkbutton(self.config_frame, variable=self.drop_0_var)
        # self.drop_0_checkbox.grid(row=8, column=2)

        self.show_options("Dimensions", 1, "File Path") # , "Vendor Column", "Width Column", "Height Column", "Depth Column", "Part# Column", "Desc. Column")
        self.show_options("Wholesale", 3, "File Path") # , "Vendor Column", "Sold Column", "Part# Column")
        self.show_options("Service", 5, "File Path") # , "Vendor Column", "Sold Column", "Part# Column")
        self.show_options("Inventory", 7, "File Path") # , "Vendor Column", "Inventory Column", "Bin Column", "Part# Column")

        
        tk.Button(self.config_frame, text="   Apply Changes   ", command=self.apply_changes, font=("Segoe UI Emoji", 10, "bold")).grid(row=8, column=0, pady=(20,0))
        tk.Button(self.config_frame, text="     Cancel     ", command=self.root.destroy, font=("Segoe UI Emoji", 10, "bold")).grid(row=8, column=1, pady=(20,0))

    def apply_changes(self):
        globals()['config'] = {'Dimensions Config': {
                        'File Path': self.var_dict["Dimensions"]["File Path"].get(),
                        'Columns': {
                            'Part# Column':  "Part#", # self.var_dict["Dimensions"]['Part# Column'].get(),
                            'Desc. Column': "Part Desc.", # self.var_dict["Dimensions"
                            'Vendor Column': "Vendor", #  self.var_dict["Dimensions"]["Vendor Column"].get(),
                            'Width Column':  "Width", # self.var_dict["Dimensions"]["Width Column"].get(),
                            'Height Column': "Height", #  self.var_dict["Dimensions"]["Height Column"].get(),
                            'Depth Column':  "Depth"# self.var_dict["Dimensions"]["Depth Column"].get()
                        }
                        },
                 'Sold File 1 Config': {
                        'File Path': self.var_dict["Wholesale"]["File Path"].get(),
                        'Columns': {
                            'Part# Column': "Part#", # self.var_dict["Sold File 1"]['Part# Column'].get(),
                            'Vendor Column': "Vendor", # self.var_dict["Sold File 1"]["Vendor Column"].get(),
                            'Sold Column': "Sold" # self.var_dict["Sold File 1"]["Sold Column"].get()
                        }
                        },
                 'Sold File 2 Config': {
                        'File Path': self.var_dict["Service"]["File Path"].get(),
                        'Columns': {
                            'Part# Column': "Part#", # self.var_dict["Sold File 2"]['Part# Column'].get(),
                            'Vendor Column': "Vendor", # self.var_dict["Sold File 2"]["Vendor Column"].get(),
                            'Sold Column': "Sold" # self.var_dict["Sold File 2"]["Sold Column"].get()
                        }
                        },
                 'Inventory Config': {
                        'File Path': self.var_dict["Inventory"]["File Path"].get(),
                        'Columns': {
                            'Part# Column': "Part#", # self.var_dict["Inventory"]['Part# Column'].get(),
                            'Vendor Column': "Vendor", # self.var_dict["Inventory"]["Vendor Column"].get(),
                            'Inventory Column': "OH", # self.var_dict["Inventory"]["Inventory Column"].get(),
                            'Bin Column': 'Bin' # self.var_dict["Inventory"]["Bin Column"].get(),
                        }
                        },
                 'Drop 0 Dimensions': 'false'#str(self.drop_0_var.get()).lower()
                 }
        
        with open('conf.txt', 'w') as conf:
            conf.write(str(globals()['config']))
        

    def show_options(self, title, row, *options):
        options_frame = tk.Frame(self.config_frame)
        options_frame.grid(row=row, column=0, columnspan=3)

        if title not in self.var_dict:
            self.var_dict[title] = {}

        # tk.Label(options_frame, text=title).grid(row=0, column=0, columnspan=len(options))

        for i, option in enumerate(options):
            var = tk.StringVar()
            label = tk.Label(options_frame, text=option)
            label.grid(row=i+1, column=0)
            entry = ttk.Entry(options_frame, textvariable=var, width="50")
            entry.grid(row=i+1, column=1)
            if option == "File Path": 
                button = ttk.Button(options_frame, text="Browse", command=lambda t=title, o=option: self.browse_file(t, o))
                button.grid(row=i+1, column=3)
            self.var_dict[title][option] = entry

    def browse_file(self, title, option):
        self.root.wm_attributes('-topmost', False)
        filepath = filedialog.askopenfilename(title=f"Select {title} file", filetypes=[('Excel Files', '*.xlsx *.xls')])
        if filepath:
            self.var_dict[title][option].delete("1", tk.END)
            self.var_dict[title][option].insert(tk.END, filepath)
        self.root.wm_attributes("-topmost", True)

    def run(self):
        self.root.mainloop()



class MainGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stockmap GUI")
        self.title_label = tk.Label(self.root, text="Stockmap GUI", font=("Helvetica", 20, "bold"), fg="#0066cc")
        self.title_label.pack(pady=20)  # Add some padding around the label
        self.aSZDone = False
        self.df_Main = None
        self.buttons = {}

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)
        self.buttons['config'] = tk.Button(self.button_frame, text=" Set DataFile Path ", font=("Helvetica", 11, "bold"), command=self.open_config_window)#, state="disabled")
        self.buttons['config'].pack(side=tk.LEFT, padx=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)
        self.buttons['apply'] = tk.Button(self.button_frame, text=" Apply Zone and Storage ", font=("Helvetica", 11, "bold"), command=self.aSZ)
        self.buttons['apply'].pack(side=tk.LEFT, padx=10)

        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)
        self.buttons['allocation'] = tk.Button(self.button_frame, text=" Actual Bin Allocation ", font=("Helvetica", 11, "bold"), command=self.aBA)
        self.buttons['allocation'].pack(side=tk.LEFT, padx=10)
            
        self.button_frame = tk.Frame(self.root)
        self.button_frame.pack(pady=20)
        self.closeButton = tk.Button(self.button_frame, text=" Close ", font=("Helvetica", 11, "bold"), command=self.close)
        self.closeButton.pack(side=tk.LEFT, padx=10)

        self.log_label = tk.Label(self.root, text="Log (Info / Error):", font=("Helvetica", 11, "bold"))
        self.log_label.pack(pady=20)
        self.log_text = tk.Text(self.root, height=15, width=100, font=('Segoe UI Emoji', 10))
        self.log_text.pack()

        self.progress_text = tk.Text(self.root, height=1, width=100, font=('Segoe UI Emoji', 10))
        self.progress_text.pack()


        try:
            globals()['config'] = {}
            with open('conf.txt') as conf:
                globals()['config'] = string_to_json(conf.read())

            self.root.protocol("WM_DELETE_WINDOW", self.close)
        except Exception as e:
            self.log_text.insert(tk.END, e)


    def disable_all_buttons(self):
        for button in self.buttons.values():
            button.config(state="disabled")

    def enable_all_buttons(self):
        for button in self.buttons.values():
            button.config(state="active")

    def open_config_window(self):
        self.config_window = ConfigWindow()

    def close(self):
        try:
            self.config_window.root.destroy()
            self.root.destroy()
        except:
            self.root.destroy()



    def aSZ(self):
        self.disable_all_buttons()
        self.thread = Thread(target=self.aSZMain)
        self.thread.daemon = True
        self.thread.start()

    def aSZMain(self):
        self.log_text.insert(tk.END, "Process Started... Reading Files... \n")
        generator = applyZoningStorageFunc(globals()['config'])
        while True:
            try:
                message = next(generator)
                if message[0] == "Return": self.df_Main = message[1]; continue
                if "Completion:" in message:
                    self.progress_text.insert(tk.END, '\n' + message)
                    self.progress_text.see(tk.END)
                    continue
                self.log_text.insert(tk.END, message + '\n')
                self.log_text.see(tk.END)
            except StopIteration:
                break
            except Exception as e:
                self.log_text.insert(tk.END, e)
                self.log_text.see(tk.END)
            self.aSZDone = True
        
        # After the process is complete, re-enable the button
        self.root.after(0, self.enable_all_buttons)
   
        
    def aBA(self):
        if not self.aSZDone: self.log_text.insert(tk.END, "Please first run - Apply Zone and Storage Button\n"); return
        self.thread = Thread(target=self.aBAMain)
        self.thread.daemon = True
        self.thread.start()

    def aBAMain(self):
        self.log_text.insert(tk.END, "Process Started... Reading Bins Data... \n")
        generator = actualBinAllocation(self.df_Main)
        while True:
            try:
                message = next(generator)
                if "Completion:" in message:
                    self.progress_text.insert(tk.END, '\n' + message)
                    self.progress_text.see(tk.END)
                    continue
                self.log_text.insert(tk.END, message + '\n')
                self.log_text.see(tk.END)
            except StopIteration:
                break
            except Exception as e:
                self.log_text.insert(tk.END, e)
                self.log_text.see(tk.END)
        self.thread.terminate()


    def run(self):
        self.root.mainloop()



if __name__ == "__main__":
    main_gui = MainGUI()
    main_gui.run()