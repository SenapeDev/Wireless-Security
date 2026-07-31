## Overview and design philosophy
Bluetooth is a **short-range wireless communication** standard originally conceived in 1994 by Ericsson as a low-power replacement for physical cables connecting phones and accessories. It was designed with a narrow and specific goal: to eliminate short cables such as USB connections between devices, rather than to serve as a general-purpose wireless network. This design philosophy has shaped every architectural decision in the standard, from its network topology to its medium access control mechanisms.

Bluetooth is standardized under two complementary frameworks: **IEEE 802.15.1**, which provided the initial formal standardization, and the specifications maintained by the **Bluetooth Special Interest Group** (*SIG*), the industry consortium that drives ongoing development. The technology operates in the **2.4–2.5 GHz ISM** (*Industrial, Scientific, and Medical*) radio band, which is unlicensed and shared with other technologies such as Wi-Fi and microwave ovens. To coexist in this crowded band, Bluetooth uses **frequency hopping spread spectrum** (*FHSS*), changing its transmission frequency in a pseudo-random sequence on every time slot. This makes it robust against narrowband interference and reduces the probability of sustained collisions with other devices operating in the same band.

## Bluetooth versions and data rates
Bluetooth has gone through several major revisions since its first formal specification. These versions are divided into two distinct technology lineages:
- **Bluetooth Classic** (*BC*), also referred to as **Basic Rate** (*BR*) / **Enhanced Data Rate** (*EDR*), which covers versions 1.x through 3.x; 
- **Bluetooth Low Energy** (*BLE*), introduced in version 4.0, which is a fundamentally different standard with different protocol stacks, different physical layer parameters, and different target use cases.

### Bluetooth Classic (versions 1.x to 3.x)
The first formal specification, Bluetooth 1.0, was released in 1999. Version 1.1 added point-to-multipoint communication, and version 1.2 (2003) introduced **adaptive frequency hopping** (*AFH*), which allows the device to detect and avoid channels occupied by other interference sources instead of hopping across all 79 channels indiscriminately.

Bluetooth 2.0 (2004) introduced the **Enhanced Data Rate** (*EDR*) option, raising the maximum net data rate to approximately 2.1–2.4 Mbps. Version 2.1 (2007) improved the pairing security model, adding support for NFC-assisted pairing and a more robust **Secure Simple Pairing** (*SSP*) mechanism.

Bluetooth 3.0 (2009) nominally reached speeds of up to 24 Mbps, but accomplished this by using Bluetooth only for connection coordination while offloading actual bulk data transfer to a co-located 802.11 (Wi-Fi) radio. This is sometimes described informally as "cheating" because the throughput gain does not come from the Bluetooth radio itself.

The following table summarizes the maximum transmission rates across versions:

| Bluetooth version | Maximum transmission rate |
|---|---|
| 1.0a and 1.0b | 732.2 kbps |
| 1.1 | 732.2 kbps |
| 1.2 | 1 Mbps |
| 2.0 and 2.1 | 2.1 Mbps |
| 3.0 | 24 Mbps |
| 4.0 | 24 Mbps |
| 4.1 and 4.2 | 25 Mbps |
| 5.0, 5.1, and 5.2 | 50 Mbps |

### Bluetooth Low Energy (version 4.x onward)
Starting with version 4.0 (2010), Bluetooth development bifurcated. **Bluetooth Low Energy** (*BLE*) is an independent protocol standard, not an evolution of Classic Bluetooth. It has no backward compatibility with Bluetooth Classic unless a device implements a dual-mode stack that supports both.

BLE was designed for applications in healthcare, fitness monitoring, location beacons, home automation, and the broader **Internet of Things** (*IoT*) ecosystem, where devices may spend most of their time sleeping and only wake periodically to transmit small amounts of data. Its primary mechanism for achieving low energy is sleeping for long intervals between connection events, minimizing radio-on time.

BLE is not backward compatible with Bluetooth Classic. Devices that need to support both must implement a **dual-mode stack**, running both the BR/EDR and LE protocol stacks concurrently. The two modes coexist on the same physical device and can share the same radio hardware in some implementations.
#### Other improvements
Version 4.1 (2013) improved coexistence with LTE networks. Version 4.2 (2014) added support for IPv6 and **6LoWPAN** (*IPv6 over Low-Power Wireless Personal Area Networks*), enabling BLE devices to participate in IP-based networks directly.

Bluetooth 5.0 (2016) significantly extended BLE capabilities: it doubled the data rate (to 2 Mbps), quadrupled range through a new long-range physical layer mode, and increased advertising data capacity eightfold. Subsequent minor versions added location services with angle-of-arrival and angle-of-departure measurements (5.1), LE Audio and **EATT** (*Enhanced Attribute Protocol*) (5.2), advertising enhancements (5.3), and **PAwR** (*Periodic Advertising with Responses*) along with **EAD** (*Encrypted Advertising Data*) for IoT use (5.4).

Bluetooth 6.0 (2024) introduced channel sounding for improved distance and angle estimation, further reduced power consumption, and refined the core specification in several areas relevant to localization and IoT deployments.

## Network topologies

### Piconet

The fundamental Bluetooth network unit is the **piconet**. A piconet is an ad-hoc network formed by one **central node** (historically called the master) and one or more **peripheral nodes** (historically called slaves). No fixed infrastructure such as access points or base stations is required; devices self-assemble into a piconet through a process called bootstrapping.
![[Pasted image 20260428102335.png]]
In Bluetooth Classic, a piconet supports up to **7 active peripheral nodes** simultaneously connected to one central node. All communication within a piconet is exclusively between the central node and a single peripheral at a time; peripheral nodes cannot communicate directly with each other. The central node controls all communication parameters, including which peripheral is communicating and when. This requires the central node to assign **temporary addresses** to peripherals so that it can reference them within the scheduling context of the piconet.

In BLE, there is no hard limit of 7 peripheral nodes. The number of peripherals is bounded only by the device's available resources (memory, processing capacity, and scheduling capability).

Because all traffic passes through the central node, two peripheral devices that need to exchange data must do so indirectly, via the path: Peripheral A → Central → Peripheral B. 
This is not a limitation that was overlooked in the design; it is a deliberate architectural choice. The reason two peripherals cannot communicate directly is fundamentally rooted in how Bluetooth controls access to the medium.

Bluetooth uses a **polling-based MAC** (*Medium Access Control*) layer in which the central node owns all time and frequency control. The central node determines which peripheral transmits, on which frequency, and at what time. Peripheral nodes have no synchronization with each other and no autonomy to access the medium independently. They cannot form the shared timing state required to communicate directly. This centralized control also means Bluetooth inherently avoids the **hidden terminal problem** that affects distributed MAC protocols like Wi-Fi's CSMA/CA: rather than solving contention among competing transmitters, Bluetooth eliminates the conditions that would create contention in the first place, by making medium access entirely centrally scheduled.

Parked (inactive) devices are a third category within a piconet. A peripheral node can enter **parked mode**, in which it gives up its active address and goes to sleep, retaining only a minimal association with the piconet. This allows many more devices to be associated with a piconet than are actively communicating at any moment, which is important for battery-operated devices that only need to transmit infrequently.

### Scatternet

A **scatternet** is formed by overlapping piconets. Because a peripheral node is not exclusively bound to a single piconet, it can participate in multiple piconets simultaneously or by time-multiplexing its presence. A node that acts as a peripheral in one piconet may simultaneously act as the central node of another, effectively bridging the two piconets and enabling data to flow across them.
![[Pasted image 20260428102812.png]]
The constraint is that a node can serve as the central node in only one piconet at a time. Cross-piconet communication in a scatternet requires routing procedures and the use of globally unique addresses to distinguish devices across piconet boundaries, since the temporary addresses used within each piconet are local to that piconet only.

## Medium access control in Bluetooth Classic

Bluetooth Classic combines two multiplexing techniques: **Time Division Multiplexing** (*TDM*) and **Frequency Division Multiplexing** (*FDM*).

Time is divided into **625-microsecond slots**. In each slot, only one device transmits; the central node and a given peripheral alternate in a time-division fashion. The central node polls peripherals in sequence, and a peripheral may only transmit in response to a poll from the central node.

Simultaneously, the frequency used for each slot changes according to a **pseudo-random frequency hopping sequence** known to all devices in the piconet. Bluetooth Classic uses **79 frequency channels** across the 2.4 GHz ISM band. BLE uses **40 channels** (3 advertising channels and 37 data channels). Because the hopping sequence is pseudo-random but deterministic (based on shared state), devices in the piconet stay synchronized, while external devices that do not share the hopping state can only interfere on a fraction of slots. This combination of TDM and FHSS is the basis for Bluetooth's coexistence properties in the ISM band.

The bootstrapping process by which a device discovers nearby Bluetooth devices, establishes a piconet, and sets up communication requires dedicated procedures for inquiry, paging, authentication, authorization, and establishment of encrypted links.