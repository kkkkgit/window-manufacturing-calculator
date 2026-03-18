#!/usr/bin/env python3
"""
Window Manufacturing Calculator GUI
Allows users to input window parameters and view the calculated parts list.
"""

import threading
import tkinter as tk
from tkinter import ttk, messagebox
from window_calculator import get_parts_list, format_output
from ai_customizer import apply_customer_customization


class WindowCalculatorApp:
    """GUI application for window manufacturing calculations."""

    def __init__(self, root):
        """Initialize the GUI."""
        self.root = root
        self.root.title("Window Manufacturing Calculator")
        self.root.geometry("800x600")
        
        # Create main frame
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create input frame
        self.input_frame = ttk.LabelFrame(self.main_frame, text="Input Parameters", padding="10")
        self.input_frame.pack(fill=tk.X, pady=5)
        
        # Window Type
        ttk.Label(self.input_frame, text="Window Type:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.window_type = tk.StringVar(value="A")
        ttk.Combobox(self.input_frame, textvariable=self.window_type, values=["A", "TA"], state="readonly").grid(row=0, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Width
        ttk.Label(self.input_frame, text="Width (mm):").grid(row=1, column=0, sticky=tk.W, padx=5, pady=2)
        self.width = tk.IntVar(value=900)
        ttk.Entry(self.input_frame, textvariable=self.width).grid(row=1, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Height
        ttk.Label(self.input_frame, text="Height (mm):").grid(row=2, column=0, sticky=tk.W, padx=5, pady=2)
        self.height = tk.IntVar(value=900)
        ttk.Entry(self.input_frame, textvariable=self.height).grid(row=2, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Tolerance (tk)
        ttk.Label(self.input_frame, text="Tolerance (tk):").grid(row=3, column=0, sticky=tk.W, padx=5, pady=2)
        self.tolerance = tk.IntVar(value=3)
        ttk.Entry(self.input_frame, textvariable=self.tolerance).grid(row=3, column=1, sticky=tk.W, padx=5, pady=2)
        
        # Hand
        ttk.Label(self.input_frame, text="Hand:").grid(row=4, column=0, sticky=tk.W, padx=5, pady=2)
        self.hand = tk.StringVar(value="P")
        ttk.Combobox(self.input_frame, textvariable=self.hand, values=["P", "V"], state="readonly").grid(row=4, column=1, sticky=tk.W, padx=5, pady=2)

        # Calculate button
        ttk.Button(self.input_frame, text="Calculate", command=self.calculate_parts).grid(row=5, column=0, columnspan=2, pady=10)

        # Special requests section
        self.custom_frame = ttk.LabelFrame(self.main_frame, text="Kliendi erisoovid (AI agent)", padding="10")
        self.custom_frame.pack(fill=tk.X, pady=5)

        ttk.Label(self.custom_frame, text="Erisoov:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=2)
        self.custom_request = tk.StringVar()
        ttk.Entry(self.custom_frame, textvariable=self.custom_request, width=60).grid(row=0, column=1, sticky=tk.EW, padx=5, pady=2)
        self.custom_frame.columnconfigure(1, weight=1)

        self.apply_btn = ttk.Button(self.custom_frame, text="Rakenda erisoovid", command=self.apply_customization)
        self.apply_btn.grid(row=1, column=0, columnspan=2, pady=5)

        self._base_result = None
        
        # Create output frame
        self.output_frame = ttk.LabelFrame(self.main_frame, text="Calculation Results", padding="10")
        self.output_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        
        # Text widget for output
        self.output_text = tk.Text(self.output_frame, wrap=tk.WORD, font=("Courier", 10))
        self.output_text.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.output_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.output_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.output_text.yview)

    def calculate_parts(self):
        """Calculate and display the parts list."""
        try:
            window_type = self.window_type.get()
            width = self.width.get()
            height = self.height.get()
            tolerance = self.tolerance.get()
            hand = self.hand.get()

            if width <= 0 or height <= 0 or tolerance < 0:
                messagebox.showerror("Error", "Dimensions must be positive.")
                return

            self._base_result = get_parts_list(window_type, width, height, tolerance, hand)

            output = format_output(self._base_result)
            self.output_text.delete(1.0, tk.END)
            self.output_text.insert(tk.END, output)

        except ValueError as e:
            messagebox.showerror("Error", str(e))
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred: {e}")

    def apply_customization(self):
        """Apply customer special request using AI agent."""
        if not self._base_result:
            messagebox.showwarning("Hoiatus", "Esmalt arvuta akna mõõdud (Calculate).")
            return

        request = self.custom_request.get().strip()
        if not request:
            messagebox.showwarning("Hoiatus", "Palun sisesta erisoov.")
            return

        self.apply_btn.config(state="disabled", text="AI töötab...")
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, "AI agent rakendab erisoove...\n")

        def run_in_thread():
            try:
                modified = apply_customer_customization(self._base_result, request)
                output = format_output(modified)
                self.root.after(0, self._show_customization_result, output)
            except Exception as e:
                self.root.after(0, self._show_customization_error, str(e))

        threading.Thread(target=run_in_thread, daemon=True).start()

    def _show_customization_result(self, output: str):
        self.output_text.delete(1.0, tk.END)
        self.output_text.insert(tk.END, output)
        self.apply_btn.config(state="normal", text="Rakenda erisoovid")

    def _show_customization_error(self, error: str):
        messagebox.showerror("Viga", f"Erisoovide rakendamine ebaõnnestus:\n{error}")
        self.apply_btn.config(state="normal", text="Rakenda erisoovid")


def main():
    """Run the GUI application."""
    root = tk.Tk()
    app = WindowCalculatorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()