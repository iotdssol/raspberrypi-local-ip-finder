import subprocess
import re
import paramiko

def is_ssh_open(hostname, username):
    # initialize SSH client
    client = paramiko.SSHClient()
    # add to know hosts
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(hostname=hostname, username=username, password="anything", timeout=3)
    except paramiko.AuthenticationException:
        return True
    except Exception as e:
        print(e)
        return False
    else:
        return True

# Get the list of IP addresses from the "arp -a" command
output = subprocess.run(["arp", "-a"], capture_output=True).stdout.decode()
ip_addresses = re.findall(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', output)

# Loop through the IP addresses and try to connect to each one via SSH
for ip in ip_addresses:
    print(ip)
    ssh_open = is_ssh_open(ip,username)
    if ssh_open:
        print("Raspberry pi ip: ", ip)
        break
else:
    print("Raspberry Pi ip was not found")
