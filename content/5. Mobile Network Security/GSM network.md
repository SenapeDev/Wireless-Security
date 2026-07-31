**GSM** (*Global System for Mobile Communications*) is the second-generation (2G) digital cellular standard that became the dominant mobile telephony technology worldwide. Understanding its architecture requires distinguishing between two major functional domains: the **radio access network**, which handles wireless communication between devices and the infrastructure, and the **core network**, which handles routing, mobility, and interconnection with other networks.

## First architecture: circuit-switched services
The original GSM architecture was designed exclusively for **circuit-switched** (*CS*) services, with voice telephony as the primary use case. In circuit-switched communication, a dedicated end-to-end path is reserved for the entire duration of a call, regardless of whether data is actually being transmitted at any given moment. This model mirrors that of the traditional telephone network.
![[Pasted image 20260602163245.png]]
The architecture is divided into two main segments: the **Radio Access Network** (*RAN*) and the **CS Core Network**.

### RAN elements
The radio access network contains the components responsible for managing the wireless link between users and the fixed network infrastructure.

- **UE** (*User Equipment*): also referred to as a Mobile Station in GSM terminology, the UE is the user's mobile device. It consists of a **TE** (*Terminal Equipment*), which is the physical handset, and a **SIM** (*Subscriber Identity Module*) card, which stores the subscriber's identity and authentication credentials.
- **BTS** (*Base Transceiver Station*): the GSM base station. The BTS manages the physical layer connection with UEs over the radio interface and executes resource allocation commands received from the BSC. It handles the actual transmission and reception of radio signals.
- **BSC** (*Base Station Controller*): the element responsible for implementing higher-layer protocols and managing all transmission resources across the BTSs connected to it. While the BTS handles the physical radio layer, the BSC operates at a higher level, controlling which radio channels are allocated, managing handovers within its area, and acting as the concentration point between the radio access and the core network.

### CS core network elements
The circuit-switched core network contains the elements responsible for call routing, subscriber data management, and interconnection with the public telephone network.

- **MSC** (*Mobile Switching Centre*): the functional equivalent of a telephone exchange in the mobile network. The MSC includes all control and signalling functions needed to manage calls and handle mobility. It routes calls to and from mobile subscribers and coordinates with other network elements during handovers.
- **VLR** (*Visitor Location Register*): a database that is logically and often physically co-located with the MSC. It stores temporary information about subscribers currently located within the area served by the associated MSC. When a UE enters a new MSC area, the VLR is populated with the relevant subscriber data so that the MSC can serve the user without having to query the central database for every transaction.
- **GMSC** (*Gateway MSC*): the MSC that connects the mobile network to external telephone networks, most notably the **PSTN** (*Public Switched Telephone Network*). The GMSC implements all the signalling interworking functions required to allow calls to be established between the mobile network and the fixed telephone network.
- **HLR** (*Home Location Register*): the central database of the mobile network. It stores permanent subscriber information (such as the subscribed services and the IMSI) as well as dynamic location information indicating which VLR currently serves a given subscriber. The HLR also incorporates an **AuC** (*Authentication Centre*), which stores the security credentials used to authenticate subscribers and generate encryption keys.

### Interfaces
The radio interface of GSM, designated **Um**, is based on a combined **FDM** (*Frequency Division Multiplexing*) and **TDM** (*Time Division Multiplexing*) scheme, described in detail later. The **Abis** interface connects BTSs to their controlling BSC, and the **A interface** connects the BSC to the MSC. Both Abis and A interfaces are based on classical telephone transport infrastructure, using 64 kb/s circuits carried over **E1** links running at 2.048 Mb/s, each E1 link carrying 32 circuits. The interfaces between the core network elements (MSCs, HLR, GMSC) similarly rely on classical telephone transport with circuit and signalling links.

## GPRS: extending GSM with packet-switched data

The original GSM architecture had no provision for packet-switched data services. To address this, **GPRS** (*General Packet Radio Service*) was introduced as an overlay on the existing GSM infrastructure. GPRS, along with its successor **EDGE** (*Enhanced Data rates for GSM Evolution*), introduced a **PS Core Network** (*Packet-Switched Core Network*) running in parallel with the existing CS core, enabling mobile data connectivity. The radio access network remained largely the same, with the addition of one new element.

![[Pasted image 20260602163653.png]]
### GPRS/EDGE architecture nodes

- **PCU** (*Packet Control Unit*): an additional module attached to the BSC. The PCU manages the protocols and radio resources specific to packet-switched data traffic, separating packet data handling from the circuit-switched functions of the BSC.
- **SGSN** (*Serving GPRS Support Node*): an IP router that plays, in the packet core network, a role analogous to the MSC in the circuit-switched core. Beyond standard IP routing, the SGSN has additional functions for managing the interfaces and protocols towards the radio access network, supporting mobility as UEs move between cells, and forwarding packets towards the GGSN. It maintains a **LR** (*Location Register*) that tracks which UEs are active in its serving area.
- **GGSN** (*Gateway GPRS Support Node*): the interworking node between the GPRS packet core and an external **PDN** (*Packet Data Network*), typically the Internet. The GGSN manages the activation of external IP connectivity for UEs, which includes assigning them an IP address when they establish a data session.

![[Pasted image 20260602163617.png]]

The GPRS architecture introduces new interfaces: the **Gb** interface connects the BSC/PCU to the SGSN, the **Gn** interface connects the SGSN to the GGSN, the **Gi** interface connects the GGSN to the external IP network, and the **Gr** interface connects the SGSN to the HLR for subscriber data retrieval.

## Combined 2G architecture

When both CS and PS services are present, the full 2G architecture combines the GSM circuit-switched infrastructure with the GPRS packet-switched additions. The radio access network in this combined configuration is referred to as **GERAN** (*GSM EDGE Radio Access Network*). A single GERAN connects to both the CS core (via the A interface to the MSC) and the PS core (via the Gb interface to the SGSN). The HLR serves both cores and is accessible by both the MSC (via the C and D interfaces) and the SGSN (via the Gr interface).
