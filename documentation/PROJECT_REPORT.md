# Corporate Office Network with Centralized Services — Project Report

## 1. Abstract
This project simulates a corporate LAN serving HR, Finance, IT, and Sales. Each department is placed in a separate VLAN and IPv4 subnet. Centralized servers provide DHCP, DNS, an internal website, and email. A router performs inter-VLAN routing, while a managed switch provides VLAN segmentation. The design is tested under normal and selected failure conditions.

## 2. Problem statement
A corporate office requires reliable communication between departments and shared access to central services. A flat network makes segmentation, addressing, administration, and troubleshooting more difficult. This project uses departmental VLANs and subnets, centralized services, and a documented test plan to demonstrate a manageable office network.

## 3. Objectives
1. Create a LAN with separate VLANs and subnets for HR, Finance, IT, Sales, and servers.
2. Configure inter-VLAN routing using router-on-a-stick.
3. Provide centralized DHCP using DHCP relay.
4. Configure DNS records for an internal web portal and mail server.
5. Host an internal HTTP website and configure email.
6. Verify normal connectivity and service operation.
7. Test selected service/link failures and recovery.
8. Record actual performance observations and clearly identify simulation limitations.

## 4. Scope and devices
- One router (e.g. Cisco 2911)
- One managed switch (e.g. Cisco 2960)
- Four departmental PCs
- Four servers: DHCP, DNS, web, email
- Cisco Packet Tracer; optional Flask companion dashboard
- Optional Wireshark packet verification if required by faculty

## 5. Architecture
The router connects to the switch over an 802.1Q trunk. The router has one subinterface per VLAN. Each department's access ports belong to its own VLAN. The server VLAN hosts centralized services.

## 6. IP addressing plan
| Network | VLAN | Network | Gateway |
|---|---:|---|---|
| HR | 10 | 192.168.10.0/24 | 192.168.10.1 |
| Finance | 20 | 192.168.20.0/24 | 192.168.20.1 |
| IT | 30 | 192.168.30.0/24 | 192.168.30.1 |
| Sales | 40 | 192.168.40.0/24 | 192.168.40.1 |
| Servers | 50 | 192.168.50.0/24 | 192.168.50.1 |

Server addresses: DNS `192.168.50.10`, DHCP `192.168.50.11`, Web `192.168.50.20`, Email `192.168.50.30`. Mask `255.255.255.0`.

## 7. Protocols and design
- **VLAN / 802.1Q:** separates broadcast domains and tags frames across the trunk.
- **IPv4 subnetting:** provides a distinct IP network for each department and the server segment.
- **Router-on-a-stick:** routes between VLANs through router subinterfaces.
- **DHCP / DORA:** dynamically allocates client network settings; relay (`ip helper-address`) forwards requests to the server on another subnet.
- **DNS:** resolves `intranet.corp.local` to the web server and `mail.corp.local` to the email server.
- **HTTP:** delivers the intranet page over TCP port 80.
- **SMTP / POP3:** supports email sending and retrieval where available in Packet Tracer.
- **ICMP:** used by ping to test IP reachability.

## 8. Implementation
Document the switch VLAN commands, trunk, router subinterfaces, DHCP pools, DNS A records, HTTP page, email accounts, and PC DHCP settings. Insert screenshots from the actual implementation.

## 9. Test plan and results
Complete `TEST_MATRIX.md` with observed outcomes. Do not mark a test as Pass before running it. Do not invent latency, throughput, jitter, packet-loss, or recovery values.

## 10. Performance evaluation
Record latency and packet loss from actual tests. Record DHCP/DNS/service success rates using a stated number of attempts. Note that Packet Tracer timings are simulated and may not represent a physical corporate LAN.

## 11. Limitations and future enhancements
Potential limitations include single points of failure (one router, switch, and each server), simplified access control, and simulated performance. Future improvements may include redundant links/devices, monitoring, ACL-based least privilege, backups, HTTPS, and real packet captures.

## 12. Individual contribution
- Member 1: topology, VLANs, switch configuration, architecture diagram.
- Member 2: router subinterfaces, DHCP relay, client connectivity.
- Member 3: server IPs, DHCP/DNS/HTTP/email services.
- Member 4: test matrix, failure tests, performance records, report/demo coordination.
Each member should contribute to validation and understand the whole project.

## 13. Conclusion
Summarize what worked, the observed test outcomes, service failures/recovery, and the main benefits of departmental segmentation and centralized services.

## 14. References
List the course material, Packet Tracer documentation, and any other sources actually consulted.
