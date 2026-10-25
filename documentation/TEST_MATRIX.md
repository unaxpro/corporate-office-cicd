# Test Matrix — Corporate Office Network

Fill the actual result and status after each test. Keep screenshots for important results.

## Functional tests
| ID | Test | Procedure | Expected result | Actual result/status |
|---|---|---|---|---|
| F1 | VLAN configuration | Run `show vlan brief` | VLANs 10,20,30,40,50 exist with correct ports | |
| F2 | Trunk | Run `show interfaces trunk` | Router link carries required VLANs | |
| F3 | Router interfaces | Run `show ip interface brief` | Subinterfaces are up/up | |
| F4 | DHCP HR | Set HR PC to DHCP | IP in 192.168.10.0/24, correct gateway/DNS | |
| F5 | DHCP Finance | Set Finance PC to DHCP | IP in 192.168.20.0/24, correct gateway/DNS | |
| F6 | DHCP IT | Set IT PC to DHCP | IP in 192.168.30.0/24, correct gateway/DNS | |
| F7 | DHCP Sales | Set Sales PC to DHCP | IP in 192.168.40.0/24, correct gateway/DNS | |
| F8 | Gateway reachability | Ping local gateway from each PC | Gateway responds | |
| F9 | Server reachability | Ping authorized server IP | Server reachable | |
| F10 | DNS | Browse to `http://intranet.corp.local` | Name resolves to web server and page loads | |
| F11 | Email | Send email from HR account to IT account | Message can be retrieved by recipient | |
| F12 | Cross-VLAN routing | Ping a PC in another department | Succeeds if no ACL blocks it; document intended policy | |

## Failure tests
| ID | Failure | Procedure | Expected result | Actual result/status |
|---|---|---|---|---|
| E1 | DNS failure | Turn DNS service off; access website by name and IP | Name resolution fails; direct IP may still work | |
| E2 | DHCP failure | Turn DHCP service off and attempt new lease | New DHCP allocation fails | |
| E3 | HTTP failure | Turn HTTP off | Web request fails; ping may still work | |
| E4 | Core link failure | Disconnect trunk | Routed access to other VLANs/services fails | |
| E5 | Recovery | Restore service/link | Normal tests work again | |

## Performance worksheet (only record measured values)
| Metric | Method | Test details/sample size | Measured value |
|---|---|---|---|
| Round-trip latency | Ping | Source, destination, probe count: | |
| Packet loss | Ping statistics | Sent/received/lost: | |
| DHCP success rate | Successful leases / attempts | Number of clients/attempts: | |
| DNS success rate | Successful lookups / attempts | Name and attempts: | |
| Service success rate | Successful web/email tests / attempts | Test details: | |
| Recovery time | Time from failure to restored service | Failure and measurement method: | |

Do not substitute expected values for measured results. If a metric cannot be measured in the chosen simulator, write “not measured” and explain why.
