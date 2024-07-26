import os

def apply_security_hardening():
    # Ensure the script is run as root
    if os.geteuid() != 0:
        print("This script must be run as root. Please use 'sudo'.")
        exit(1)

    # Disable TCP forwarding in SSH (Placeholder path)
    sshd_config_path = '/etc/ssh/sshd_config'
    print(f"Appending 'AllowTcpForwarding no' to {sshd_config_path}")
    with open(sshd_config_path, 'a') as f:
        f.write('\nAllowTcpForwarding no\n')

    # Enable PAM in SSH (Placeholder path)
    print(f"Appending 'UsePAM yes' to {sshd_config_path}")
    with open(sshd_config_path, 'a') as f:
        f.write('\nUsePAM yes\n')

    # Enable reverse path filtering (Placeholder path)
    sysctl_config_path = '/etc/sysctl.conf'
    print(f"Appending 'net.ipv4.conf.default.rp_filter=1' to {sysctl_config_path}")
    with open(sysctl_config_path, 'a') as f:
        f.write('\nnet.ipv4.conf.default.rp_filter=1\n')

    # Disable the CUPS service
    print("Disabling CUPS service")
    os.system('systemctl disable cups')

if __name__ == '__main__':
    apply_security_hardening()
    print("Security hardening applied.")
