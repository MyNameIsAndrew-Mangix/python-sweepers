import socket

def scan_ports(target_ip, specific_ports=None, verbose=True):
    open_ports = []

    for port in specific_ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex((target_ip, port))

            if result == 0:
                open_ports.append(port)
                if verbose:
                    print(f"Port {port} is open")
            elif verbose:
                print(f"Port {port} is closed")

    return open_ports

if __name__ == "__main__":
    print("Welcome to the Port Sweeper")

    # Default values
    default_ip = "192.168.1.1"
    preset_choice = "1"         # Default to Quick Scan
    verbose = True              # Default to verbose output
    
    # Define presets
    quick_scan_ports = [20, 21, 22, 23, 25, 53, 80, 110, 143, 443, 3389]
    custom_scan_ports = None
    complete_scan_ports = list(range(1, 65536))
    
    use_default_ip = input(f"Use default IP ({default_ip})? (yes/no, default: yes): ").lower()
    
    if use_default_ip != "no":
        target_ip = default_ip
    else:
        target_ip = input("Enter the target IP address (press Enter for default): ").strip() or default_ip
    
    preset_choice = input("Select a scan preset:\n"
                          "1. Quick Scan (common ports)\n"
                          "2. Custom Scan (user-input specific ports)\n"
                          "3. Complete Scan (all ports)\n"
                          "Enter the number of your choice (default: 1): ").strip() or "1"
    
    # Set ports to scan based on preset choice
    if preset_choice == "1":
        specific_ports = quick_scan_ports
    elif preset_choice == "2":
        specific_ports = []
        start_port = input("Enter the starting port number (press Enter for default): ").strip()
        start_port = int(start_port) if start_port else 1
        end_port = input("Enter the ending port number (press Enter for default): ").strip()
        end_port = int(end_port) if end_port else 65535
        specific_ports += list(range(start_port, end_port + 1))
        
        additional_ports = input("Enter specific ports to scan (comma-separated list with no spaces, e.g., 80,443,5000) "
                                  "(press Enter for none): ").strip()
        additional_ports = [int(port) for port in additional_ports.split(",")] if additional_ports else []
        specific_ports += additional_ports
    else:
        specific_ports = complete_scan_ports
    
    output_file = input("Enter the output file name (press Enter for default): ").strip() or "open_ports.txt"
    
    verbose_input = input("Enable verbose output? (yes/no, default: yes): ").strip().lower() or "yes"
    verbose = verbose_input == "yes"

    open_ports = scan_ports(target_ip, specific_ports=specific_ports, verbose=verbose)

    if open_ports:
        print("Open ports:")
        for port in open_ports:
            print(port)
    else:
        print("No open ports found.")
    
    with open(output_file, "w") as f:
        for port in open_ports:
            f.write(f"{port}\n")

    print(f"Open ports written to {output_file}")
