## The role of signalling

**Signalling** is the exchange of control information that allows a network to set up,
manage, and tear down communication services. It is distinct from **user traffic**, which
carries the actual content the user wants to transmit (voice, video, data). Signalling
carries the control information the network needs to make communication possible:
authentication, paging, handovers, location updates, session establishment, and radio
resource allocation. A useful intuition is that user traffic contains what the user wants
to communicate, while signalling coordinates the network that delivers it.

In classic telephone service, signalling is responsible for routing and establishing
circuits for calls. In IP telephony, signalling sets up media sessions. More generally,
signalling in networks serves three main purposes:

- **Setting up and tearing down services**: initiating and terminating voice calls, video
  calls, data sessions, and similar services.
- **Assigning resources to services**: allocating radio channels, transmission channels, and
  other network resources.
- **Modifying services**: managing events such as mobility (handovers, location updates) or
  service changes during an active session.

Most of the signalling protocols and procedures used in mobile networks derive from
telephone signalling developed for fixed networks. Mobile signalling builds on this
foundation and extends it with procedures specific to radio access and user mobility.

Signalling is divided into two categories based on where it flows:

- **User signalling**: communication between user terminals and the network, used to request
  services, indicate the called party, and receive status information from the network (such
  as call in progress, destination reached, etc.).
- **Network signalling**: communication among network elements, used for routing calls along
  available paths, allocating resources, providing supplementary services, and managing
  mobility.

### User signalling: the analog telephone interface

In the analog telephone system, user signalling is conveyed through physical electrical
states on the subscriber line rather than structured digital messages. The sequence of
events for a basic outgoing call on an analog interface is:

1. The user lifts the handset, applying a DC loop to the line (**phone pick up**).
2. The telephone signals the network that the line is in use (**line in use signal**).
3. The network responds with a **dial tone** (busy tone sound) to indicate it is ready.
4. The user dials the destination number; each digit is encoded as a pair of audio
   frequencies (**DTMF multi-frequency tones**), which the telephone sends to the network.
5. The telephone echoes the number tones back to the user for confirmation.
6. The network locates the destination and sends a **ringing current** to the destination
   terminal.
7. The calling user hears a **ringing tone** generated locally by the network.
8. When the destination answers, the network sends a **Hello** signal back, and the
   conversation begins.
![[Pasted image 20260601184516.png]]
### User signalling: ISDN and DSS1

With the introduction of **Integrated Services Digital Network** (*ISDN*), user signalling
moved from physical line states to structured digital messages. The ISDN interface provides
two types of logical channels: **B channels** (bearer channels), which carry user voice or
data traffic at 64 Kbps each, and a **D channel** (data channel), which is dedicated
exclusively to signalling.

![[Pasted image 20260602160733.png]]

The protocol stack for user signalling in ISDN is defined by the **Digital Subscriber
Signalling System No. 1** (*DSS1*), standardized in ITU-T recommendations Q.930, Q.931, and
Q.932. DSS1 messages are carried directly inside **Link Access Procedure on the D-channel**
(*LAPD*) frames at the data-link layer. This layered structure means that signalling
messages travel on a separate logical channel from user traffic, which is a significant
architectural advance over the analog interface.

The main DSS1 message types and their functions are:

| Message type | Function |
|---|---|
| SETUP | Call setup request |
| SETUP ACKNOWLEDGE | Acknowledgment of SETUP message |
| INFORMATION | Additional dialed digits for call setup |
| CALL PROCEEDING | Call in progress |
| ALERTING | Destination terminal ringing |
| CONNECT | Setup completed, call answered |
| CONNECT ACKNOWLEDGE | Acknowledgment of CONNECT message |
| PROGRESS | Call in progress (intermediate status) |
| DISCONNECT | Call disconnect request |
| RELEASE | Call release |
| RELEASE COMPLETE | Acknowledgment of RELEASE message |
| RESTART | Restart request of signalling procedure |
| RESTART ACKNOWLEDGE | Acknowledgment of RESTART message |
| INFORMATION | Information for call setup |

#### ISDN basic call setup

The sequence of messages for establishing a basic call with an ISDN interface is:

1. The calling user picks up the handset. The terminal sends a **SETUP** message to the
   network on the D channel.
2. The network responds with **SETUP ACKNOWLEDGE**, confirming it received the request.
3. The user dials the number; the terminal sends an **INFORMATION** message containing the
   dialed digits. The user hears the echo of number tones locally.
4. The network sends **CALL PROCEEDING**, indicating it is processing the call. These
   messages travel on Channel D.
5. The network forwards a **SETUP** message toward the destination terminal.
6. The destination network responds with **CALL PROCEEDING** and then **ALERTING** as the
   destination terminal starts ringing.
7. The calling terminal receives **ALERTING** and plays a ringing tone to the calling user.
8. When the destination user answers, the destination terminal sends **CONNECT** to the
   network, which forwards it back as **CONNECT** to the calling terminal, followed by
   **CONNECT ACKNOWLEDGE** in both directions.
9. Once the connection is established, voice traffic flows on **Channel B**, while signalling
   continues on Channel D.

#### ISDN call teardown

Call release in ISDN follows a three-way exchange:

1. The initiating terminal (either side) sends **DISCONNECT** to the network.
2. The network sends **RELEASE** to the initiating terminal and simultaneously forwards
   **DISCONNECT** to the other terminal.
3. Both terminals respond with **RELEASE COMPLETE**. The network releases all circuit
   resources.

Beyond the basic call, the ISDN DSS1 protocol also supports a large set of supplementary
services, including caller ID presentation and restriction, call forwarding variants, call
waiting, call hold, call transfer, conference calling, and closed user groups. These
services are negotiated through additional ISDN messages and form the basis for the
corresponding features in mobile networks.

### Network signalling: SS7

#### Overview

**Signalling System No. 7** (*SS7*) is the protocol stack used for network-level signalling
in telephone networks. Introduced in the late 1970s, it remains in operational use today,
particularly in 2G and 3G networks, and is present in interworking functions of modern
networks through legacy interconnection paths.

SS7 implements **out-of-band signalling**, also called **Common Channel Signalling**
(*CCS*): signalling messages travel on a dedicated, physically separate packet-switched
network, completely independent from the circuit-switched network that carries user voice
traffic. This separation is a fundamental architectural principle: the signalling network
and the user traffic network are distinct. Before SS7, older systems used **in-band
signalling**, where control tones traveled on the same channels as voice. Out-of-band
signalling is more secure, more efficient, and allows signalling to occur without tying up
a voice circuit.

The SS7 network is a **datagram network** with its own nodes and routing, entirely separate
from the voice switching nodes.

![[Pasted image 20260602161006.png]]
#### SS7 node types

Three types of nodes exist in the SS7 architecture:

- **Service Switching Points** (*SSP*): these are the telephone switches. They manage calls
  and services, establish and control voice circuits or sessions, and generate and consume
  signalling messages. SSPs are the points where the circuit-switched voice network and the
  SS7 signalling network meet.
- **Signal Transfer Points** (*STP*): these are the packet routers of the SS7 network. They
  forward signalling messages between SSPs, databases, and other network elements. STPs do
  not carry user voice traffic; they handle only signalling packets. They may also act as
  gateways between different SS7 networks.
- **Service Control Points** (*SCP*): these provide access to application-layer databases
  and services, such as number translation for toll-free numbers, calling card validation,
  and subscriber profile lookups. SCPs communicate with other SS7 nodes using structured
  interfaces called **primitives**, which provide access from one protocol level to another.

![[Pasted image 20260616172128.png]]
#### SS7 protocol stack

The lower three layers of the SS7 stack are collectively called the **Message Transfer Part**
(*MTP*). They provide functions analogous to the physical, data-link, and network layers of
the OSI model:

| SS7 layer | Main function | OSI equivalent |
|---|---|---|
| MTP-1 | Physical transmission (DS-0 channels, 56 or 64 Kbps) | Layer 1 |
| MTP-2 | Reliable link transport: error checking, flow control, sequence checking | Layer 2 |
| MTP-3 | Routing and network management: node addressing, alternate routing, congestion control | Layer 3 |

Above MTP, several upper-layer protocols handle specific services:

- **SCCP** (*Signalling Connection Control Part*): extends MTP-3 with additional addressing
  and connection-oriented transport capabilities. It is used by applications that need more
  than basic datagram delivery.
- **ISUP** (*ISDN User Part*): handles the signalling for basic circuit-switched calls and
  supplementary services. It runs above SCCP and is responsible for setting up, managing,
  and releasing voice circuits between switching points.
- **TCAP** (*Transaction Capabilities Application Part*): provides a framework for
  request-response transactions between application entities, used for database queries and
  intelligent network services.
- **OMAP** (*Operation, Maintenance and Administration Part*): supports network management
  operations.
- **ASE** (*Application Service Element*): provides application-layer interfaces for
  intelligent network services.

#### Basic call setup with SS7 and ISUP

In SS7, the call setup between two telephone exchanges uses ISUP messages. The sequence for
a basic call between a calling terminal (TE) connected to a local exchange (LE) and a
destination TE connected to another LE, with a transit station in between, proceeds as
follows:

1. The calling TE sends **SETUP** to its LE on the D channel (DSS1 user signalling).
2. The LE responds with **SETUP ACKNOWLEDGE**, and the calling TE sends **INFORMATION** with
   the dialed number.
3. The LE sends **CALL PROCEEDING** to the TE and simultaneously sends an **IAM** (Initial
   Address Message) over SS7 to the transit station.
4. The transit station forwards the **IAM** to the destination LE.
5. The destination LE sends a **SETUP** message to the destination TE (DSS1). The
   destination TE replies with **CALL PROCEEDING** and then **ALERTING** as it starts
   ringing.
6. The destination LE sends an **ACM** (Address Complete Message) back through the transit
   station to the originating LE, which forwards **ALERTING** to the calling TE.
7. When the destination TE answers, it sends **CONNECT** to its LE, which sends an **ANM**
   (Answer Message) back through the SS7 network to the originating LE. The originating LE
   sends **CONNECT** and **CONNECT ACKNOWLEDGE** to the calling TE.
8. A **Channel B** end-to-end circuit is now established and voice traffic flows between the
   two terminals.
9. To release the call, the initiating side sends **DISCONNECT** to its LE, which sends
   **REL** (Release) over SS7. The receiving LE sends **DISCONNECT** to its TE and responds
   with **RLC** (Release Complete) over SS7. Both TEs complete their local release exchange
   (RELEASE / RELEASE COMPLETE on the D channel).

![[Pasted image 20260602161411.png]]
#### Security considerations in SS7

SS7 was designed in an era when the telephone network was a closed system accessible only
to trusted operators, and security was not a primary design concern. As a result, SS7 lacks
proper authentication mechanisms: nodes in the SS7 network implicitly trust messages
received from other nodes, with no cryptographic verification of origin or integrity.

This design assumption became a serious vulnerability as the network grew and as access to
SS7 infrastructure became more widely available. Attackers who gain access to SS7 can
exploit these missing protections to:

- **Intercept and manipulate communications**: by exploiting call setup messages, an
  attacker can redirect calls or intercept voice traffic.
- **Track user location**: SS7 location management procedures can be queried by any node
  with SS7 access, allowing an attacker to determine the approximate geographic location of
  a subscriber.
- **Intercept SMS messages**: the same location tracking and call redirection techniques
  apply to SMS, enabling interception of text messages including those used for
  two-factor authentication.
- **Conduct denial-of-service attacks**: network management messages can be abused to
  disrupt service for targeted subscribers.
- **Commit fraud**: spoofed messages can be used to manipulate billing or unblock stolen
  devices.

Despite these vulnerabilities, SS7 remains in operational use today. Many telecom
infrastructures still rely on it because of legacy 2G and 3G networks, circuit-switched
voice services, global roaming interconnections, and the need for backward compatibility
with older devices. Even modern LTE networks may interact with SS7 through interworking
functions for roaming and legacy services. LTE primarily uses the **Diameter** protocol for
its own signalling, and 5G moves further toward HTTP/2 with TLS in a service-based
architecture. However, because operators must support legacy devices and because global
roaming infrastructure has evolved incrementally over decades, SS7 has not disappeared. The
long lifecycle of telecom systems means that trust assumptions embedded in SS7 remain
present in many operational networks, making SS7 security an active concern in mobile
network security today.
