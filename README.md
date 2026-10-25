# Corporate Office Network with Centralized Services

A beginner-friendly project scaffold adapted from the supplied Hotel Network Management System reference. It includes:
1. A real device-level network to build and verify in Cisco Packet Tracer.
2. An optional Flask dashboard that logically demonstrates DHCP, DNS, access policy, and failure scenarios.
3. Router/switch configuration templates, a report outline, a test matrix, demo plan, and viva questions.

## Important distinction
The Flask companion is a logical model. It does not control Packet Tracer, inspect the `.pkt` file, or transmit real packets. Verify network behavior separately in Packet Tracer. Do not report performance values until measured.

## Proposed topology
- 1 Cisco router (e.g. 2911)
- 1 managed switch (e.g. 2960)
- 4 departmental PCs: HR, Finance, IT, Sales
- 4 servers: DHCP, DNS, internal web, email
- Router-on-a-stick inter-VLAN routing
- VLANs 10, 20, 30, 40, 50
- DHCP relay from departmental VLANs to the central DHCP server

## IP plan
| Department/service | VLAN | Subnet | Gateway / server IP |
|---|---:|---|---|
| HR | 10 | 192.168.10.0/24 | 192.168.10.1 |
| Finance | 20 | 192.168.20.0/24 | 192.168.20.1 |
| IT | 30 | 192.168.30.0/24 | 192.168.30.1 |
| Sales | 40 | 192.168.40.0/24 | 192.168.40.1 |
| Servers | 50 | 192.168.50.0/24 | 192.168.50.1 |
| DNS server | 50 | — | 192.168.50.10 |
| DHCP server | 50 | — | 192.168.50.11 |
| Web server | 50 | — | 192.168.50.20 |
| Email server | 50 | — | 192.168.50.30 |

All subnets use mask `255.255.255.0`. Servers use static addresses and gateway `192.168.50.1`.

## Build order
1. Build and cable the topology following `packet_tracer/BUILD_IN_PACKET_TRACER.md`.
2. Configure switch VLANs and trunk.
3. Configure router subinterfaces.
4. Configure static IPs on servers.
5. Configure DHCP pools and router DHCP relay.
6. Configure DNS, HTTP, and email.
7. Set PCs to DHCP.
8. Test connectivity and services.
9. Run failure tests and record actual outcomes.
10. Optionally run the Flask companion dashboard.

## Physical port map (adjust if your device labels differ)
- Router G0/0 ↔ Switch Fa0/1 (trunk)
- HR PC ↔ Fa0/2 (VLAN 10)
- Finance PC ↔ Fa0/3 (VLAN 20)
- IT PC ↔ Fa0/4 (VLAN 30)
- Sales PC ↔ Fa0/5 (VLAN 40)
- DNS server ↔ Fa0/6 (VLAN 50)
- DHCP server ↔ Fa0/7 (VLAN 50)
- Web server ↔ Fa0/8 (VLAN 50)
- Email server ↔ Fa0/9 (VLAN 50)

## Run the Flask companion on macOS
Open Terminal and run:

```bash
cd Corporate_Office_Network_Project/python_gui
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python app.py
```

Then open `http://127.0.0.1:5000`. Stop the app with `Ctrl+C`.

Run automated tests:

```bash
python -m unittest discover -s tests -v
```

## Packet Tracer limitations
Packet Tracer service names and support can vary by version. Configure and test each service in your own file. The archive does not include a newly generated `.pkt` file; build and save your own Packet Tracer topology.

## Managing PCs in the dashboard

The Python dashboard lets you grow or shrink each department:

- **Add PC** (in any department card) opens a dialog: pick a name (optional) and how many PCs (1-10). Blank names are auto-numbered (HR PC 2, HR PC 3...).
- **Trash icon** removes a PC (click twice to confirm). Its DHCP lease is released and the address becomes free for reuse.
- **Tag icon** requests a DHCP address for that PC; **Assign IPs to all** does it for every PC.
- **Default PCs** restores the original four PCs.
- Rules: up to 12 PCs per department, and every department keeps at least one PC.
- PCs in the same department share a VLAN, so they can reach each other through the switch (even if the trunk is down). Traffic between departments stays blocked by the demo policy.
- PCs live in memory only, so restarting the app returns to the default four. This models the network; add matching PCs in Packet Tracer yourself.
