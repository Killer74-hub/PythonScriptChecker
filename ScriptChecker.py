import tkinter as tk
from tkinter import scrolledtext
import sys
import io
import os
import importlib.util
import subprocess

class ScriptErrorChecker:
    def __init__(self, root):
        self.root = root
        self.root.title("Script Error Checker")

        # Text area for pasting the script
        self.script_text = scrolledtext.ScrolledText(root, width=50, height=20, wrap=tk.WORD)
        self.script_text.pack(pady=10)

        # Button to check for errors
        self.check_button = tk.Button(root, text="Check for Errors", command=self.check_errors)
        self.check_button.pack()

        # Text area to display errors
        self.error_text = scrolledtext.ScrolledText(root, width=50, height=10, wrap=tk.WORD, state=tk.DISABLED)
        self.error_text.pack(pady=10)

        # Text area to display installation messages
        self.installation_text = scrolledtext.ScrolledText(root, width=50, height=5, wrap=tk.WORD, state=tk.DISABLED)
        self.installation_text.pack(pady=10)

    def check_errors(self):
        # Clear the error text area
        self.error_text.config(state=tk.NORMAL)
        self.error_text.delete(1.0, tk.END)

        # Redirect stdout to capture error messages
        sys.stdout = io.StringIO()
        try:
            exec(self.script_text.get("1.0", tk.END))
        except Exception as e:
            error_message = str(e)
            self.error_text.insert(tk.END, error_message)
            self.install_missing_libraries(error_message)
        finally:
            # Restore stdout
            sys.stdout = sys.__stdout__
            self.error_text.config(state=tk.DISABLED)

    def install_missing_libraries(self, error_message):
        missing_libs = self.extract_missing_libraries(error_message)
        for lib in missing_libs:
            self.install_library(lib)

    def extract_missing_libraries(self, error_message):
        # Extract missing libraries from the error message
        missing_libs = []
        lines = error_message.split('\n')
        for line in lines:
            if "No module named" in line:
                missing_lib = line.split("'")[1]
                missing_libs.append(missing_lib)
        return missing_libs

    def install_library(self, library):
        try:
            # Use pip to install the missing library
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', library])
            # Display success message
            self.installation_text.config(state=tk.NORMAL)
            self.installation_text.insert(tk.END, f"Successfully installed {library}\n")
            self.installation_text.config(state=tk.DISABLED)
        except subprocess.CalledProcessError as e:
            # Failed to install library
            print(f"Failed to install {library}: {e}")
        else:
            print(f"Successfully installed {library}")

if __name__ == "__main__":
    # Hide the Python console
    sys.stdout = open(os.devnull, "w")
    
    root = tk.Tk()
    app = ScriptErrorChecker(root)
    root.mainloop()