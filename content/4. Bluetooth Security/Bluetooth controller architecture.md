## The controller part: top-down approach

### Controller-side HCI

On the controller side, the HCI handles the same boundary from the other direction. When the controller receives packets from the radio, it extracts the raw data and forwards it to the host via the HCI. When it receives commands from the host, it executes the corresponding radio-layer operations and generates events to confirm completion or report errors.

### Link Layer

The **Link Layer** (*LL*) is the BLE equivalent of the MAC sublayer in the OSI model. It manages the radio state machine and defines the operational role of the device at any moment: Central, Peripheral, Advertiser, or Scanner. It is responsible for:

- Managing connection timing and the frequency hopping sequence on data channels.
- Implementing the **TDMA** (*Time Division Multiple Access*) scheme: in a connected BLE piconet, the central node determines the instants at which peripheral nodes must listen and transmit. Communication is structured as **connection events**: at each event, one device transmits a packet at a predetermined time, and the other responds after a fixed interval. This polling-based schedule is entirely determined by the central node.
- Performing CRC error detection on received packets.
- Implementing AES-CCM link-layer encryption and integrity checking.

In Bluetooth Classic, the analogous function is performed by the **Link Manager** (*LM*) in conjunction with the Baseband layer. The Baseband layer spans the boundary between the physical and data-link layers of the OSI model and handles framing, modulation interfacing, and timing.

### Physical layer

#### Spectrum and channels

Both Bluetooth Classic and BLE use the **2.4–2.485 GHz UHF** (*Ultra High Frequency*) ISM band. This band is unlicensed and shared with other technologies, most notably 802.11 (Wi-Fi). The ISM band is therefore a congested spectrum, and both Bluetooth variants address interference through frequency hopping.

Bluetooth Classic (BR/EDR) uses **79 channels of 1 MHz each**, spanning from 2.402 GHz to 2.480 GHz, with a hopping rate of **1600 hops per second**. Each slot therefore lasts 1000 ms / 1600 = **0.625 ms**.

BLE uses **40 channels of 2 MHz each**. These are divided into two groups by function: 3 **advertising channels** (channels 37, 38, and 39) and 37 **data channels** (channels 0 to 36).
![[Pasted image 20260610183303.png]]
The three advertising channels are positioned strategically within the 2.4 GHz band to minimize interference from Wi-Fi. In the 2.4 GHz band, the three standard non-overlapping Wi-Fi channels in the US occupy approximately 2.412 GHz (channel 1), 2.437 GHz (channel 6), and 2.462 GHz (channel 11), each with roughly 20 MHz of bandwidth. BLE advertising channel 37 sits at approximately 2.402 GHz (near the lower edge of the band, below Wi-Fi channel 1), advertising channel 38 sits at approximately 2.426 GHz (between Wi-Fi channels 1 and 6), and advertising channel 39 sits at approximately 2.480 GHz (near the upper edge, above Wi-Fi channel 11). By distributing the three advertising channels across the band and placing them away from the center frequencies of the dominant Wi-Fi channels, the design maximizes the probability that at least one advertising channel is free of heavy interference at any given moment.

The 37 data channels use **adaptive frequency hopping**: once a connection is established, the central and peripheral hop across data channels in a pseudo-random sequence known to both parties, and the AFH algorithm avoids channels that have been identified as carrying significant interference.

#### Modulation

**Bluetooth Classic** uses two modulation schemes depending on the mode in use. The basic rate (BR) mode uses **GFSK** (*Gaussian Frequency Shift Keying*): the binary data signal (+1 or -1) is filtered through a Gaussian filter before frequency-shift keying, which smooths the transitions between symbols, reduces spectral sidebands, and lowers the interference footprint of the signal. The EDR mode uses **DQPSK** (*Differential Quadrature Phase-Shift Keying*) at 2 Mbps or **8-DPSK** (*8-state Differential Phase-Shift Keying*) at 3 Mbps. These phase-shift keying schemes encode more bits per symbol, achieving higher spectral efficiency and therefore higher data rates at the cost of reduced noise margin.

**BLE** uses GFSK throughout, at either 1 Mbps or 2 Mbps (Bluetooth 5.0+). The long-range coded PHY modes, introduced in Bluetooth 5.0, achieve 500 kbps or 125 kbps by adding forward error correction coding at the physical layer rather than changing the modulation.

#### Spread spectrum and frequency hopping

**Spread spectrum** is a transmission technique in which a signal occupies more bandwidth than the minimum required for the data rate alone. By spreading the signal energy across a wider frequency range, the power spectral density at any single frequency is reduced, making the signal more resistant to narrowband noise and interference. Spread spectrum also provides resilience against both unintentional interference (from other devices in the band) and intentional jamming.

The two primary spread spectrum techniques are **CDMA** (*Code Division Multiple Access*), which spreads the signal using a code sequence, and **frequency hopping**, which changes the carrier frequency on a per-slot basis.
![[Pasted image 20260611162216.png|575]]
Bluetooth uses **FHSS** (*Frequency Hopping Spread Spectrum*). The transmitter and receiver share a pseudo-random hopping sequence that determines which frequency channel is used in each time slot. External devices that do not share the hopping state will only interfere with a Bluetooth transmission in the fraction of slots where their operating frequency happens to coincide with the current hopping channel. From Bluetooth 1.2 onward, **AFH** allows the hopping algorithm to detect and exclude channels with high interference from the usable set, further reducing sustained collisions. A notable caution with AFH in dense environments is that if many Bluetooth devices are simultaneously trying to avoid the same congested channels, they can cluster on the remaining channels and create mutual interference there instead.

#### Baseband error correction

The **Baseband** layer in Bluetooth Classic spans the boundary of the physical and data link layers. It handles data before and after modulation and implements two complementary error control mechanisms.

**ARQ** (*Automatic Repeat Request*) operates as a stop-and-wait protocol: the transmitter sends a packet, computes a CRC over the packet content, and waits for an acknowledgment (ACK) from the receiver before sending the next packet. If the CRC check at the receiver fails, or if no ACK is received within the timeout, the transmitter retransmits. Retransmission attempts are bounded by a configurable limit, and a **flush timeout** defines the maximum time the radio holds a frame in its buffer before discarding it and moving on.

**FEC** (*Forward Error Correction*) allows the receiver to correct errors without requesting retransmission, by adding redundancy to the transmitted data. Bluetooth offers two FEC options:

- **1/3 rate**: each bit is transmitted three times. The receiver uses a majority vote to recover the original bit. This provides strong error correction at the cost of reducing usable throughput to one-third of the raw bit rate.
- **2/3 rate**: for every 10 data bits, 5 parity bits are appended using a shortened (15,10) Hamming code. This code can correct any single-bit error and detect any two-bit error within each 15-bit codeword, at a cost of 1/3 overhead.

The reason such a large fraction of physical capacity is devoted to FEC is that Bluetooth operates in an unlicensed, interference-prone band without any guarantee of channel quality. The wireless channel introduces bit errors that are not recoverable by simply retransmitting (since interference may persist), and for time-sensitive traffic types such as synchronous voice, retransmission is not acceptable at all. FEC allows the receiver to recover corrupted data in real time.

A process called **whitening** is applied before transmission to randomize the bit stream, ensuring that the probability of a 0 and a 1 are approximately equal. This prevents long runs of identical bits, which would create DC bias in the signal and cause synchronization problems in the receiver's clock recovery circuits.

The transmit processing pipeline on the sender side proceeds as: payload encryption, CRC generation, whitening, FEC encoding, pattern mapping, and then transmission via the RF interface. The receiver applies the inverse sequence.
![[Pasted image 20260611162851.png]]

## Link layer framing

### BT Classic frame structure

In Bluetooth Classic, all frames share a common structure consisting of three parts: an **access code**, a **packet header**, and a **payload**.

The **access code** (72 bits) serves two purposes: timing synchronization and piconet identification. Each piconet has a unique access code derived from the central node's address, which allows peripheral nodes to distinguish packets intended for their piconet from packets belonging to other piconets.

The **packet header** (54 bits, transmitted three times for redundancy, giving 54 bits in total after the 18-bit raw header is tripled) contains:

- **Address** (3 bits): identifies which of the up to 7 active peripheral nodes the packet is addressed to, or confirms the central node.
- **Type** (4 bits): identifies the packet type and implicitly the payload structure.
- **Flow** (1 bit): a flow control flag indicating whether the receiver's buffer is full and it cannot accept further data.
- **ARQN** (1 bit): the acknowledgment bit for the stop-and-wait ARQ protocol.
- **SEQN** (1 bit): a sequence number bit for the stop-and-wait protocol, used to detect duplicates.
- **CRC** (8 bits): a header error check covering the header fields.

The **payload** carries up to 2744 bits of data. Its internal structure depends on the type of logical link established (synchronous, asynchronous, etc.).

In BR mode, the entire frame, including the payload, is transmitted using GFSK at 1 Mbps. In EDR mode, the frame structure is extended: the access code and header are still transmitted in GFSK at 1 Mbps to maintain backward compatibility (legacy devices can detect and parse the header, then ignore an EDR payload they cannot decode), but the payload is preceded by a **guard time** and a **synchronization sequence** and is then transmitted at either 2 Mbps (using π/4-DQPSK) or 3 Mbps (using 8-DPSK). The guard time separates the GFSK portion from the PSK portion, allowing the receiver's demodulator to switch modes. Because the slot duration (625 µs) is unchanged in EDR, packing more bits into the same slot duration is what produces the higher net throughput.

### BLE frame structure

BLE packets have a single uniform frame structure, regardless of their content:

```
| Preamble (1 byte) | Access Address (4 bytes) | PDU (2–257 bytes) | CRC (3 bytes) |
```

The **preamble** (1 byte) is used by the receiver to synchronize its clock and automatic gain control to the incoming signal.

The **Access Address** (4 bytes) identifies the connection context:

- For **advertising packets**, the Access Address is fixed at the well-known value **0x8E89BED6**, which is the same for all BLE devices. This allows any scanner to receive any advertising packet.
- For **data packets** (exchanged within an established connection), the Access Address is a **randomly generated value negotiated during connection establishment**. Each connection has a distinct Access Address (the probability of two simultaneous connections sharing the same address is $2^{-32}$). This means that a device's actual MAC address is **not included in data packets**; it is only transmitted in advertising packets, which has privacy implications.

The **PDU** (*Protocol Data Unit*) field carries the actual content. Two PDU formats exist:

- **Advertisement Channel PDU**: contains a 2-byte Link Layer header, the 6-byte MAC address of the advertiser, and up to 31 bytes of advertising payload (BLE 4.x), or up to 255 bytes with advertising extension in BLE 5.0+.
- **Data Channel PDU**: contains a 2-byte Link Layer header, a 4-byte L2CAP header, a 3-byte ATT header, an ATT payload of 0–244 bytes (BLE 4.2+), and a 4-byte **MIC** (*Message Integrity Code*) when link-layer encryption is enabled.

The **CRC** (3 bytes) at the end of every frame provides data integrity verification at the link layer.

For reference, data payload capacity has grown across versions: BLE 4.0 supports 27-byte total PDU payloads (20 bytes available for application data); BLE 4.2+ extended this to 251 bytes total (244 bytes of application data).

## Bluetooth device addressing
Every Bluetooth device is assigned a unique **BD_ADDR** (*Bluetooth Device Address*), a 48-bit identifier standardized by IEEE using the same format as MAC addresses in Ethernet. The address is divided into three fields:

- **NAP** (*Non-significant Address Part*): the most significant 2 bytes (16 bits). Used in frequency hopping synchronization frames.
- **UAP** (*Upper Address Part*): 1 byte (8 bits). Together with the NAP, it forms the **OUI** (*Organizationally Unique Identifier*), which identifies the manufacturer. The UAP is also used as a seed value in several Bluetooth algorithms (e.g., for generating the hopping sequence and the access code).
- **LAP** (*Lower Address Part*): the least significant 3 bytes (24 bits). Allocated by the vendor. The LAP uniquely identifies an individual device within a manufacturer's range, and it appears in the access code of every transmitted frame in Bluetooth Classic.

![[Pasted image 20260611164650.png]]
## Comparison of BT Classic and BLE

The following table summarizes the key physical and link-layer parameters for BLE and Bluetooth Classic:

| Parameter | BLE | Bluetooth Classic |
|---|---|---|
| Frequency band | 2.4 GHz ISM (2.402–2.480 GHz) | 2.4 GHz ISM (2.402–2.480 GHz) |
| Channels | 40 channels, 2 MHz spacing | 79 channels, 1 MHz spacing |
| Channel usage | FHSS | FHSS |
| Modulation | GFSK | GFSK, π/4-DQPSK, 8-DPSK |
| Data rate | 2 Mbps (LE 2M PHY), 1 Mbps (LE 1M PHY), 500 kbps / 125 kbps (coded PHY) | 3 Mbps (8-DPSK EDR), 2 Mbps (π/4-DQPSK EDR), 1 Mbps (BR GFSK) |
| Max TX power | ≤ 100 mW (+20 dBm) | ≤ 100 mW (+20 dBm) |
| Data transports | Asynchronous connection-oriented, isochronous connection-oriented, asynchronous connectionless, synchronous connectionless, isochronous connectionless | Asynchronous connection-oriented, synchronous connection-oriented |
| Topologies | Point-to-point, broadcast, mesh | Point-to-point (piconet) |
| Positioning | Advertising-based presence detection, direction finding via AoA/AoD, RSSI-based distance estimation | None |

Both technologies use FHSS and the same 2.4 GHz band, and both organize channel access using a combination of frequency division and time division. The key architectural differences lie in the channel count and spacing, the modulation flexibility in Classic, the much lower power consumption profile of BLE achieved through sleep-centric connection design, and the expanded topology and positioning capabilities in BLE.

In Bluetooth Classic, the physical channel is the foundation for a hierarchy of link abstractions: the physical channel supports one or more physical links, each of which carries one or more logical transports (which can be synchronous, asynchronous, or isochronous), each logical transport in turn carrying one or more logical links, and finally L2CAP channels on top. Traffic from multiple logical links is multiplexed onto the physical link by a scheduling function in the resource manager, which assigns slots to each logical link.

In BLE, the same fundamental principle applies: all devices in a piconet share the same hopping pattern, and the central node controls medium access through a polling-based TDMA scheme. The central node determines the precise instants at which each peripheral must listen and respond, coordinating the entire piconet through a sequence of connection events.