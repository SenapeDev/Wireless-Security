The Bluetooth architecture is organized as a layered protocol stack. The stack is divided into two major functional blocks: the **[[Bluetooth controller architecture|Controller]]** and the **[[Bluetooth host architecture|Host]]**, separated by a standardized interface.
![[Pasted image 20260428104422.png|422]]
The **Host Controller Interface** (*HCI*) defines the boundary between the Controller and the Host. Below the HCI sits the Controller, which includes the physical layer and the lower data link layer components. These are typically implemented in dedicated hardware (the Bluetooth chip). Above the HCI sits the Host, which implements higher-layer protocols and application-facing interfaces, and is typically implemented in software running on the main processor.

### BLE protocol stack layers
The BLE single-mode stack consists of the following layers, from bottom to top:

- **LE PHY** (*Low Energy Physical Layer*): The physical layer defines the radio parameters for BLE. It uses the 2.4 GHz ISM band with 40 channels of 2 MHz width each. The modulation scheme is **GFSK** (*Gaussian Frequency Shift Keying*). The basic data rate is 1 Mbps; Bluetooth 5.0 added a 2 Mbps mode and a long-range coded PHY at 125 kbps or 500 kbps.

- **Link Layer**: The link layer sits immediately above the physical layer and implements the core state machine for BLE operation, including advertising, scanning, initiating connections, and maintaining connections. It controls the frequency hopping sequence, manages the connection timing, performs packet error detection via **CRC** (*Cyclic Redundancy Check*), and handles retransmission logic. It also implements **AES-CCM** (*Advanced Encryption Standard in Counter with CBC-MAC mode*) encryption at the link level.

- **L2CAP** (*Logical Link Control and Adaptation Protocol*): L2CAP provides protocol multiplexing, allowing multiple higher-layer protocols to share a single logical link. It also performs segmentation and reassembly of larger packets into the smaller PDUs that the link layer can transmit.

- **ATT** (*Attribute Protocol*): ATT defines a client-server model for data exchange. A device acting as a server exposes a set of **attributes**, each identified by a 16-bit handle and a **UUID** (*Universally Unique Identifier*). Clients read, write, or subscribe to notifications on these attributes. ATT is a simple, stateless protocol designed for small data exchanges.

- **GATT** (*Generic Attribute Profile*): GATT sits on top of ATT and defines how attributes are organized into **services** and **characteristics**. It defines the roles of GATT server (the device that holds the data) and GATT client (the device that reads or writes the data). GATT is the framework within which all BLE application data is structured.

- **SMP** (*Security Manager Protocol*): SMP runs in parallel with GATT and handles the pairing process, key generation, key distribution, and encryption setup between two BLE devices. It is responsible for establishing the cryptographic keys that the link layer uses for encryption and authentication.

- **GAP** (*Generic Access Profile*): GAP defines the highest-level control procedures: how a device makes itself discoverable, how it advertises its presence, how connections are established, and what roles devices assume (broadcaster, observer, peripheral, central). GAP is the layer that governs device discovery and connection management.

Above the GATT/GAP layer sit **application profiles**, which are standardized specifications defining how a particular application type uses BLE. A profile defines the roles of the devices involved, the services they use, and the data they exchange.

### Bluetooth Classic and dual-mode stacks
In Bluetooth Classic (BR/EDR single-mode), the stack uses the BR/EDR PHY, a **Link Manager** (*LMP*) in place of the BLE Link Layer, L2CAP, and then **RFCOMM** (*Radio Frequency Communication*) protocols that emulate serial port connections. RFCOMM enables legacy serial-port-based applications to run over Bluetooth without modification. The application layer in BR/EDR uses profiles built on top of RFCOMM or directly on L2CAP.

A dual-mode device runs both stacks. It has both a BR/EDR PHY and an LE PHY, both a Link Manager (for BR/EDR) and a Link Layer (for LE), and a shared L2CAP above both. Above L2CAP, it runs both the RFCOMM-based profile stack (for BR/EDR) and the GATT/GAP stack (for LE). A single HCI interface connects both stacks to the Host.

## BLE specifications: profiles, services, and characteristics
BLE functionality is organized through a three-level specification hierarchy.

### Bluetooth Core Specification
The **Bluetooth Core Specification** defines the complete architecture of the Bluetooth stack: the layers, their protocols, the formal procedures for key operations (pairing, connection establishment, encryption), and the data formats used at each layer. It is the normative technical reference for all BLE implementations.

### Profiles
A **profile** defines the rules for using BLE in a specific application context. It specifies:
- The **roles** of the devices involved (e.g., which device is the server and which is the client).
- The **behavior** expected from each role.
- The **data** that the server exposes and the client consumes.

For example, the Heart Rate Profile defines a heart rate monitor as a server that exposes heart rate measurements and a collector (e.g., a smartwatch) as the client that reads them. The profile specifies exactly which services and characteristics must be present on the server, what operations the client performs, and how the two devices interact.

### Services
A **service** is a collection of related data items grouped together on a GATT server. Services are identified by UUIDs (either 16-bit SIG-assigned UUIDs for standard services or 128-bit UUIDs for custom ones). Each service contains one or more **characteristics**.

### Characteristics and descriptors

A **characteristic** is the fundamental data unit in the GATT model. It has a value (the actual data, e.g., a heart rate reading of 72 bpm) and a set of properties that define how the client can interact with it (read, write, notify, indicate). Each characteristic may also have **descriptors**, which provide metadata about the characteristic, such as a human-readable name or configuration options for notifications.

For example, the Heart Rate Service contains at minimum a Heart Rate Measurement characteristic (which holds the current BPM value) and a Body Sensor Location characteristic (which describes where on the body the sensor is placed). A client connecting to a heart rate monitor discovers these characteristics through **GATT service discovery**, which is performed after connection establishment.

![[Screenshot from 2026-04-28 10-57-30.png]]
### Why service discovery happens after connection

A design question that arises naturally is why full service and characteristic information is not broadcast in advertising packets, so that clients could discover everything about a device before connecting. The answer lies in the constraints imposed by the advertising channel and the energy model of BLE.

Advertising packets are small (a maximum payload of 31 bytes in BLE 4.x, extended to 255 bytes in BLE 5.x with extended advertising), broadcast to all nearby devices, and transmitted frequently, sometimes every few tens of milliseconds. Including full service lists, characteristics, descriptors, and permission sets in advertising packets would make them far larger, increase transmission time, increase the probability of collisions on the advertising channels, and directly increase energy consumption. This contradicts the core design requirement of BLE.

Furthermore, most clients follow a filter-first model: a client discovers a device, reads the minimal information in the advertising packet (a short UUID list or a device name), decides whether the device is relevant, and only then connects. Full discovery is only warranted once interest has been established.

GATT service discovery is also inherently interactive: a client may browse services incrementally, request attribute handles, follow UUID references, and read descriptor values. This request-response pattern requires a connected, stateful channel that the broadcast advertising mechanism cannot provide.

The architectural separation is therefore clean and deliberate: **GAP** (the advertising layer) signals presence and provides a minimal summary of capabilities; **GATT** (the connected layer) provides the complete data model on demand. This split keeps advertising lean, scalable in dense environments, and energy-efficient, while still allowing full capability negotiation once a connection is formed.