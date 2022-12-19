import subprocess
import re
import paramiko
import argparse

def is_ssh_open(hostname, username, password):
    # initialize SSH client
    client = paramiko.SSHClient()
    # add to know hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password=password, timeout=3)
    except Exception as e:
        print(e)
        return False
    else:
        return True

def find_local_ip_by_username(username, password):
    # Get the list of IP addresses from the "arp -a" command
    output = subprocess.run(["arp", "-a"], capture_output=True).stdout.decode()
    ip_addresses = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', output)
    # Loop through the IP addresses and try to connect to each one via SSH
    for ip in ip_addresses:
        print(ip)
        ssh_open = is_ssh_open(ip,username, password)
        if ssh_open:
            return True, ip
        
    return False, None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--username', type=str, default='pi')
    parser.add_argument('--password', type=str, default='12345678')

    args = parser.parse_args()

    ret, raspberry_pi_ip = find_local_ip_by_username(args.username, args.password)
    if ret:
        print("Raspberry pi ip: ", raspberry_pi_ip)
    else:
        print("Raspberry pi ip was not found")
    
