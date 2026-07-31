## Main novelties of 4G
The fourth generation of mobile networks, standardised by 3GPP, introduced a fundamental redesign of both the radio access and the core network. The key design principles that differentiate 4G from its predecessors are:

- **All-IP architecture**: the entire system is built around IP as the universal transport. Both the user plane (carrying user data) and the control plane (carrying signalling) use IP-based protocols throughout. There is no longer a circuit-switched domain; voice calls in 4G are handled as IP packets using **VoLTE** (*Voice over LTE*).
- **Flat network architecture**: earlier generations had multiple hierarchical layers of network elements in the user plane path (e.g., BTS/NodeB, BSC/RNC, SGSN, GGSN in 2.5G/3G). 4G adopts a "flat network" concept that reduces this hierarchy to two nodes in the user plane: the base station (eNodeB) and the gateway. This reduces cost, latency, and management complexity.
- **Separation of control and user planes**: the EPC explicitly separates the control plane (handling signalling and state management) from the user plane (carrying actual data traffic). This allows each plane to scale and evolve independently.
- **RNC functions absorbed into the base station**: in 3G, the RNC was a separate element that handled radio resource management and handover coordination. In 4G, these functions are moved into the base station (eNodeB), further flattening the architecture.
- **Self-Organizing Network**: **SON** (*Self Organizing Network*) capabilities allow eNodeBs to auto-configure, reducing the need for manual configuration during deployment.
- **Flexible radio interface**: the LTE radio interface supports bandwidths ranging from 1.25 MHz to 20 MHz and can operate across many different frequency bands.

## System nomenclature: EPS, LTE, EPC, and SAE
The commonly used name for 4G technology is **LTE** (*Long Term Evolution*), but the complete 3GPP standard introduced in Release 8 is formally called the **EPS** (*Evolved Packet System*). The EPS consists of two components:

- **SAE** (*Service Architecture Evolution*), which defines the core network and is formally specified as the **EPC** (*Evolved Packet Core*).
- **LTE**, which defines the radio access network and is formally specified as the **e-UTRAN** (*Evolved Universal Terrestrial Radio Access Network*).

The naming can be summarised as: EPS = LTE (e-UTRAN) + SAE (EPC).
![[Pasted image 20260603111235.png]]
### Evolution toward the flat network
The progression from 2G to 4G represents a steady reduction in the number of network elements that user plane traffic must traverse. In 3GPP Release 6 (GSM/UMTS), user plane data passes through four elements: BTS/NodeB, BSC/RNC, SGSN, and GGSN. Release 7 introduced two intermediate steps. First, the **Direct Tunnel** option allowed the SGSN to be bypassed for user plane data, so that traffic flowed directly between the RNC and the GGSN, reducing the user plane to three elements. Second, an option to co-locate the RNC functionality within the NodeB further reduced the chain. By Release 8 (SAE/LTE), the user plane is reduced to just two elements: the eNodeB and the Serving/PDN Gateway. The control plane is reduced from three interfaces to two, with simplified signalling.
![[Pasted image 20260603111331.png]]
![[Pasted image 20260603111835.png]]

This progression also meant that in the LTE architecture, the interface count dropped significantly. In GSM/UMTS, the user plane required three sequential interfaces. In LTE, it requires only one. The control plane similarly went from three interfaces to two, with reduced signalling overhead.

The core network evolution across generations can be characterised as follows:
- **2G**: CS core only, connected to the PSTN.
- **2.5G/3G**: parallel CS and PS cores, with IP connectivity added alongside the circuit-switched infrastructure.
- **3G with IMS**: the **IMS** (*IP Multimedia Subsystem*) is introduced as a layer above the PS core to provide IP-based multimedia services, enabling IP-based voice as an alternative to circuit-switched calls.
- **4G EPS**: the CS core is eliminated entirely. A single all-IP packet core handles all services, with IMS providing voice and multimedia services over IP.

![[Pasted image 20260603112301.png]]
### SAE: Evolved Packet Core
The **EPC** is an all-IP core network designed to serve not only 3GPP radio access networks (LTE, UMTS, GSM/EDGE) but also non-3GPP access technologies such as WLAN and WiMAX, as well as fixed access (Ethernet, DSL, optical fibre). This technology-agnostic design makes the EPC the single unified connectivity platform for a wide range of access types.

The EPC provides:
- **Mobility**, including handover between different access technologies.
- **Policy management**, including unified charging across services.
- **Security**, including authentication and encryption.

### LTE/EPC architecture overview
The LTE/EPC architecture consists of the e-UTRAN radio access network and the EPC core network. The main elements are:

- **UE** (*User Equipment*)
- **eNB** (*evolved NodeB*)
- **MME** (*Mobility Management Entity*)
- **S-GW** (*Serving Gateway*)
- **P-GW** (*Packet Data Network Gateway*, also called PDN-GW)
- **HSS** (*Home Subscriber Server*)

The eNB connects to the EPC via the **S1 interface**, which is split into two logical sub-interfaces: **S1-UP** for user plane traffic (connecting the eNB to the S-GW) and **S1-CP** for control plane traffic (connecting the eNB to the MME). Adjacent eNBs are connected to each other via the **X2 interface** for handover coordination. The MME connects to the S-GW via the **S11 interface**, and to the HSS via the **S6 interface**. The S-GW connects to the P-GW via the **S5/S8 interface**. The P-GW connects to the Internet via the **SGi interface**.
![[Pasted image 20260603112322.png]]
Both the S1 and X2 interfaces are **logical connections transported over IP physical connectivity**: the underlying transport infrastructure is an IP network, and the logical interfaces are implemented as IP tunnels over this common transport.
![[Pasted image 20260603112455.png]]
### User Equipment (UE)
The UE encompasses any device used to access the LTE network: smartphones, tablets, USB modems, sensors, and so on. Internally, the UE consists of:

- A **UICC** (*Universal Integrated Circuit Card*) containing the **USIM** (*Universal Subscriber Identity Module*), which stores subscriber credentials, authentication data, and security keys, analogous to the SIM in GSM.
- The **TE** (*Terminal Equipment*), which is the physical device itself.

LTE UEs may also include a VoIP client for **VoLTE** (*Voice over LTE*) calls. Most commercial UEs support multiple antennas for **MIMO** (*Multiple Input Multiple Output*) operation, which improves throughput and reliability by transmitting and receiving on multiple antenna paths simultaneously. Most modern UEs are multi-standard devices that support GSM, HSPA, and LTE, including both **FDD** (*Frequency Division Duplexing*) and **TDD** (*Time Division Duplexing*) variants of LTE.

### eNB: Evolved Node B
The **eNB** is the base station of the e-UTRAN. Unlike in 3G, where the base station (NodeB) had limited intelligence and most control functions resided in the RNC, the eNB in LTE absorbs all the radio access control functions previously distributed between the NodeB and the RNC. This is the core of the flat network concept.

Each eNB manages one or more cells and is responsible for:

- **Radio Resource Management (RRM)**: including radio bearer control (managing the allocation of radio resources to individual connections), radio admission control (deciding whether to accept new connection requests based on current load), connection mobility control (managing the radio aspects of handover), and scheduling in both uplink and downlink.
- **IP header compression**: reducing the overhead of IP headers before transmission over the radio interface, which is important given the limited bandwidth of the air interface.
- **Data flow encryption**: encrypting user data at the PDCP layer before transmission.
- **MME selection**: when a UE requests connection to the network, the eNB selects an appropriate MME to handle the session.
- **Routing of user plane data**: forwarding user data packets to the S-GW over the S1-UP interface.
- **Scheduling and transmission of paging messages** (originated by the MME) and broadcast information (originated by the MME or the operations and management system).
- **Measurements for mobility and scheduling**: collecting and reporting radio measurements used to support handover decisions and adaptive scheduling.

For IP connectivity toward the EPC, the eNB acts as a Layer 2 relay, bridging the radio interface and the IP backhaul network.

Adjacent eNBs are interconnected via the **X2 interface**, which is used for handover management and inter-cell coordination functions. The X2 interface is self-configured: when an eNB is deployed, it automatically discovers its neighbours and establishes X2 connections without manual intervention, a key feature of the SON capability.

### Evolved Packet Core (EPC) elements

![[Pasted image 20260603112728.png]]

#### MME: Mobility Management Entity

The **MME** is the central control plane node of the EPC. It consolidates functions that in 2G/3G networks were distributed across multiple elements (MSC, SGSN, VLR). The MME is involved exclusively in the control plane and has no user plane data passing through it.

The MME maintains simultaneous connections with multiple UEs, eNBs, other MMEs (including those of different operators for roaming), S-GWs, and HSSs. Its main responsibilities are:

**Authentication and security**: working together with the HSS, the MME manages mutual authentication between the UE and the network, and derives the encryption and integrity protection keys used for both the control plane and the user plane.

**Mobility management**: when a UE registers with the network, the MME instructs the eNB and S-GW to allocate the necessary resources. It tracks the UE's location: when the UE is in idle mode, the MME stores the **Tracking Area** (a group of cells) that the UE has reported; when the UE is in active mode, the MME knows the specific eNB serving it. The MME is involved in handover procedures in coordination with eNBs, S-GWs, and other MMEs.

**User profile management and service connectivity**: the MME provides the basic IP connectivity for the initial exchange of messages between the UE and the network (the **default bearer**). It selects the appropriate PDN (i.e., the P-GW) to assign to each UE. When additional connectivity is requested by the network or the UE, the MME establishes a **dedicated bearer**, verifying the UE's subscription profile and services before authorising the allocation.

#### S-GW: Serving Gateway

The **S-GW** is the user plane anchor point for the e-UTRAN. Its primary function is to manage the **GTP-U** (*GPRS Tunnelling Protocol for the User Plane*) tunnels that carry user data between the eNB and the P-GW, and to reroute these tunnels when the UE moves between eNBs or between S-GWs.

The S-GW operates entirely based on commands received from the MME, P-GW, and **PCRF** (*Policy and Charging Rules Function*). Its main functions are:

- **Mobility anchor point**: during inter-eNB handovers within the same S-GW, the S-GW reroutes the data tunnel from the old eNB to the new eNB. During inter-S-GW handovers (when the UE moves to a cell served by a different S-GW), the MME tears down the tunnel from the old S-GW and establishes a new tunnel with the new S-GW, while the P-GW remains unchanged.
- **Data buffering for idle UEs**: when the P-GW receives downlink packets destined for a UE that is in idle mode (and therefore has no active radio connection), the S-GW buffers those packets and requests the MME to initiate the **paging procedure** to wake the UE.
- **Packet tagging for QoS**: the S-GW tags packets at the transport layer with appropriate QoS markings in both uplink and downlink directions.
- **Traffic statistics and charging**: the S-GW collects per-UE, per-PDN, and per-QoS-class traffic statistics used for charging.
- **Interworking**: the S-GW is involved in interworking with 2G and 3G systems, providing continuity when a UE hands over from LTE to GSM or UMTS.

#### P-GW: Packet Data Network Gateway

The **P-GW** is the edge node between the EPC and external IP networks. It is the point at which user IP traffic enters and exits the mobile network. Its main functions are:

- **IP address allocation**: the P-GW allocates IPv4 and/or IPv6 addresses to UEs, either statically or dynamically using DHCP.
- **IP flow mapping and GTP tunnels**: the P-GW maps IP flows to GTP tunnels toward the S-GW and enforces per-flow policies.
- **Packet filtering and traffic policing**: through its internal **PCEF** (*Policy and Charging Enforcement Function*) component, the P-GW filters IP traffic on a per-UE basis, applies QoS policies received from the PCRF, and calculates charging statistics based on active services in both uplink and downlink.
- **Data rate control** in the downlink direction.
- **Traffic interception**: legal interception functions.
- **Interworking with non-3GPP access**: the P-GW allows UEs to connect through non-3GPP access technologies such as WiMAX and WLAN, enabling a single IP session to be maintained across heterogeneous access networks.

#### HSS: Home Subscriber Server

The **HSS** is the central subscriber database of the 4G architecture. It performs the same basic functions as the HLR in 2G/3G networks: it stores permanent subscriber data (subscription profiles, service authorisation, authentication credentials) and tracks subscriber location at the level of the serving MME. The HSS implements the specific signalling protocols defined for the 4G architecture, including the **Diameter** protocol used on the S6 interface with the MME.

In practice, since most operators run multi-generation networks, the HLR and HSS functions are typically combined into a single physical platform that presents both the legacy SS7/MAP interfaces (for 2G/3G nodes) and the new Diameter interfaces (for 4G nodes), ensuring seamless roaming and service continuity across technologies.

## User plane protocols and IP packet delivery in LTE

### Protocol stack

The LTE user plane uses a layered protocol stack that spans from the UE to the external PDN. On the radio interface (LTE-Uu), between the UE and the eNB, the following protocol layers are present:

- **PHY** (*Physical Layer*): handles modulation, coding, and all physical transmission aspects.
- **MAC** (*Medium Access Control*): manages scheduling based on priority, multiplexing of data flows, and **HARQ** (*Hybrid Automatic Repeat Request*), a mechanism that combines forward error correction with retransmission for efficient error recovery.
- **RLC** (*Radio Link Control*): handles segmentation and concatenation of data units and provides error correction through **ARQ** (*Automatic Repeat Request*).
- **PDCP** (*Packet Data Convergence Protocol*): in the user plane, PDCP performs **IP header compression** to reduce the overhead of IP and TCP/UDP headers over the air interface; in the control plane, PDCP provides **encryption and integrity protection**.
- **RRC** (*Radio Resource Control*): manages radio resources, signalling connections, data connections, and handover procedures. RRC is a control plane protocol that operates over the radio interface.

Above the radio interface, user IP packets are transported across the core network using **GTP-U** (*GPRS Tunnelling Protocol - User Plane*). GTP-U encapsulates the user's IP packets inside a GTP header, which is itself transported over UDP/IP. This tunnelling mechanism is used on the S1-U interface (between eNB and S-GW), on the S5/S8 interface (between S-GW and P-GW), and on the X2 interface (between eNBs during handover).

![[Pasted image 20260603112815.png]]

### GTP-U tunnelling mechanism

GTP-U is a tunnelling protocol: it takes a user's IP packet (the **inner IP packet**) and wraps it inside a new IP/UDP/GTP-U header (the **outer headers**) for transport across the core network infrastructure. This approach keeps the user's IP address and traffic invisible to the intermediate core network nodes, which only see the outer tunnel headers.

Each GTP-U tunnel is identified by a **TEID** (*Tunnel Endpoint Identifier*), a 32-bit value that uniquely identifies the tunnel at the receiving endpoint. Two TEIDs are involved for each direction of communication: one identifies the uplink tunnel endpoint and one identifies the downlink tunnel endpoint.

In the LTE user plane, between the UE and the Internet, there are two GTP-U tunnels chained in sequence:

1. The **S1 GTP tunnel**: between the eNB and the S-GW, carried over the S1-U interface.
2. The **S5 GTP tunnel**: between the S-GW and the P-GW, carried over the S5 interface.

#### Uplink packet delivery (UE to Internet)

When a UE sends an IP packet to the Internet, the delivery proceeds as follows:

1. The UE generates an IP packet with source IP = UE's IP address and destination IP = Internet server. This packet is transmitted over the LTE-Uu radio interface to the eNB.
2. The eNB receives the inner IP packet and encapsulates it in a GTP-U header, creating an outer packet with source IP = eNB's IP address, destination IP = S-GW's IP address, and TEID = the uplink S1-TEID assigned to this UE's tunnel. The encapsulated packet is sent to the S-GW over the S1-U interface.
3. The S-GW receives the packet, strips the S1 GTP-U outer header (decapsulation), and re-encapsulates the inner IP packet in a new GTP-U header for the S5 tunnel, with source IP = S-GW's IP address, destination IP = P-GW's IP address, and TEID = the uplink S5-TEID for this UE's session. The re-encapsulated packet is sent to the P-GW.
4. The P-GW receives the packet, strips the S5 GTP-U outer header, and forwards the original inner IP packet (source IP = UE, destination IP = Internet) out to the Internet via the SGi interface.

#### Downlink packet delivery (Internet to UE)

When an Internet server sends an IP packet to the UE, the delivery proceeds in the reverse direction:

1. The P-GW receives an IP packet from the Internet destined for the UE's IP address. It identifies the corresponding UE session, encapsulates the packet in a GTP-U header for the S5 tunnel (source IP = P-GW, destination IP = S-GW, TEID = downlink S5-TEID), and sends it to the S-GW.
2. The S-GW receives and decapsulates the S5 GTP-U header, then re-encapsulates the inner IP packet in a GTP-U header for the S1 tunnel (source IP = S-GW, destination IP = eNB, TEID = downlink S1-TEID), and sends it to the eNB.
3. The eNB receives and decapsulates the S1 GTP-U header, recovering the original inner IP packet. It then schedules and delivers this packet to the UE over the LTE-Uu radio interface.
4. The UE receives the IP packet with destination IP = UE and source IP = Internet server.

The critical design point is that the UE's IP address is carried only in the **inner IP header** and is never exposed to the core transport infrastructure. The outer IP headers used for GTP-U tunnelling carry only the addresses of the core network nodes (eNB, S-GW, P-GW). This provides a form of address transparency and makes it straightforward to reroute tunnels during handover by simply updating the TEID and outer IP addresses at the relevant nodes, without any change to the UE's IP address or ongoing TCP/IP sessions.
