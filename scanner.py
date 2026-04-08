import socket
import threading
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from queue import Queue
import csv

# Dictionary of common ports and their services
COMMON_PORTS = {
    20: "FTP-DATA", 21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
    53: "DNS", 80: "HTTP", 110: "POP3", 135: "RPC", 139: "NetBIOS",
    143: "IMAP", 443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S",
    1723: "PPTP", 3306: "MySQL", 3389: "RDP", 5900: "VNC", 8080: "HTTP-Proxy"
}

class PortScannerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python High-Speed Port Scanner")
        self.root.geometry("600x500")
        
        self.queue = Queue()
        self.open_ports = []
        self.is_scanning = False

        self.create_widgets()

    def create_widgets(self):
        # Input Frame
        input_frame = ttk.LabelFrame(self.root, text="Scan Settings", padding=10)
        input_frame.pack(fill="x", padx=10, pady=10)

        ttk.Label(input_frame, text="Target IP/Host:").grid(row=0, column=0, sticky="w")
        self.target_entry = ttk.Entry(input_frame)
        self.target_entry.insert(0, "127.0.0.1")
        self.target_entry.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        ttk.Label(input_frame, text="Port Range (e.g. 1-1024):").grid(row=1, column=0, sticky="w")
        port_range_frame = ttk.Frame(input_frame)
        port_range_frame.grid(row=1, column=1, sticky="w")
        
        self.start_port = ttk.Entry(port_range_frame, width=8)
        self.start_port.insert(0, "1")
        self.start_port.pack(side="left", padx=2)
        
        ttk.Label(port_range_frame, text="-").pack(side="left")
        
        self.end_port = ttk.Entry(port_range_frame, width=8)
        self.end_port.insert(0, "1024")
        self.end_port.pack(side="left", padx=2)

        # Buttons
        btn_frame = ttk.Frame(self.root)
        btn_frame.pack(fill="x", padx=10)

        self.scan_btn = ttk.Button(btn_frame, text="Start Scan", command=self.start_scan_thread)
        self.scan_btn.pack(side="left", padx=5)

        self.export_btn = ttk.Button(btn_frame, text="Export CSV", command=self.export_results, state="disabled")
        self.export_btn.pack(side="left", padx=5)

        # Results Treeview
        self.tree = ttk.Treeview(self.root, columns=("Port", "Status", "Service"), show="headings")
        self.tree.heading("Port", text="Port")
        self.tree.heading("Status", text="Status")
        self.tree.heading("Service", text="Service")
        self.tree.column("Port", width=100)
        self.tree.column("Status", width=100)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # Progress Bar
        self.progress = ttk.Progressbar(self.root, orient="horizontal", mode="determinate")
        self.progress.pack(fill="x", padx=10, pady=5)

    def scan_port(self, target, port):
        try:
            # Create a socket object
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(0.5) # Fast timeout for speed
            result = s.connect_ex((target, port))
            if result == 0:
                service = COMMON_PORTS.get(port, "Unknown")
                self.open_ports.append((port, "Open", service))
                self.root.after(0, self.update_tree, port, "Open", service)
            s.close()
        except:
            pass

    def update_tree(self, port, status, service):
        self.tree.insert("", "end", values=(port, status, service))

    def worker(self, target):
        while not self.queue.empty():
            port = self.queue.get()
            self.scan_port(target, port)
            self.queue.task_done()
            # Update progress bar
            processed = self.total_ports - self.queue.qsize()
            self.progress['value'] = (processed / self.total_ports) * 100

    def start_scan_thread(self):
        if self.is_scanning:
            return
        
        target = self.target_entry.get()
        try:
            start = int(self.start_port.get())
            end = int(self.end_port.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid port numbers.")
            return

        # Reset UI
        for i in self.tree.get_children():
            self.tree.delete(i)
        self.open_ports = []
        self.scan_btn.config(state="disabled")
        self.export_btn.config(state="disabled")
        
        # Fill Queue
        for port in range(start, end + 1):
            self.queue.put(port)
        
        self.total_ports = self.queue.qsize()
        self.is_scanning = True

        # Run scan in background thread to keep UI responsive
        threading.Thread(target=self.run_scanner, args=(target,), daemon=True).start()

    def run_scanner(self, target):
        # Using 100 threads for high speed
        thread_list = []
        for _ in range(100):
            t = threading.Thread(target=self.worker, args=(target,))
            t.start()
            thread_list.append(t)

        for t in thread_list:
            t.join()

        self.is_scanning = False
        self.scan_btn.config(state="normal")
        self.export_btn.config(state="normal")
        messagebox.showinfo("Scan Complete", f"Scanning of {target} finished.")

    def export_results(self):
        if not self.open_ports:
            return
        
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'w', newline='') as f:
                writer = csv.writer(f)
                writer.writerow(["Port", "Status", "Service"])
                writer.writerows(self.open_ports)
            messagebox.showinfo("Success", f"Results exported to {file_path}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PortScannerGUI(root)
    root.mainloop()