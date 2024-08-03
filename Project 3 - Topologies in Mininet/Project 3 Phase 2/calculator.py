import subprocess
import time

def run_command_in_xterm(host_name, command):
    xterm_command = f"xterm -e 'bash -c \"{command}; bash\"'"
    subprocess.Popen(['xterm', '-e', f'sudo python -m pywin.modes.tf {xterm_command}'])

def measure_latency(source_ip, destination_ip):
    ping_command = f"ping -c 4 {destination_ip}"  # Send 4 ICMP echo requests
    result = subprocess.run(ping_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    # Extract and parse latency from the result
    # Record the latency measurement

def measure_throughput(server_ip, client_ip):
    iperf_server_command = f"iperf -s -p 4000"  # Start iPerf server on port 4000
    iperf_client_command = f"iperf -c {server_ip} -p 4000"  # Start iPerf client on port 4000
    run_command_in_xterm('h3', iperf_server_command)  # Run server in h3 XTerm
    time.sleep(2)  # Wait for server to start
    run_command_in_xterm('h1', iperf_client_command)  # Run client in h1 XTerm

# Host IP addresses in the topology
host_ips = {
    'h1': '10.0.0.1',
    'h2': '10.0.0.2',
    'h3': '10.0.0.3',
    'h4': '10.0.0.4',
    'h5': '10.0.0.5',
    'h6': '10.0.0.6',
    'h7': '10.0.0.7',
    'h8': '10.0.0.8',
    'h9': '10.0.0.9'
}

# Links between switches in the topology
switch_links = [('s1', 's2'), ('s2', 's3'), ('s3', 's4'), ('s3', 's5')]

# Measure latency and throughput for each link
for link in switch_links:
    source_switch = link[0]
    destination_switch = link[1]
    source_ip = host_ips[f'h{int(source_switch[1:])}']
    destination_ip = host_ips[f'h{int(destination_switch[1:])}']
    
    # Measure latency
    measure_latency(source_ip, destination_ip)
    
    # Measure throughput
    measure_throughput(source_ip, destination_ip)
