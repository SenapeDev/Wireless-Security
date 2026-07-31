IEEE 802.11 is part of the broader **IEEE 802** family of standards for local area networks. Several characteristics are shared across all 802.11 variants:

- **Half-duplex operation**: A device cannot transmit and receive simultaneously on the same channel. The wireless medium is shared, and only one device should transmit at a time within a given coverage area.
- **Frequency bands**: The original and most common bands are **2.4 GHz** (part of the ISM band, which is unlicensed and shared with other technologies such as Bluetooth and microwave ovens) and **5 GHz** (part of the U-NII band). Newer standards, starting with Wi-Fi 6E and Wi-Fi 7, also support the **6 GHz** band, which offers more available spectrum and less congestion.
- **Medium access control**: All 802.11 variants use **CSMA/CA** (*Carrier Sense Multiple Access with Collision Avoidance*) as their MAC protocol, described in detail later.

## Evolution of 802.11

The standard has gone through multiple generations since its introduction in 1997, with each generation increasing maximum throughput and often adding support for additional frequency bands. The table below summarizes the main generations:

|Generation name|IEEE standard|Adopted|Max link rate|Frequency bands|
|---|---|---|---|---|
|(none)|802.11|1997|1-2 Mbit/s|2.4 GHz|
|(none)|802.11b|1999|1-11 Mbit/s|2.4 GHz|
|(none)|802.11a|1999|6-54 Mbit/s|5 GHz|
|(none)|802.11g|2003|6-54 Mbit/s|2.4 GHz|
|Wi-Fi 4|802.11n|2009|6.5-600 Mbit/s|2.4, 5 GHz|
|Wi-Fi 5|802.11ac|2013|6.5-6933 Mbit/s|5 GHz|
|Wi-Fi 6 / Wi-Fi 6E|802.11ax|2021|0.4-9608 Mbit/s|2.4, 5, 6 GHz|
|Wi-Fi 7|802.11be|2024|0.4-23059 Mbit/s|2.4, 5, 6 GHz|
|Wi-Fi 8|802.11bn|2028 (expected)|~100,000 Mbit/s|2.4, 5, 6 GHz|

Early versions such as 802.11b used **Direct Sequence Spread Spectrum** (*DSSS*) at the physical layer, where all hosts share the same chipping code. Starting with 802.11a and 802.11g, **OFDM** (*Orthogonal Frequency Division Multiplexing*) became the dominant physical layer technique. 802.11n introduced **MIMO** (*Multiple Input Multiple Output*), using multiple antennas at both sender and receiver to increase throughput significantly.

### Frequency bands and channel structure

The **2.4 GHz** band is divided into 14 channels, each 22 MHz wide, spaced 5 MHz apart. Because the channels overlap significantly, only three non-overlapping channels exist in most regulatory regions (typically channels 1, 6, and 11). Interference between overlapping channels is a practical concern in dense deployments. The 2.4 GHz band offers better range and wall penetration than higher frequencies, but supports slower data rates and is more congested due to the large number of devices and other technologies sharing it.
![[Pasted image 20260402212201.png]]

The **5 GHz** band offers 23 non-overlapping channels with no overlapping channel problem, enabling faster data transmission with less interference. Its shorter wavelength means reduced range and worse obstacle penetration compared to 2.4 GHz. The 5 GHz band is used exclusively by 802.11a, and also by 802.11n, 802.11ac, 802.11ax, and later standards.

The **6 GHz** band, introduced with Wi-Fi 6E, provides additional spectrum with even more non-overlapping channels, further reducing congestion in high-density environments.

## The 802.11 frame format

### Frame structure
![[Pasted image 20260403113409.png]]

The **frame control** field encodes the frame type (data, RTS, CTS, ACK, beacon, etc.) and subtype, along with control flags including To AP, From AP, Retry, Power Management, More Data, WEP, and More Fragments.

The **duration** field carries the **NAV** value: the amount of time (in microseconds) the channel is reserved for the current exchange. Stations that receive a frame update their NAV timers accordingly and defer transmission.

The **sequence control** field contains a sequence number used to detect and discard duplicate frames in case of retransmission.

### Addressing

802.11 frames use up to four address fields, which serve different roles depending on the direction of the frame and the network topology.

- **Address 1**: the MAC address of the wireless device or AP that is the immediate recipient of this frame.
- **Address 2**: the MAC address of the wireless device or AP that is transmitting this frame.
- **Address 3**: the MAC address of the router interface to which the AP is connected on the wired network side.
- **Address 4**: used only in ad-hoc (mesh) mode; not used in standard infrastructure networks.

To illustrate why three addresses are needed in infrastructure mode, consider a station H1 sending a packet to the Internet through an AP connected to router R1. The 802.11 frame carries: 
- Address 1 = AP's MAC (the next wireless hop)
- Address 2 = H1's MAC (the sender)
- Address 3 = R1's MAC (the ultimate wired destination)

When the AP forwards the packet onto the wired network, it constructs a standard 802.3 Ethernet frame with R1's MAC as the destination and H1's MAC as the source. The AP uses Address 3 from the 802.11 frame to know where to forward the packet on the wired side.

## Advanced capabilities

### Rate adaptation

As a station moves and its distance from the AP changes, the Signal-to-Noise Ratio of the link varies. Lower SNR means higher bit error rates (BER) for a given modulation scheme. 802.11 devices implement **rate adaptation**: they dynamically select the physical layer modulation and coding scheme to match the current channel quality.
![[Pasted image 20260403114015.png|460]]
At high SNR, high-order modulation schemes such as **256-QAM** (Quadrature Amplitude Modulation) can be used, encoding many bits per symbol and achieving high throughput. As SNR decreases, the device falls back to less aggressive schemes such as **16-QAM**, **QPSK**, or **BPSK**, which encode fewer bits per symbol but are more robust to noise. The AP and station continuously monitor the channel and adjust the transmission rate accordingly. This mechanism ensures that link reliability is maintained as conditions change, at the cost of reduced throughput when the channel is poor.

### Power management

802.11 includes a **power management** (*PM*) mechanism that allows stations to enter a low-power sleep state between beacon intervals, which is important for battery-operated devices.

When a station wants to sleep, it notifies the AP by setting the Power Management bit in a transmitted frame. The AP acknowledges this and begins **buffering** any frames destined for that station rather than transmitting them immediately. The station then enters a doze state.

Before each beacon interval, the station wakes up to receive the beacon frame. The beacon contains a **Traffic Indication Map** (*TIM*), which lists the AIDs of stations for which the AP has buffered frames. If the station's AID appears in the TIM, the station sends a **PS-Poll** frame to retrieve its buffered frames and remains awake to receive them. If its AID does not appear, the station goes back to sleep until the next beacon.

This mechanism raises a security concern: because the power management state is signaled in unprotected management frames (at least in older protocol versions), an attacker can **forge power-save notifications** on behalf of legitimate stations. By sending spoofed frames that tell the AP a station has gone to sleep, the attacker causes the AP to buffer frames destined for that station indefinitely, effectively preventing the station from receiving traffic. From the victim station's perspective, its network connectivity is disrupted even though it is awake and operating normally. This constitutes a DoS attack exploiting the power management feature. The attack is inexpensive to carry out because the attacker only needs to inject a small number of management frames, and it is effective because the AP has no way to verify the authenticity of the power-save notification in the absence of management frame protection. Later additions to the standard, such as **Management Frame Protection** (*MFP*) introduced in 802.11w, address this by cryptographically authenticating management frames, preventing such spoofing.