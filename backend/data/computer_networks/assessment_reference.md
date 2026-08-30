# Computer Networks Assessment Reference

## OSI & TCP/IP Models
Layering separates responsibilities, while encapsulation adds headers as data moves downward. Real protocols do not always map perfectly to seven OSI layers.
## Physical & Data Link Layers
The physical layer moves signals; the data-link layer frames local delivery and detects errors. Error detection does not necessarily imply correction or end-to-end reliability.
## Ethernet, MAC & VLANs
Switches learn source MAC locations and forward using destination MAC tables. VLANs create separate broadcast domains; trunks carry multiple tagged VLANs.
## IP Addressing & Subnetting
A prefix divides network and host bits; CIDR supports variable prefixes and aggregation. Routers select the longest matching prefix, not the numerically closest address.
## ARP, ICMP & NAT
ARP resolves IPv4 next-hop addresses on a local link; ICMP reports diagnostics and errors. NAT translates addressing and often ports but is not inherently a firewall.
## Routing
Distance-vector shares path distance with neighbors, link-state distributes topology, and BGP exchanges policy-driven interdomain routes. Routing chooses paths; forwarding applies the chosen next hop.
## TCP
TCP provides ordered reliable byte streams using sequence numbers, acknowledgements, retransmission, flow control, and congestion control. Message boundaries are not preserved.
## UDP
UDP offers datagrams with checksum but no built-in delivery, ordering, or congestion guarantees. Applications may add their own reliability when latency needs justify it.
## DNS
Resolvers follow delegation and cache records by TTL. Recursive resolvers act for clients; authoritative servers answer for zones and are not necessarily the domain registrar.
## HTTP & HTTPS
HTTP is stateless at protocol level, while cookies and tokens add application state. HTTPS is HTTP over TLS and protects transit, not a compromised endpoint.
## TLS
Certificates bind identities to public keys through trust chains; the handshake authenticates and establishes session keys. Symmetric encryption normally protects bulk traffic after key exchange.
## Sockets & Client-Server Communication
A socket endpoint combines protocol, address, and port. TCP servers listen and accept new connected sockets; the listening socket does not carry each client stream.
## Firewalls & Network Security
Packet filters, stateful firewalls, proxies, VPNs, IDS, and IPS solve different problems. Segmentation and least privilege limit lateral movement.
## Wireless Networks
Wi-Fi shares radio spectrum, so channel overlap, interference, signal quality, and contention affect throughput. Association is distinct from IP configuration.
## Network Troubleshooting
Diagnose layer by layer: link, address, route, name resolution, transport reachability, TLS, then application. A successful ping does not prove the target service is healthy.
