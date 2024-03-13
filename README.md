# NetGuardian

## Introduction

NetGuardian is an advanced network security tool designed to combat Distributed Denial of Service (DDoS) attacks. Developed using Python3, it diligently monitors network traffic, effectively detecting and mitigating various types of attacks, including:

- SYN Flood Attacks
- SYN-ACK Flood Attacks
- ICMP Smurf Attacks
- Ping of Death

In addition to detection, NetGuardian provides detailed insights into the origins of attacks, empowering users with comprehensive information about attackers. This version of NetGuardian introduces significant optimizations, leveraging threads, the Quart framework, and WebSockets to deliver an intuitive and responsive Web User Interface.

## Key Features

### 1. Comprehensive Attack Detection
   - Detects SYN Flood, SYN-ACK Flood, ICMP Smurf, and Ping of Death attacks.
   - Provides detailed information about detected attacks and attackers.

### 2. Optimized Performance
   - Utilizes threads for efficient concurrent processing.
   - Implements significant optimizations for improved performance.

### 3. Intuitive Web Interface
   - Built using the Quart framework and WebSockets.
   - Offers a user-friendly and responsive Web User Interface for easy interaction.

## Upcoming Features

In future releases, NetGuardian aims to enhance its capabilities with the following features:

- Expansion of attack detection algorithms to cover a wider range of threats.
- Implementation of defense mechanisms to neutralize DDoS attacks (available for LINUX only).
- Enhancement of animations and transitions to create a visually engaging Web UI experience.

## Installation

To install NetGuardian, follow these simple steps:

```bash
git clone https://github.com/Pranjeban/NetGuardian
cd NetGaurdian
pip install -r requirements.txt
```
## Usage
Before running NetGuardian, ensure you have appropriate permissions:

1. Linux: Execute the script with root privileges.
2. Windows: Run the script as an Administrator.
To launch NetGuardian, execute the following command:
``` bash
sudo python3 app.py
```
This will initiate the web interface on your local port 5000. Simply open your web browser and navigate to http://127.0.0.1:5000 to access it.
