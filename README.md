Python High-Speed Port Scanner
Manual network reconnaissance and port scanning can be complex and time-consuming. This project provides a fast, lightweight, and user-friendly visual tool to quickly identify open ports and active services on a target network without typing complex commands.

🚀 Features

Multi-Threaded Performance: Utilizes a high-speed, multi-threaded architecture (up to 500 concurrent workers) to scan thousands of ports in seconds.
+3


User-Friendly GUI: Built with Tkinter, offering an intuitive interface for inputting targets and viewing real-time results.


Target Flexibility: Supports scanning via both IP addresses and Hostnames (e.g., 127.0.0.1 or localhost).
+1


Service Mapping: Automatically maps open ports to their corresponding common services (e.g., HTTP, SSH, FTP, SMB).
+2


Real-Time Progress: Features a dynamic progress bar and status updates to track the scan's completion.
+1


Result Export: Allows users to save a formatted list of open ports and services to a .txt file for further vulnerability assessment.

🛠️ Built With
Python: The core programming language.


Socket: For low-level network communication and TCP connections.
+1


Threading & Queue: To handle concurrent port scanning without freezing the UI.
+1


Tkinter: For the graphical user interface components.
+1

💻 Installation & Usage
Prerequisites
Python 3.x installed on your machine.

Git installed (optional, for cloning the repository).

Running the Application
Clone the Repository:

Bash
git clone https://github.com/yashgitofficial/python-port-scanner.git
cd python-port-scanner
Launch the Scanner:

Bash
python scanner.py
Start a Scan:

Enter the Target IP/Hostname (e.g., 127.0.0.1).

Define the Start Port and End Port range (e.g., 1 to 1024).

Click Start Scan to begin the process.

Once complete, use Save Results to export your findings.
+1

📑 Project Structure

scanner.py: The main application script containing both the logic and GUI.
+1

.gitignore: Prevents temporary Python files and scan result logs from being uploaded to the repository.

README.md: Project documentation.

⚠️ Ethical Disclaimer
Important: This tool is developed for educational and authorized security testing purposes only. Port scanning unauthorized networks or systems is illegal and unethical. Always ensure you have explicit written permission before scanning any target that you do not own.
