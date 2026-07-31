## Network signalling: SS7 and MAP
Signalling in mobile networks encompasses the exchange of control messages between network elements to establish calls, manage mobility, and coordinate resources. In GSM and UMTS, the core network signalling is based on **SS7** (*Signalling System No. 7*), the standard signalling protocol suite used in traditional telephone networks worldwide.

![[Pasted image 20260603105827.png]]

SS7 is a layered protocol stack. At the bottom, the **MTP** (*Message Transfer Part*) provides three levels of functionality corresponding roughly to the physical layer (MTP level 1), the data link layer (MTP level 2), and the network layer (MTP level 3). Above MTP, the **SCCP** (*Signalling Connection and Control Part*) provides additional routing and connection-oriented services. Two application-level protocols sit above SCCP and MTP:

- **ISUP** (*ISDN User Part*): handles the establishment, maintenance, and teardown of voice calls between switching centres. In the mobile network, ISUP is still used for call routing between MSCs and for rerouting calls during inter-MSC handovers.
- **TCAP** (*Transaction Capabilities Application Part*): provides a framework for invoking remote operations between network nodes, used as a transport for higher-level mobile application protocols.

On top of TCAP runs **MAP** (*Mobile Application Part*), the SS7 application protocol that contains all additional signalling functions needed for mobile networks. MAP is responsible for the procedures that have no equivalent in the fixed telephone network: location updates, subscriber data retrieval, authentication coordination, and handover signalling between MSCs. MAP runs on the MSC, GMSC, and HLR, enabling these entities to exchange mobile-specific information.

The **BSSAP** (*Base Station Sub-system Application Part*) handles signalling between the BSC and the MSC, covering radio resource management, paging, handover initiation, and security procedures.

## User signalling

In traditional SS7 telephone networks, a permanent dedicated signalling channel exists between each subscriber and the switching centre. In mobile networks, this is not feasible because there are too many potential subscribers and they are not always active. Instead, an **access procedure** is used to establish a temporary direct signalling channel between the UE and the MSC on demand.

Once a signalling channel is established, two main categories of procedures are executed over it:

- **CM** (*Connection Management*) procedures: handle the establishment, modification, and release of calls. These are functionally identical to their counterparts in traditional telephony.
- **MM** (*Mobility Management*) procedures: manage handovers between cells and location updates, which are functions unique to mobile networks.

### Radio access signalling

In addition to user and network signalling, a separate layer of radio access signalling manages the radio resources within the RAN. This involves three main protocols:

- **RR** (*Radio Resource Management*) protocol: involves the UE, BTS, and BSC in allocating and releasing radio channels.
- **BTSM** (*BTS Management*): used by the BSC to send configuration and management commands to the BTS.
- **BSSMAP** (*BSS Mobile Application Part*): operates between the BSC and the MSC to handle paging, handover coordination, and security procedures.