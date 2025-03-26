# main.py
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import webbrowser
import csv
import requests
from bs4 import BeautifulSoup
import time
import threading

class LinkOpenerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Sitemap Opener by Sceiiya")
        self.root.geometry("375x500")

        # Sitemap URL Entry
        self.sitemap_label = tk.Label(root, text="Enter Sitemap URL:")
        self.sitemap_label.pack(pady=5)
        
        self.sitemap_entry = tk.Entry(root, width=40)
        self.sitemap_entry.pack(pady=5)
        
        self.sitemap_button = tk.Button(root, text="Open Sitemap Links", command=self.start_sitemap_links)
        self.sitemap_button.pack(pady=5)

        # CSV File Upload
        self.csv_label = tk.Label(root, text="Or Upload CSV File:")
        self.csv_label.pack(pady=10)
        
        self.csv_button = tk.Button(root, text="Choose CSV File", command=self.start_csv_links)
        self.csv_button.pack(pady=5)

        # Delay Setting
        self.delay_label = tk.Label(root, text="Delay between links (seconds):")
        self.delay_label.pack(pady=5)
        
        self.delay_entry = tk.Entry(root, width=10)
        self.delay_entry.insert(0, "3")
        self.delay_entry.pack(pady=5)

        # Control Buttons
        self.pause_button = tk.Button(root, text="Pause", command=self.pause_links, state='disabled')
        self.pause_button.pack(pady=5)
        
        self.resume_button = tk.Button(root, text="Resume", command=self.resume_links, state='disabled')
        self.resume_button.pack(pady=5)
        
        self.stop_button = tk.Button(root, text="Stop", command=self.stop_links, state='disabled')
        self.stop_button.pack(pady=5)

        # Progress Display
        self.progress_label = tk.Label(root, text="Progress: 0/0 links opened")
        self.progress_label.pack(pady=5)
        
        self.progress_bar = ttk.Progressbar(root, length=300, mode='determinate')
        self.progress_bar.pack(pady=5)
        
        # Status Label
        self.status = tk.Label(root, text="")
        self.status.pack(pady=10)
        
        self.developer_label = ttk.Label(root, text="2025 © Sceiiya", foreground="purple", cursor="hand2")
        self.developer_label.pack(pady=5)

        self.developer_label.bind("<Button-1>", self.open_github)

        # State variables
        self.paused = False
        self.stopped = False
        self.current_index = 0
        self.links = []
        self.thread = None


    def open_github(event):
      webbrowser.open('https://github.com/sceiiya')
    
    def get_sitemap_links(self, sitemap_url):
        try:
            response = requests.get(sitemap_url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'xml')
            urls = [loc.text for loc in soup.find_all('loc') if loc.text]
            return urls
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch sitemap: {str(e)}")
            return []

    def open_links_with_delay(self):
        try:
            delay = float(self.delay_entry.get())
            if delay < 0:
                raise ValueError("Delay cannot be negative")
        except ValueError:
            messagebox.showwarning("Warning", "Invalid delay value, using 3 seconds")
            delay = 3

        total_links = len(self.links)
        self.progress_bar['maximum'] = total_links
        self.progress_label.config(text=f"Progress: {self.current_index}/{total_links} links opened")
        self.status.config(text=f"Opening {total_links} links with {delay}s delay...")
        self.root.update()

        for i in range(self.current_index, total_links):
            if self.stopped:
                break
            if self.paused:
                while self.paused and not self.stopped:
                    time.sleep(0.1)  # Wait while paused
                if self.stopped:
                    break
            
            self.current_index = i
            webbrowser.open_new_tab(self.links[i])
            self.progress_bar['value'] = i + 1
            self.progress_label.config(text=f"Progress: {i + 1}/{total_links} links opened")
            self.root.update()
            if i < total_links - 1:  # Don't delay after the last link
                time.sleep(delay)
        
        if self.stopped:
            self.status.config(text=f"Stopped at {self.current_index + 1}/{total_links} links")
        else:
            self.status.config(text=f"Finished opening {total_links} links")
        self.reset_buttons()

    def reset_buttons(self):
        self.sitemap_button.config(state='normal')
        self.csv_button.config(state='normal')
        self.pause_button.config(state='disabled')
        self.resume_button.config(state='disabled')
        self.stop_button.config(state='disabled')
        self.paused = False
        self.stopped = False
        self.current_index = 0
        self.links = []

    def start_sitemap_links(self):
        sitemap_url = self.sitemap_entry.get().strip()
        if not sitemap_url:
            messagebox.showwarning("Warning", "Please enter a sitemap URL")
            return
        
        self.links = self.get_sitemap_links(sitemap_url)
        if self.links:
            self.start_opening()
        else:
            self.status.config(text="No valid links found in sitemap")
            self.progress_label.config(text="Progress: 0/0 links opened")
            self.progress_bar['value'] = 0

    def start_csv_links(self):
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        if not file_path:
            return
        
        self.status.config(text="Reading CSV...")
        self.root.update()
        
        try:
            with open(file_path, 'r', newline='') as csvfile:
                reader = csv.reader(csvfile)
                self.links = [row[0] for row in reader if row and row[0]]
            if self.links:
                self.start_opening()
            else:
                self.status.config(text="No valid links found in CSV")
                self.progress_label.config(text="Progress: 0/0 links opened")
                self.progress_bar['value'] = 0
        except Exception as e:
            messagebox.showerror("Error", f"Failed to process CSV: {str(e)}")
            self.status.config(text="Error occurred")

    def start_opening(self):
        self.sitemap_button.config(state='disabled')
        self.csv_button.config(state='disabled')
        self.pause_button.config(state='normal')
        self.stop_button.config(state='normal')
        self.paused = False
        self.stopped = False
        if not self.thread or not self.thread.is_alive():
            self.thread = threading.Thread(target=self.open_links_with_delay)
            self.thread.start()

    def pause_links(self):
        self.paused = True
        self.pause_button.config(state='disabled')
        self.resume_button.config(state='normal')
        self.status.config(text=f"Paused at {self.current_index + 1}/{len(self.links)} links")

    def resume_links(self):
        self.paused = False
        self.pause_button.config(state='normal')
        self.resume_button.config(state='disabled')
        self.status.config(text=f"Resuming from {self.current_index + 1}/{len(self.links)} links")

    def stop_links(self):
        self.stopped = True
        self.paused = False  # Ensure it doesn't stay paused
        self.pause_button.config(state='disabled')
        self.resume_button.config(state='disabled')
        self.stop_button.config(state='disabled')

def main():
    root = tk.Tk()
    app = LinkOpenerApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()