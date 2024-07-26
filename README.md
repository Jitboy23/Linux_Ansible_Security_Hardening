# Security Hardening Automation Project

## 🚀 Overview

**Security Hardening Automation** is a comprehensive solution designed to streamline and automate server security hardening, health checks, and disk management. Utilizing Ansible for automation and Python for detailed system analysis, this project ensures robust security practices and optimal system performance with minimal manual intervention.


## 🛠️ Features
- **Automated Security Hardening**: Apply critical security configurations with ease.
- **Health Checks**: Perform real-time checks on disk and CPU usage to maintain system integrity.
- **Disk Management**: Automated cleanup and space management to prevent system overloads.
- **Robust Logging and Reporting**: Detailed output for easy monitoring and issue resolution.


## 📦 Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/yourusername/security-hardening-automation.git

2. **Navigate to the Project Directory**:
   cd security-hardening-automation

3. **Prerequisites**:
   - **Ansible**: Ensure Ansible is installed and configured.
   - **Python 3**: Required for running the security hardening and health check scripts.


⚙️ **Usage**
1. **Configure Your Environment**:
   - Update **hosts.ini** with your server details.
   - Adjust paths in **site.yml**, **security_hardening.py**, and **health_check.py** as needed.

2. **Run the Ansible Playbook**:
     ```bash
   ansible-playbook -i hosts.ini site.yml


**This playbook performs the following:**
   - Pre-checks: Verify server connectivity and disk usage.
   - Security Hardening: Apply security configurations.
   - Post-checks: Validate SSH status and run health checks.
   - Handle High Disk Utilization: Automatically manage disk space issues.


📝 **Configuration**
- **hosts.ini** Define your server details and SSH key.
- **site.yml** Ansible playbook orchestrating the entire process.
- **security_hardening.py** Python script for applying security configurations.
- **health_check.py** Python script for monitoring disk and CPU usage.

After running the playbook, you can expect detailed logs of:
- Disk and CPU utilization status.
- Actions taken to handle high disk usage.


🤝 **Contributing**: 
Contributions are welcome! If you have suggestions or improvements, please open an issue or submit a pull request.


📄 **License**: 
This project is licensed under the MIT License. See the [License](https://github.com/Jitboy23/Linux_Ansible_Security_Hardening/blob/main/MIT%20LICENSE)
file for more details.


📫 **Contact**: 
For any questions or inquiries, please reach out to jdunlap01@gmail.com
