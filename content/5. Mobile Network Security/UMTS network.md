## UMTS

**UMTS** (*Universal Mobile Telecommunications System*) is the third-generation (3G) mobile standard. While GSM was primarily designed around voice telephony, UMTS was designed with data as its central focus. Rather than replacing the 2G core network entirely, UMTS introduced a new radio access network while reusing and minimally modifying the existing 2G core network components.

### Key design principles

A fundamental architectural principle introduced with UMTS is the **separation between the Access Stratum** (*AS*) **and the Non-Access Stratum** (*NAS*). The AS encompasses all signalling protocols and procedures related to the radio access network, while the NAS encompasses those related to the core network. This separation was intentional: by decoupling the radio access protocols from the core network protocols, future evolutions of either component can proceed independently without requiring a redesign of the whole system.

### 3G architecture: RAN elements

The UMTS radio access network is called **UTRAN** (*UMTS Terrestrial Radio Access Network*) and introduces two new elements to replace the BTS and BSC of GSM.

- **Node-B**: the UMTS base station, equivalent to the BTS in GSM. Node-B is responsible for all functions required to send and receive data over the radio interface, which in UMTS is based on **CDMA** (*Code Division Multiple Access*) rather than the TDMA scheme used in GSM. Its functions include channel coding, spreading and despreading of outgoing and incoming frames, and modulation. Node-B is also responsible for **power control** across all active connections, adjusting transmission power to maintain link quality while minimising interference.
- **RNC** (*Radio Network Controller*): the main control element of the UTRAN, analogous to the BSC in GSM but with significantly expanded responsibilities. The RNC controls the radio resources of all Node-Bs connected to it and manages mobility. Because CDMA enables **soft handover** (a technique in which a UE is simultaneously connected to more than one Node-B during a transition between cells), the RNC has more complex functions than the BSC. There is also an additional **Iur** interface between RNCs, which enables coordination during soft handovers that span two different RNCs.
![[Pasted image 20260603103039.png]]
### 3G architecture: interfaces

The radio interface in UMTS is designated **Uu** and is based on CDMA, which is the primary technical novelty of the standard compared to GSM. Initially, both voice and data services used dedicated physical channels, each assigned a unique spreading code. Later releases introduced a shared-channel approach for data services through **HSPA** (*High-Speed Packet Access*), which significantly improved spectral efficiency for bursty data traffic.

The **Iu interfaces** connect the UTRAN to the core network. In the initial deployment of UMTS, these interfaces were based on traditional E1 telephone trunks, identical to the approach used in 2G. Over time, the Iu interfaces were migrated to IP-based transport for both user data and signalling, which required an architectural change in the CS core network.

### Transition to all-IP transport in the CS core

The migration of internal interfaces to IP transport led to the decomposition of the MSC into two separate functional entities:

- **MGW** (*Media Gateway*): replaces the circuit-based switching element within the MSC. The MGW is responsible for transporting media (voice) as flows of IP packets rather than over dedicated circuits.
- **MSC Server**: implements all the signalling functions that were previously part of the MSC. The MSC Server controls the MGW by instructing it to create, modify, and terminate media flows. The two elements communicate over the **Mc interface**, while MGWs interconnect over the **Nb interface**.

![[Pasted image 20260603103518.png]]

In this evolved architecture, all interfaces are based on IP transport with adaptation protocols to carry both media and signalling. The **Mc** and **Nb** interfaces enable the separation of the bearer plane (handled by the MGW) from the signalling plane (handled by the MSC Server).

### Integrated 2G and 3G architecture

The final 2G and 3G architectures are fully integrated: the GERAN (GSM radio access network) and the UTRAN (UMTS radio access network) both connect to the same shared CS and PS core networks. A single MSC Server and MGW pair can serve both GERAN and UTRAN subscribers simultaneously, as can the SGSN and GGSN for packet data. The HLR remains the central subscriber database for both generations.

![[Pasted image 20260603103851.png]]