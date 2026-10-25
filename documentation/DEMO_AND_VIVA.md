# Five-minute demo and viva — Corporate Office Network

## Five-minute demonstration
- **0:00–0:40:** Explain the problem statement and show the topology.
- **0:40–1:20:** Show VLANs, switch trunk, and router subinterfaces.
- **1:20–2:00:** Show a PC's DHCP address, gateway, and DNS.
- **2:00–2:50:** Open `http://intranet.corp.local` and explain DNS/HTTP.
- **2:50–3:30:** Demonstrate sending/receiving an email.
- **3:30–4:20:** Demonstrate one prepared failure and restore it.
- **4:20–5:00:** Show actual test results and conclusion.

## Viva questions and answers
1. **What is a VLAN?** A logical Layer-2 broadcast domain.
2. **Why use separate departmental VLANs?** To separate broadcast domains and make management and access policies easier.
3. **What is subnetting?** Dividing an IP network into smaller networks.
4. **What does /24 mean?** A 24-bit network prefix, mask 255.255.255.0.
5. **What is a default gateway?** The router address used to reach other IP networks.
6. **What is an 802.1Q trunk?** A link carrying traffic for multiple VLANs using VLAN tags.
7. **What is router-on-a-stick?** Inter-VLAN routing through multiple router subinterfaces over one physical link.
8. **What is DHCP?** Dynamic Host Configuration Protocol; it provides client IP configuration.
9. **What is DORA?** Discover, Offer, Request, Acknowledge.
10. **Why is `ip helper-address` used?** It relays DHCP requests from a client VLAN to a DHCP server on another subnet.
11. **What is DNS?** A service that maps hostnames to resource records such as IPv4 addresses.
12. **What is an A record?** A DNS record mapping a hostname to an IPv4 address.
13. **What is HTTP?** A protocol for web requests and responses.
14. **What do SMTP and POP3 do?** SMTP sends email; POP3 retrieves email.
15. **What does ping test?** IP reachability using ICMP echo messages.
16. **Why might the first ping fail?** ARP resolution or initial convergence may delay the first reply.
17. **Why use centralized services?** To simplify configuration and administration.
18. **What is a single point of failure in this design?** The only router, switch, or an individual centralized server.
19. **Does a VLAN automatically provide complete security?** No; routed access controls and suitable switch controls may also be needed.
20. **Does the Flask dashboard prove Packet Tracer is working?** No. It is a separate logical model; Packet Tracer tests provide device-level evidence.
21. **What is packet loss?** The fraction of sent packets that fail to arrive.
22. **What is latency?** Time taken for data to travel between endpoints, often measured as round-trip time.
23. **What is jitter?** Variation in packet delay.
24. **How can reliability be improved?** Add redundancy, backups, monitoring, and tested recovery procedures.
25. **What should be done after a failure test?** Restore the service/link and rerun the relevant normal tests.
