import tkinter as tk
from tkinter import ttk, messagebox
import math
import json
import os
from datetime import datetime

class SmartCalculator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🧮 Smart Calculator - Everything In One - by saunue")
        self.root.geometry("800x600")
        self.root.resizable(True, True)
        
        # Variables
        self.display_var = tk.StringVar(value="0")
        self.current_input = ""
        self.history = []
        self.is_dark_mode = False
        
        # Colors
        self.light_colors = {
            'bg': '#f0f0f0',
            'button_bg': '#ffffff',
            'button_active': '#e1e1e1',
            'text': '#000000',
            'accent': '#0078d4'
        }
        
        self.dark_colors = {
            'bg': '#2b2b2b',
            'button_bg': '#404040',
            'button_active': '#555555',
            'text': '#ffffff',
            'accent': '#0078d4'
        }
        
        self.colors = self.light_colors
        
        # Load history
        self.load_history()
        
        # Create GUI
        self.create_widgets()
        self.apply_theme()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Notebook for tabs
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Tab 1: Calculator
        self.calc_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.calc_frame, text="🧮 Calculator")
        
        # Tab 2: Unit Converter
        self.converter_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.converter_frame, text="🔄 Conversion")
        
        # Tab 3: History
        self.history_frame = ttk.Frame(self.notebook)
        self.notebook.add(self.history_frame, text="📝 History")
        
        self.create_calculator_tab()
        self.create_converter_tab()
        self.create_history_tab()
        
    def create_calculator_tab(self):
        # Top frame for theme toggle
        top_frame = tk.Frame(self.calc_frame)
        top_frame.pack(fill=tk.X, pady=(0, 10))
        
        theme_btn = tk.Button(top_frame, text="🌙 Dark Mode", 
                             command=self.toggle_theme,
                             font=('Arial', 10))
        theme_btn.pack(side=tk.RIGHT)
        
        # Display frame
        display_frame = tk.Frame(self.calc_frame)
        display_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Display
        self.display = tk.Entry(display_frame, textvariable=self.display_var,
                               font=('Arial', 20), justify='right',
                               state='readonly', bd=2, relief='sunken')
        self.display.pack(fill=tk.X, ipady=10)
        
        # Buttons frame
        buttons_frame = tk.Frame(self.calc_frame)
        buttons_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scientific buttons (top row)
        sci_frame = tk.Frame(buttons_frame)
        sci_frame.pack(fill=tk.X, pady=(0, 5))
        
        sci_buttons = [
            ('sin', lambda: self.scientific_operation('sin')),
            ('cos', lambda: self.scientific_operation('cos')),
            ('tan', lambda: self.scientific_operation('tan')),
            ('log', lambda: self.scientific_operation('log')),
            ('ln', lambda: self.scientific_operation('ln')),
            ('√', lambda: self.scientific_operation('sqrt')),
            ('x²', lambda: self.scientific_operation('square')),
            ('π', lambda: self.insert_number(str(math.pi))),
        ]
        
        for i, (text, command) in enumerate(sci_buttons):
            btn = tk.Button(sci_frame, text=text, command=command,
                           font=('Arial', 10), width=8, height=2)
            btn.grid(row=0, column=i, padx=2, pady=2, sticky='nsew')
            sci_frame.grid_columnconfigure(i, weight=1)
        
        # Main calculator buttons
        calc_frame = tk.Frame(buttons_frame)
        calc_frame.pack(fill=tk.BOTH, expand=True)
        
        # Button layout
        button_layout = [
            [('C', self.clear), ('CE', self.clear_entry), ('⌫', self.backspace), ('÷', lambda: self.insert_operator('/'))],
            [('7', lambda: self.insert_number('7')), ('8', lambda: self.insert_number('8')), ('9', lambda: self.insert_number('9')), ('×', lambda: self.insert_operator('*'))],
            [('4', lambda: self.insert_number('4')), ('5', lambda: self.insert_number('5')), ('6', lambda: self.insert_number('6')), ('-', lambda: self.insert_operator('-'))],
            [('1', lambda: self.insert_number('1')), ('2', lambda: self.insert_number('2')), ('3', lambda: self.insert_number('3')), ('+', lambda: self.insert_operator('+'))],
            [('±', self.toggle_sign), ('0', lambda: self.insert_number('0')), ('.', lambda: self.insert_number('.')), ('=', self.calculate)]
        ]
        
        for row, buttons in enumerate(button_layout):
            for col, (text, command) in enumerate(buttons):
                btn = tk.Button(calc_frame, text=text, command=command,
                               font=('Arial', 14), width=8, height=3)
                btn.grid(row=row, column=col, padx=2, pady=2, sticky='nsew')
                
        # Configure grid weights
        for i in range(5):
            calc_frame.grid_rowconfigure(i, weight=1)
        for i in range(4):
            calc_frame.grid_columnconfigure(i, weight=1)
    
    def create_converter_tab(self):
        # Temperature Converter
        temp_frame = tk.LabelFrame(self.converter_frame, text="🌡️ Temperature conversion", 
                                  font=('Arial', 12, 'bold'), padx=10, pady=10)
        temp_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(temp_frame, text="Celsius:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.celsius_var = tk.StringVar()
        celsius_entry = tk.Entry(temp_frame, textvariable=self.celsius_var, font=('Arial', 10))
        celsius_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        celsius_entry.bind('<KeyRelease>', self.convert_temperature)
        
        tk.Label(temp_frame, text="Fahrenheit:", font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.fahrenheit_var = tk.StringVar()
        fahrenheit_entry = tk.Entry(temp_frame, textvariable=self.fahrenheit_var, font=('Arial', 10))
        fahrenheit_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        fahrenheit_entry.bind('<KeyRelease>', self.convert_temperature)
        
        tk.Label(temp_frame, text="Kelvin:", font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=5)
        self.kelvin_var = tk.StringVar()
        kelvin_entry = tk.Entry(temp_frame, textvariable=self.kelvin_var, font=('Arial', 10))
        kelvin_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        kelvin_entry.bind('<KeyRelease>', self.convert_temperature)
        
        temp_frame.grid_columnconfigure(1, weight=1)
        
        # Length Converter
        length_frame = tk.LabelFrame(self.converter_frame, text="📏 Lenght conversion",
                                   font=('Arial', 12, 'bold'), padx=10, pady=10)
        length_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(length_frame, text="Met:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.meter_var = tk.StringVar()
        meter_entry = tk.Entry(length_frame, textvariable=self.meter_var, font=('Arial', 10))
        meter_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        meter_entry.bind('<KeyRelease>', self.convert_length)
        
        tk.Label(length_frame, text="Centimet:", font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.cm_var = tk.StringVar()
        cm_entry = tk.Entry(length_frame, textvariable=self.cm_var, font=('Arial', 10))
        cm_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        cm_entry.bind('<KeyRelease>', self.convert_length)
        
        tk.Label(length_frame, text="Inch:", font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=5)
        self.inch_var = tk.StringVar()
        inch_entry = tk.Entry(length_frame, textvariable=self.inch_var, font=('Arial', 10))
        inch_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        inch_entry.bind('<KeyRelease>', self.convert_length)
        
        tk.Label(length_frame, text="Feet:", font=('Arial', 10)).grid(row=3, column=0, sticky='w', pady=5)
        self.feet_var = tk.StringVar()
        feet_entry = tk.Entry(length_frame, textvariable=self.feet_var, font=('Arial', 10))
        feet_entry.grid(row=3, column=1, padx=5, pady=5, sticky='ew')
        feet_entry.bind('<KeyRelease>', self.convert_length)
        
        length_frame.grid_columnconfigure(1, weight=1)
        
        # Weight Converter
        weight_frame = tk.LabelFrame(self.converter_frame, text="⚖️ Weight conversion",
                                   font=('Arial', 12, 'bold'), padx=10, pady=10)
        weight_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(weight_frame, text="Kilogram:", font=('Arial', 10)).grid(row=0, column=0, sticky='w', pady=5)
        self.kg_var = tk.StringVar()
        kg_entry = tk.Entry(weight_frame, textvariable=self.kg_var, font=('Arial', 10))
        kg_entry.grid(row=0, column=1, padx=5, pady=5, sticky='ew')
        kg_entry.bind('<KeyRelease>', self.convert_weight)
        
        tk.Label(weight_frame, text="Gram:", font=('Arial', 10)).grid(row=1, column=0, sticky='w', pady=5)
        self.gram_var = tk.StringVar()
        gram_entry = tk.Entry(weight_frame, textvariable=self.gram_var, font=('Arial', 10))
        gram_entry.grid(row=1, column=1, padx=5, pady=5, sticky='ew')
        gram_entry.bind('<KeyRelease>', self.convert_weight)
        
        tk.Label(weight_frame, text="Pound:", font=('Arial', 10)).grid(row=2, column=0, sticky='w', pady=5)
        self.pound_var = tk.StringVar()
        pound_entry = tk.Entry(weight_frame, textvariable=self.pound_var, font=('Arial', 10))
        pound_entry.grid(row=2, column=1, padx=5, pady=5, sticky='ew')
        pound_entry.bind('<KeyRelease>', self.convert_weight)
        
        weight_frame.grid_columnconfigure(1, weight=1)
    
    def create_history_tab(self):
        # History controls
        controls_frame = tk.Frame(self.history_frame)
        controls_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(controls_frame, text="🗑️ Delete history", 
                 command=self.clear_history, font=('Arial', 10)).pack(side=tk.LEFT)
        
        tk.Button(controls_frame, text="💾 Save history", 
                 command=self.save_history, font=('Arial', 10)).pack(side=tk.LEFT, padx=10)
        
        # History listbox with scrollbar
        history_list_frame = tk.Frame(self.history_frame)
        history_list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(history_list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.history_listbox = tk.Listbox(history_list_frame, yscrollcommand=scrollbar.set,
                                         font=('Courier', 10))
        self.history_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.history_listbox.yview)
        
        # Double click to use history item
        self.history_listbox.bind('<Double-1>', self.use_history_item)
        
        self.update_history_display()
    
    def insert_number(self, number):
        if self.display_var.get() == "0" or self.display_var.get() == "Error":
            self.current_input = number
        else:
            self.current_input += number
        self.display_var.set(self.current_input)
    
    def insert_operator(self, operator):
        if self.current_input and self.current_input[-1] not in "+-*/":
            self.current_input += operator
            self.display_var.set(self.current_input)
    
    def clear(self):
        self.current_input = ""
        self.display_var.set("0")
    
    def clear_entry(self):
        if self.current_input:
            self.current_input = self.current_input[:-1]
            if not self.current_input:
                self.display_var.set("0")
            else:
                self.display_var.set(self.current_input)
    
    def backspace(self):
        self.clear_entry()
    
    def toggle_sign(self):
        if self.current_input and self.current_input != "0":
            if self.current_input.startswith('-'):
                self.current_input = self.current_input[1:]
            else:
                self.current_input = '-' + self.current_input
            self.display_var.set(self.current_input)
    
    def calculate(self):
        try:
            if self.current_input:
                # Replace display operators with Python operators
                expression = self.current_input.replace('×', '*').replace('÷', '/')
                result = eval(expression)
                
                # Add to history
                timestamp = datetime.now().strftime("%H:%M:%S")
                history_item = f"[{timestamp}] {self.current_input} = {result}"
                self.history.append(history_item)
                
                # Update display
                self.current_input = str(result)
                self.display_var.set(self.current_input)
                
                # Update history display
                self.update_history_display()
                
        except Exception as e:
            self.display_var.set("Error")
            self.current_input = ""
    
    def scientific_operation(self, operation):
        try:
            if self.current_input:
                value = float(self.current_input)
                
                if operation == 'sin':
                    result = math.sin(math.radians(value))
                elif operation == 'cos':
                    result = math.cos(math.radians(value))
                elif operation == 'tan':
                    result = math.tan(math.radians(value))
                elif operation == 'log':
                    result = math.log10(value)
                elif operation == 'ln':
                    result = math.log(value)
                elif operation == 'sqrt':
                    result = math.sqrt(value)
                elif operation == 'square':
                    result = value ** 2
                
                # Add to history
                timestamp = datetime.now().strftime("%H:%M:%S")
                history_item = f"[{timestamp}] {operation}({value}) = {result}"
                self.history.append(history_item)
                
                # Update display
                self.current_input = str(result)
                self.display_var.set(self.current_input)
                
                # Update history display
                self.update_history_display()
                
        except Exception as e:
            self.display_var.set("Error")
            self.current_input = ""
    
    def convert_temperature(self, event=None):
        try:
            widget = event.widget
            value = float(widget.get())
            
            if widget == self.celsius_var.get():  # From Celsius
                fahrenheit = (value * 9/5) + 32
                kelvin = value + 273.15
                self.fahrenheit_var.set(f"{fahrenheit:.2f}")
                self.kelvin_var.set(f"{kelvin:.2f}")
            
        except (ValueError, AttributeError):
            pass
    
    def convert_length(self, event=None):
        try:
            widget = event.widget
            value = float(widget.get())
            
            # Convert based on which field was changed
            # This is a simplified version - you can expand it
            
        except (ValueError, AttributeError):
            pass
    
    def convert_weight(self, event=None):
        try:
            widget = event.widget
            value = float(widget.get())
            
            # Convert based on which field was changed
            # This is a simplified version - you can expand it
            
        except (ValueError, AttributeError):
            pass
    
    def update_history_display(self):
        self.history_listbox.delete(0, tk.END)
        for item in reversed(self.history[-50:]):  # Show last 50 items
            self.history_listbox.insert(0, item)
    
    def use_history_item(self, event):
        selection = self.history_listbox.curselection()
        if selection:
            item = self.history_listbox.get(selection[0])
            # Extract the calculation part
            if "] " in item and " = " in item:
                calc_part = item.split("] ")[1].split(" = ")[0]
                self.current_input = calc_part
                self.display_var.set(calc_part)
    
    def clear_history(self):
        if messagebox.askyesno("Confirm", "Are you sure to delete all history?"):
            self.history.clear()
            self.update_history_display()
            self.save_history()
    
    def save_history(self):
        try:
            with open('calculator_history.json', 'w', encoding='utf-8') as f:
                json.dump(self.history, f, ensure_ascii=False, indent=2)
            messagebox.showinfo("Success", "History saved!")
        except Exception as e:
            messagebox.showerror("Error", f"Can not save history: {e}")
    
    def load_history(self):
        try:
            if os.path.exists('calculator_history.json'):
                with open('calculator_history.json', 'r', encoding='utf-8') as f:
                    self.history = json.load(f)
        except Exception as e:
            self.history = []
    
    def toggle_theme(self):
        self.is_dark_mode = not self.is_dark_mode
        self.colors = self.dark_colors if self.is_dark_mode else self.light_colors
        self.apply_theme()
    
    def apply_theme(self):
        # Update root background
        self.root.configure(bg=self.colors['bg'])
        
        # Update all frames and widgets recursively
        self.update_widget_colors(self.root)
    
    def update_widget_colors(self, widget):
        widget_class = widget.winfo_class()
        
        if widget_class in ['Frame', 'Toplevel']:
            widget.configure(bg=self.colors['bg'])
        elif widget_class == 'Button':
            widget.configure(bg=self.colors['button_bg'], 
                           fg=self.colors['text'],
                           activebackground=self.colors['button_active'])
        elif widget_class in ['Label', 'Entry']:
            widget.configure(bg=self.colors['button_bg'], 
                           fg=self.colors['text'])
        
        # Recursively update children
        for child in widget.winfo_children():
            self.update_widget_colors(child)
    
    def run(self):
        # Keyboard bindings
        self.root.bind('<Return>', lambda e: self.calculate())
        self.root.bind('<KP_Enter>', lambda e: self.calculate())
        self.root.bind('<Escape>', lambda e: self.clear())
        self.root.bind('<BackSpace>', lambda e: self.backspace())
        
        # Number and operator bindings
        for i in range(10):
            self.root.bind(str(i), lambda e, num=str(i): self.insert_number(num))
        
        self.root.bind('+', lambda e: self.insert_operator('+'))
        self.root.bind('-', lambda e: self.insert_operator('-'))
        self.root.bind('*', lambda e: self.insert_operator('*'))
        self.root.bind('/', lambda e: self.insert_operator('/'))
        self.root.bind('.', lambda e: self.insert_number('.'))
        
        # Focus on the calculator
        self.root.focus_set()
        
        # Start the main loop
        self.root.mainloop()

if __name__ == "__main__":
    app = SmartCalculator()
    app.run()