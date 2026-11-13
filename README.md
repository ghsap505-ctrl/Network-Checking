![CyberScan Pro](assets/alhawa-cover.svg)

# Network-Checking · CyberScan Pro

A Python command-line utility for basic network visibility and authorized network auditing.

## Capabilities
- **ARP discovery:** identify responsive devices on a local IPv4 network and display their IP and MAC addresses.
- **TCP port checks:** test a selected host against a small list of commonly used TCP ports.
- **Terminal feedback:** show scan progress and a concise summary of discovered devices or open ports.

## Requirements
- Python 3
- Scapy (`pip install scapy`)
- Appropriate local privileges for ARP packet operations (often administrator/root).

## Run
```bash
pip install scapy
sudo python3 app.py
```

On Windows, run the terminal with the permissions required by your network adapter and Scapy installation.

## Responsible use
Use this tool only on networks and systems you own or are explicitly authorized to assess. Port scanning and network discovery may be restricted by organizational policy or local law. The tool is a learning utility, not a substitute for a maintained professional security scanner.

---

<p align="center"><b>CYBERSCAN PRO</b> · Discover responsibly.</p>
