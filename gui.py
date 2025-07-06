import os
import tkinter as tk
from tkinter import filedialog, messagebox, scrolledtext
from tkinter import ttk
from PIL import Image, ImageTk

from project import analyze_java_code, generate_report, save_report, save_pdf_report


os.chdir(os.path.dirname(os.path.abspath(__file__)))


class JavaStaticAnalyzerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Java Static Analyzer")
        self.geometry("900x650")
        self.minsize(700, 500)

        self.dark_mode = False
        self.report_text = ""
        self.current_file = ""
        self.icons = {}

        self.load_icons()

        self.splash_label = tk.Label(self, text="Welcome to Java Static Analyzer", font=("Segoe UI", 24, "bold"))
        self.splash_label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        self.after(10, self.animate_splash, 0)

        self.main_frame = ttk.Frame(self)

    def load_icons(self):
        icon_names = ["clear_icon.png", "download_icon.png", "folder_icon.png", "pdf_icon.png", "theme_icon.png"]
        keys = ["clear", "download", "folder", "pdf", "theme"]
        for key, filename in zip(keys, icon_names):
            path = os.path.join("iconss", filename)
            try:
                img = Image.open(path).resize((24, 24), Image.Resampling.LANCZOS)
                self.icons[key] = ImageTk.PhotoImage(img)
            except Exception as e:
                print(f"Error loading {filename}: {e}")
                self.icons[key] = None

    def animate_splash(self, alpha):
        if alpha <= 20:
            gray_val = 255 - (alpha * 12)
            color = f"#{gray_val:02x}{gray_val:02x}{gray_val:02x}"
            self.splash_label.config(fg=color)
            self.after(50, self.animate_splash, alpha + 1)
        else:
            self.splash_label.destroy()
            self.build_main_ui()
            self.main_frame.pack(fill=tk.BOTH, expand=True)

    def build_main_ui(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()

        heading_label = ttk.Label(self.main_frame, text="Java Static Analyzer", font=("Segoe UI", 20, "bold"))
        heading_label.pack(pady=(10, 5))

        icon_frame = ttk.Frame(self.main_frame)
        icon_frame.pack(pady=10)

        icons_data = [
            ("folder", "Open File", self.select_and_analyze),
            ("clear", "Clear", self.clear_text),
            ("download", "Download TXT", self.download_txt_report),
            ("pdf", "Download PDF", self.download_pdf_report),
            ("theme", "Toggle Theme", self.toggle_theme)
        ]

        for idx, (key, text, cmd) in enumerate(icons_data):
            frame = ttk.Frame(icon_frame)
            frame.grid(row=0, column=idx, padx=15)

            icon_image = self.icons.get(key)
            if icon_image:
                icon_label = tk.Label(frame, image=icon_image, cursor="hand2")
            else:
                icon_label = tk.Label(frame, text="❌", font=("Segoe UI", 14), cursor="hand2")

            icon_label.pack()
            icon_label.bind("<Button-1>", lambda e, command=cmd: command())

            text_label = ttk.Label(frame, text=text)
            text_label.pack()

        self.text_area = scrolledtext.ScrolledText(self.main_frame, font=("Consolas", 11), wrap=tk.WORD)
        self.text_area.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        self.text_area.config(state=tk.DISABLED)

        self.status_bar = ttk.Label(self.main_frame, text="Welcome! Select a Java file to analyze.", anchor=tk.W, relief=tk.SUNKEN)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

        self.apply_light_theme()

    def clear_text(self):
        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.config(state=tk.DISABLED)
        self.report_text = ""
        self.current_file = ""
        self.update_status("Cleared report area.")

    def select_and_analyze(self):
        file_path = filedialog.askopenfilename(filetypes=[("Java Files", "*.java")])
        if not file_path:
            self.update_status("File selection cancelled.")
            return
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                code = f.read()
        except Exception as e:
            messagebox.showerror("File Error", f"Cannot read file:\n{e}")
            self.update_status("Error reading file.")
            return

        issues = analyze_java_code(code, file_path)
        report = generate_report(file_path, issues)

        self.text_area.config(state=tk.NORMAL)
        self.text_area.delete(1.0, tk.END)
        self.text_area.insert(tk.END, report)
        self.text_area.config(state=tk.DISABLED)

        self.report_text = report
        self.current_file = file_path
        self.update_status(f"Analyzed file: {os.path.basename(file_path)}")

    def download_txt_report(self):
        if not self.report_text:
            messagebox.showwarning("No Report", "No report available to save.")
            return
        try:
            path = save_report(self.report_text, self.current_file)
            messagebox.showinfo("Success", f"Report saved as:\n{path}")
            self.update_status(f"Report saved to {path}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save report:\n{e}")
            self.update_status("Failed to save report.")

    def download_pdf_report(self):
        if not self.report_text:
            messagebox.showwarning("No Report", "No report available to save.")
            return
        try:
            path = save_pdf_report(self.report_text, self.current_file)
            messagebox.showinfo("Success", f"PDF saved as:\n{path}")
            self.update_status(f"PDF report saved to {path}")
        except Exception as e:
            messagebox.showerror("Save Error", f"Failed to save PDF:\n{e}")
            self.update_status("Failed to save PDF.")

    def toggle_theme(self):
        if self.dark_mode:
            self.apply_light_theme()
        else:
            self.apply_dark_theme()

    def apply_light_theme(self):
        self.dark_mode = False
        self.set_theme_colors(bg="white", fg="black", text_bg="white", text_fg="black")
        self.update_status("Light mode activated.")

    def apply_dark_theme(self):
        self.dark_mode = True
        self.set_theme_colors(bg="#121212", fg="#00bcd4", text_bg="#1e1e1e", text_fg="#eeeeee")
        self.update_status("Dark mode activated.")

    def set_theme_colors(self, bg, fg, text_bg, text_fg):
        self.configure(bg=bg)
        self.main_frame.configure(style="MainFrame.TFrame")
        for child in self.main_frame.winfo_children():
            if isinstance(child, (ttk.Label, ttk.Frame)):
                child.configure(style="MainFrame.TFrame")
            if isinstance(child, tk.Label):
                child.configure(bg=bg, fg=fg)
        self.text_area.configure(bg=text_bg, fg=text_fg, insertbackground=fg)
        self.status_bar.configure(background=bg, foreground=fg)

    def update_status(self, message):
        self.status_bar.config(text=message)
if __name__ == "__main__":
    app = JavaStaticAnalyzerGUI()
    app.mainloop()