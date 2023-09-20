import socket
import ipaddress
import concurrent.futures

def is_ip_reachable(ip):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            s.connect((str(ip), 80))
        return True
    except (socket.timeout, ConnectionRefusedError):
        return False

def sweep_ips(start_ip, end_ip, output_file, verbose=False):
    start_ip = ipaddress.IPv4Address(start_ip)
    end_ip = ipaddress.IPv4Address(end_ip)

    reachable_ips = []

    with concurrent.futures.ThreadPoolExecutor() as executor:
        ip_range = ipaddress.summarize_address_range(start_ip, end_ip)
        for ip_network in ip_range:
            for ip in ip_network.hosts():
                if verbose:
                    print(f"Scanning {ip}...", end=" ")
                if is_ip_reachable(ip):
                    reachable_ips.append(str(ip))
                    if verbose:
                        print("Reachable")
                elif verbose:
                    print("Unreachable")

    with open(output_file, "w") as f:
        for ip in reachable_ips:
            f.write(ip + "\n")

    return reachable_ips

if __name__ == "__main__":
    print("Welcome to the IP Sweeper")

    start_ip = input("Enter the starting IP address (default: 192.168.1.1): ") or "192.168.1.1"
    end_ip = input("Enter the ending IP address (default: 192.168.1.254): ") or "192.168.1.254"
    output_file = input("Enter the output file name (default: reachable_ips.txt): ") or "reachable_ips.txt"
    
    verbose_input = input("Enable verbose output? (yes/no, default: no): ").lower()
    verbose = verbose_input == "yes"
    
    print("Starting IP sweep...")
    reachable_ips = sweep_ips(start_ip, end_ip, output_file, verbose=verbose)
    
    print("Reachable IP addresses:")
    for ip in reachable_ips:
        print(ip)

    print(f"Reachable IPs written to {output_file}")
