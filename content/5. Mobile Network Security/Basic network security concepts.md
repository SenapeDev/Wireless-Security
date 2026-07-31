## Wireless communication networks

A **wireless communication network** is a computer network in which some or all of the connections between nodes are established over a wireless medium rather than through physical cables. Wireless connectivity is used both to interconnect separate telecommunications networks and to provide network access to individual devices within business or residential environments, avoiding the cost and constraint of cabled infrastructure.

The range of systems that fall under this definition is broad. Common examples include:

- **Cellular networks**, which provide wide-area mobile connectivity through base stations managed by mobile network operators.
- **Wireless local area networks (WLANs)**, which provide short-range connectivity within homes, offices, and campuses, typically using Wi-Fi technology.
- **Wireless ad-hoc networks**, which are formed directly between devices without a fixed infrastructure.
- **Wireless sensor networks**, consisting of distributed low-power devices that collect and relay environmental data.
- **Vehicular communication networks**, which support communication between vehicles and between vehicles and roadside infrastructure.
- **Satellite communication networks**, which relay signals over long distances using orbiting satellites.

## Network infrastructure

### Wired communication infrastructure

In traditional wired networks, user equipment is referred to as **fixed communication terminals** because of the limited mobility imposed by physical cabling. Each device connects directly to a network switch or router through a dedicated cable. This model remains dominant in environments where high throughput and stability are required, such as data centers and cloud computing facilities, where servers are arranged in racks and interconnected through Top-of-Rack (ToR) switches, aggregate switches, and core switches using copper wire or fiber optic links.

The core network itself, even in predominantly wireless deployments, remains wired: the high-capacity backbone connecting routers, switches, and gateways is built on physical media that offer bandwidth and reliability difficult to match wirelessly.

### Wireless communication infrastructure

In wireless communication systems, the wireless medium is used almost exclusively **at the edge** of the network, that is, for the last segment between user equipment and the fixed infrastructure. The core network behind that edge is typically wired.

To support wireless access, additional components and resources must be introduced on top of the wired core:

- **Wireless transceivers**: the physical radio devices that provide wireless connectivity to user equipment. Depending on the technology, these are called base stations, access points (APs), mobile stations (MSs), or similar.
- **Management entities**: software and hardware systems responsible for mobility management (tracking users as they move), power management (controlling transmission power levels), radio resource management (allocating spectrum and channels), and security management.
- **Spectrum**: the radio frequency bands allocated for data transmission. The choice and management of spectrum directly affects capacity, range, and interference.
- **Deployment strategies**: techniques such as spectrum reuse that allow the same frequencies to be used in different geographic areas without interference, enabling scalable network design.

## Classification of wireless communication systems

Wireless systems can be classified according to three main criteria: **coverage**, **topology**, and **mobility**.

Coverage distinguishes between systems designed for personal-scale, local-scale, or wide-area-scale communication. Topology refers to the structural organization of nodes, distinguishing infrastructure-based systems from ad-hoc arrangements. Mobility describes whether the devices using the network are stationary, portable (moved but used in place), or fully mobile (used while in motion).

These three dimensions together define the principal categories of wireless networks: Wireless Personal Area Networks (WPANs), Wireless Local Area Networks (WLANs), and Wireless Wide Area Networks (WWANs).

### Wireless personal area networks (WPANs)

A **Wireless Personal Area Network (WPAN)** is designed for communication among devices within the immediate personal environment of a user, typically within a range of a few meters. WPANs commonly use an **ad-hoc topology**, meaning that devices communicate directly with each other without relying on a pre-existing fixed infrastructure.

Two structural modes exist for ad-hoc WPANs:

- **Central-peripheral mode** (also called master-slave mode) organizes devices around a single central (master) node. The central node defines a **piconet**, which is the basic unit of a WPAN. All peripheral (slave) nodes within the piconet connect exclusively to the central device rather than to each other. This structure provides centralized coordination for channel access and timing. Bluetooth Classic operates in this mode, with a smartphone or computer acting as the master and peripherals such as headsets or keyboards acting as slaves.

- **Mesh mode** connects nodes directly to one another through wireless links without imposing a centralized cell structure. Each node may communicate with multiple neighbors, and data can be relayed hop-by-hop across the network. This topology improves resilience and coverage but requires more complex routing protocols.

### Wireless local area networks (WLANs)

A **Wireless Local Area Network (WLAN)** is an infrastructure-based wireless system, meaning it relies on fixed network equipment to coordinate access. WLANs are built on top of an existing wired local area network and extend connectivity to wireless devices within a defined area.

The fundamental building block of a WLAN is the **Basic Service Set (BSS)**, which consists of a single **Access Point (AP)** and the set of client devices associated with it. The AP connects wirelessly to user devices and, through one or more Ethernet ports, to the wired LAN behind it. The wireless medium is **shared and broadcast**: any device within radio range of the AP can receive the frames being transmitted, regardless of whether it is the intended recipient. This property is a critical distinction from wired Ethernet, where frames are directed to specific ports.

When a deployment requires coverage over a larger area, multiple BSSs are interconnected to form an **Extended Service Set (ESS)**. In an ESS, all APs are interconnected, most commonly through wired backhaul. A user device may be within radio range of multiple APs simultaneously, but at any given moment it is associated with exactly one BSS. As the user moves through the area, the device may **roam** from one AP to another in a process called handover. The collection of BSSs forms a single logical network from the user's perspective, even though it spans multiple APs.

A typical deployment example is a campus Wi-Fi network, where dozens or hundreds of APs are distributed across buildings and outdoor areas, all interconnected through the campus wired network and managed as a unified ESS.

### Wireless wide area networks (WWANs)

A **Wireless Wide Area Network (WWAN)** provides the largest service coverage of all wireless communication categories, spanning cities, regions, or entire countries. Cellular networks (2G through 5G) are the primary examples. The architecture of a WWAN is organized into three functional levels.

**Radio level.** This is the outermost layer, directly interfacing with user equipment (UE) such as mobile phones, smart watches, or connected vehicles. UEs access the network through physical radio transceivers deployed in the infrastructure. Depending on the generation of cellular technology, these transceivers are called base stations, base transceiver subsystems (BTS), NodeBs (in 3G), or eNodeBs (in 4G LTE). A **Radio Network Controller (RNC)** bridges the radio and network levels: it manages spectrum allocation, controls transmission power, and regulates wireless access by multiple UEs.

**Network level.** This is the backbone infrastructure that interconnects all switching and routing elements. The **Mobile Switching Center (MSC)** operates at the boundary between the network and management levels. It functions as an intermediate switching system that manages mobility and tracks the location of mobile stations. It also enforces security by coordinating with the authentication center and equipment register at the management level to prevent unauthorized devices from accessing the network.

**Management level.** This level performs administrative and operational functions for the network service provider. Its components include:

- **Visitor Location Register (VLR)**: stores temporary information about UEs currently present in the MSC's service area.
- **Home Location Register (HLR)**: the permanent database of subscriber information and service profiles.
- **Authentication Center (AuC)**: stores cryptographic keys and generates authentication parameters to verify subscriber identity.
- **Operation and Maintenance Center (OMC)**: supports operational monitoring and maintenance of the network.
- **Equipment Register (EIR)**: maintains a database of device identities (IMEI numbers) used to identify and block stolen or unauthorized equipment.

## Network security

**Network security** is defined as the protection of networks and their services from unauthorized modification, destruction, or disclosure. It provides assurance that a network performs its critical functions correctly and without harmful side effects. Network security encompasses all devices, protocols, applications, and data that rely on the network, and it is shaped by the needs of individuals, the laws and regulations of a jurisdiction, and the policies of the organizations operating the network.

A foundational principle of network security design is that **a system must be assumed to be fully known to its adversaries**. The security of a system must not depend on the secrecy of its design. This principle, known as Kerckhoffs's principle and reinforced by practitioners such as Steve Bellovin (formerly of the NSA's National Computer Security Center), holds that the standard assumption should be that any new device or system has been reverse-engineered and its specifications are known to sophisticated attackers. Security through obscurity, relying solely on keeping the design secret, is not an acceptable defense.

### Generic security terminology

Understanding network security requires a common vocabulary. The key terms relate to each other as follows:

**Information** is the asset being protected. To protect it, a system defines **security requirements**, which specify what properties the information and the system must have (e.g., it must be kept confidential, it must not be altered without authorization). These requirements are achievable through certain **security abilities**, which are the technical and procedural capabilities a system can deploy (encryption, authentication mechanisms, access controls, etc.).

The opposing side is characterized by **security attacks**, which are deliberate actions taken against a system. Attacks exploit **vulnerabilities**, which are weaknesses in design, implementation, operation, or management. A **threat** is the potential for an attack to occur: it exists wherever there is a vulnerability and a plausible motivation or capability to exploit it.

## Security attacks

A **security attack** is a deliberate attempt to compromise a system by exploiting weaknesses in its design, implementation, operation, or management. Security work is fundamentally oriented around two goals: preventing attacks when possible, and detecting and recovering from attacks when prevention fails.

Attacks are formally classified into two categories by the ITU-T X.800 recommendation and IETF RFC 2828: **passive attacks** and **active attacks**.

### Passive attacks

Passive attacks involve observing or monitoring transmissions without interfering with them. The attacker does not alter data or disrupt services; instead, they gather information.

**Eavesdropping** is the most direct form of passive attack. The attacker positions themselves within the transmission range of a communication and captures the data being exchanged. In wireless networks, this is particularly easy because the radio signal is broadcast in all directions and any receiver within range can capture it without the communicating parties being aware.

**Traffic analysis** is a more subtle form of passive attack. Rather than focusing on the content of transmissions, the attacker analyzes patterns: who is communicating with whom, how frequently, at what times, and how much data is being exchanged. Even when the content is encrypted and unreadable, traffic analysis can reveal sensitive information about relationships, behaviors, and operational patterns. For example, a sudden increase in communication between two parties before an important event may be revealing even if none of the message contents can be decrypted.

Passive attacks are inherently **difficult to detect** because they involve no modification of data and no interaction with the system. The attacker leaves no trace in logs or traffic records.

### Active attacks

Active attacks involve some form of intervention in the communication or the system. Unlike passive attacks, active attacks modify data, inject new data, or disrupt services.

**Masquerade** (or impersonation) occurs when an attacker pretends to be a legitimate entity, such as an authorized user or a trusted network node. The attacker exploits weak identity verification to gain access to resources or to deceive other parties into trusting them. In wireless networks, MAC address spoofing is a common technique used to impersonate a legitimate device.

**Replay** attacks involve capturing a previously transmitted message and retransmitting it later to achieve an unauthorized effect. For example, an attacker who captures an authentication exchange can replay it to gain access without knowing the underlying credentials. The initial capture step typically relies on passive eavesdropping.

**Modification** attacks go further: the attacker intercepts a message, alters its content, and forwards the modified version to the intended recipient. The recipient receives what appears to be a legitimate message but with content that has been manipulated by the attacker. This attack directly violates data integrity.

**Denial of Service (DoS)** attacks aim to make a system's resources unavailable to authorized users. Rather than stealing or modifying information, the attacker disrupts the availability of a service. In wireless networks, DoS can be achieved by flooding a channel with traffic, sending forged management frames (such as deauthentication frames in Wi-Fi), or transmitting radio interference to disrupt the physical medium (jamming).

## Security services

**Security services** are the features a system provides to protect against attacks. They define what the system guarantees, not how those guarantees are achieved. The NIST computer security handbook identifies three core security services: **confidentiality**, **integrity**, and **availability**, often referred to together as the CIA triad. Additional services commonly included in security frameworks are **access control**, **authentication**, and **non-repudiation**.

### Access control

**Access control** regulates which entities are permitted to access which resources, and to what degree. Authorization is not binary: a legitimate user may have access to some resources but not others, depending on their role or clearance level. Access control systems enforce these policies after a user's identity has been established.

### Authentication

**Authentication** is the service that verifies the claimed identity of an entity before granting it access or trust. It applies to users connecting to a host system, to the host system itself (so users can verify they are talking to the legitimate server), and to individual messages (to confirm that a message genuinely originated from its claimed sender). Authentication is a prerequisite for meaningful access control: without it, there is no reliable basis for granting or denying access.

### Confidentiality

**Confidentiality** ensures that information is accessible only to entities that are authorized to see it. In practice, confidentiality is provided through **encryption**: data is transformed into an unintelligible form that can only be reversed by parties holding the correct key. In wireless networks, where the broadcast medium makes interception easy, encryption is an essential control for maintaining confidentiality.

### Integrity

**Data integrity** is the guarantee that information has not been altered, either accidentally or deliberately, during storage or transmission. An integrity service detects unauthorized modifications, deletions, or insertions. It does not prevent modification from occurring but provides the recipient with the means to recognize that the data they received does not match what was originally sent.

### Non-repudiation

**Non-repudiation** prevents an entity from denying that it performed a specific action, typically sending a message or entering into an agreement. It provides verifiable proof of the origin and content of a communication, so that the sender cannot later claim they did not send it or that the content was different. Non-repudiation is particularly relevant in transactional contexts such as electronic contracts and financial communications.

### Availability

**Availability** ensures that information and services are accessible to authorized parties when needed. It is the property most directly targeted by denial-of-service attacks. An available system continues to function and respond within acceptable parameters even under adverse conditions such as high load or attempted disruption.

## Security mechanisms

**Security mechanisms** are the technical methods and tools used to implement security services. While services define the security goals, mechanisms define the means. The X.800 standard defines the following principal mechanisms.

### Encipherment

Encipherment is the application of cryptographic algorithms to transform data into an unreadable form. It is the primary mechanism for providing **confidentiality**, but it also contributes to other services when combined with other mechanisms. Encipherment can be applied to data at rest or to data in transit.

### Authentication mechanisms

Authentication mechanisms provide procedures for verifying the identity of entities. This includes challenge-response protocols, cryptographic authentication exchanges, and the use of credentials such as certificates or pre-shared keys.

### Access control mechanisms

Access control mechanisms enforce authorization policies. They determine what an authenticated entity is permitted to do, based on its identity, its role, its membership in defined groups, or other attributes. They translate high-level access control policies into enforceable rules on system resources.

### Digital signature

A digital signature is a cryptographic mechanism that binds a message to the private key of its sender. It provides **proof of origin**: the recipient can verify that the message was produced by the holder of the corresponding private key and that the message has not been altered since it was signed. Digital signatures are the primary mechanism for non-repudiation.

### Data integrity mechanisms

Data integrity mechanisms detect unauthorized modifications to data. They typically operate by computing a value (such as a hash or a Message Integrity Code) from the data and attaching it to the transmission. The recipient recomputes this value upon receipt and compares it with the transmitted value; any discrepancy indicates tampering.

### Traffic padding and routing control

Traffic padding adds artificial data to transmissions to obscure the real patterns of communication, making traffic analysis more difficult. Routing control mechanisms allow data to be routed through network paths that are considered more secure, avoiding untrusted nodes or links.

### Notarization

Notarization involves the use of a trusted third party to record and certify properties of a communication, such as its origin, destination, time of transmission, and integrity. The notary's records can later be used to resolve disputes about whether a communication occurred and what it contained.

### Relationship between services and mechanisms

The table below maps each security service to the mechanisms that can be used to implement it. Multiple mechanisms are often combined to provide a single service.

|Security service|Mechanisms|
|---|---|
|Data confidentiality|Encipherment, routing control|
|Data integrity|Encipherment, digital signature, data integrity mechanisms|
|Authentication|Encipherment, digital signature, authentication exchanges|
|Non-repudiation|Digital signature, data integrity mechanisms, notarization|
|Access control|Access control mechanisms|

## Security threats specific to wireless networks

Wireless networks face a set of security challenges that do not exist, or are far less severe, in wired networks. These challenges arise directly from the physical properties of the wireless medium and the operational characteristics of wireless systems.

### Open and broadcast medium

Radio signals propagate through space in all directions and do not stop at physical boundaries such as walls, floors, or the perimeter of a building. Any device within radio range can passively receive transmissions without the communicating parties being able to detect this. In a wired network, an attacker must physically connect to a cable or port to intercept traffic. In a wireless network, interception requires only proximity and a suitable radio receiver. **Eavesdropping is therefore trivially easy by design**, and there is no wireless equivalent of the physical security that a closed wiring cabinet provides.

### No physical access control

Wired networks can enforce access control at the physical layer simply by controlling who has access to cables and ports. Wireless networks have no such mechanism. An attacker can transmit and receive frames from a car in a parking lot, a neighboring building, or any location within radio range. Access control must therefore be implemented entirely through logical mechanisms such as authentication protocols, since there is no physical barrier to stop an unauthorized device from attempting to communicate.

### Easy impersonation

Device identity in wireless networks is most often conveyed through the **MAC address**, a hardware identifier associated with the network interface. MAC addresses are not cryptographically protected at the link layer and can be trivially changed in software through a technique called **MAC spoofing**. An attacker who knows the MAC address of a legitimate device can configure their own interface to use that address, potentially bypassing MAC-based access controls or impersonating a trusted device. This makes **masquerade attacks** straightforward and gives rise to threats such as **rogue access points** and **evil twin attacks**, where an attacker sets up an AP that appears to be a legitimate one.

### Shared medium and contention

Wireless networks use a **shared medium**: at any given time, only one device in a given radio cell can successfully transmit, and all others must wait. The protocol used to coordinate this is typically **CSMA/CA (Carrier Sense Multiple Access with Collision Avoidance)**, a distributed mechanism that requires each device to independently decide when to transmit. There is no central enforcement point that can inspect or block transmissions before they occur. This means an attacker within range can **inject arbitrary frames** into the network without authentication, and can launch denial-of-service attacks by flooding the medium with traffic or by transmitting forged management frames such as deauthentication packets that force client devices to disconnect.

### Passive attacks are undetectable

Because passive attacks require no modification of traffic and no interaction with the network, they leave no trace. An attacker performing traffic analysis or capturing encrypted frames for later offline decryption cannot be detected through any network-level monitoring mechanism. This makes **confidentiality breaches difficult to discover**, and means that an attacker may have been collecting data for an extended period before any indication of a problem appears.

### Mobility and dynamic topology

Users in wireless networks are mobile: they join and leave the network, and they roam between access points as they move through a covered area. Each handover event requires the network to re-establish connectivity, update location information, and potentially re-run authentication and key establishment procedures. This creates a continuously changing network state that complicates **key management** and introduces potential **re-authentication vulnerabilities**. A poorly designed handover protocol may expose a window during which an attacker can inject frames, replay authentication messages, or redirect a user to a rogue AP.

### Heterogeneous and uncontrolled devices

Wireless networks, particularly WLANs and WWANs, are accessed by a large variety of personal devices that are not managed by the network operator. These devices may run outdated software, use weak configurations, or be compromised by malware. Unlike managed enterprise equipment, personal devices are outside the direct control of network administrators. This creates a **weak trust model** where the network cannot make strong assumptions about the security posture of the devices connecting to it, and the overall attack surface is correspondingly larger.

### Exposure to the physical layer

The wireless channel is inherently noisy and subject to interference from other radio sources, whether accidental or deliberate. **Jamming** attacks exploit this by transmitting radio energy on the frequencies used by the target network, degrading or completely blocking communication. Because the physical layer is accessible to anyone with appropriate radio equipment, availability attacks are difficult to prevent at the network or protocol level and may require physical countermeasures or frequency-hopping techniques to mitigate. The unreliability of the channel also demands that protocols be designed to cope with loss and retransmission, adding further complexity to security protocols that must remain robust under adverse radio conditions.