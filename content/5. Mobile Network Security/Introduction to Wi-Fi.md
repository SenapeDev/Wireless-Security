## Introduction to WLAN

A **Wireless Local Area Network** (*WLAN*) is a local area network that uses radio frequency transmission instead of physical cables to connect devices. The dominant WLAN technology in use today is **Wi-Fi**, a trademark of the Wi-Fi Alliance. The underlying technical standard for Wi-Fi is the **IEEE 802.11** family of specifications, which defines how wireless communication is conducted at the physical and data link layers.

### Network topologies
Wi-Fi supports two fundamental network topologies: **infrastructure mode** and **ad-hoc mode**.

- In **infrastructure mode**, one or more **Access Points** (*APs*) serve as central hubs. Wireless client devices, called **stations** (*STAs*), do not communicate directly with each other; instead, all traffic is routed through the AP. This constraint exists for two closely related reasons. First, two stations may not be within radio range of each other even if both can reach the AP, a situation known as the **hidden terminal problem**. If a station were to transmit directly to another station without knowing whether that station can hear it, collisions would be undetectable and unresolvable. Second, having all traffic pass through the AP gives the network a single, managed coordination point for medium access, addressing, and frame delivery. The performance implication is significant: the effective throughput for station-to-station traffic is halved, because the wireless channel must carry each payload twice, and the shared medium is occupied for twice as long per exchange.
- In **ad-hoc mode**, devices communicate directly with each other without any pre-deployed infrastructure. **Wi-Fi Direct** is a certification defined by the Wi-Fi Alliance for devices that support ad-hoc Wi-Fi communication, enabling direct device-to-device connections such as file transfers or screen sharing without an AP.

## Wi-Fi performance and goodput

### Why the physical layer rate is not the application layer rate

The data rates advertised for 802.11 standards (11 Mb/s for 802.11b, 54 Mb/s for 802.11g, 600 Mb/s for 802.11n, and so on) refer to the **physical layer bit rate**, which is the maximum speed at which bits can be transmitted over the radio channel under ideal conditions. This number tells you nothing directly about how much useful data an application will actually receive per second. The gap between the two is large and systematic, caused by a combination of protocol overhead, medium access contention, and the fundamental constraints of the shared wireless channel.

**Goodput** (G) is defined as the rate at which useful application-layer data is delivered to the receiver:

$$G = \frac{\text{useful data received at the application layer}}{\text{time to complete the transfer}} < C$$

where C is the physical layer capacity. Goodput is always strictly less than C, and in Wi-Fi networks the gap is significantly larger than in wired Ethernet.

### Sources of inefficiency in 802.11

Several distinct mechanisms reduce the goodput relative to the physical layer rate:

- **Shared medium and contention**: the wireless channel is shared among all stations. Only one station can transmit at a time, so channel time is divided across all active stations. During contention periods, the channel is idle.
- **Half-duplex operation**: a station cannot transmit and receive simultaneously. When the channel carries an ACK, it cannot carry data, and vice versa.
- **Control frame overhead**: every data exchange requires control frames (DIFS wait, backoff, ACK, and optionally RTS/CTS) that consume channel time but carry no application data.
- **Backoff idle time**: after each transmission, the sender must wait a random backoff period before contending again, leaving the channel idle.
- **Transmission errors and retransmissions**: bit errors cause frames to be lost and retransmitted, consuming channel time without delivering new data to the application.
- **Multi-rate environment**: in a network with devices operating at different data rates, control frames transmitted at the basic rate consume a disproportionately large share of airtime relative to the data they protect.

### Protocol layering and header overhead

Network communication is organized in layers, each of which adds its own header (control information) to the data it receives from the layer above. This encapsulation is recursive: the application data is wrapped by the transport layer (TCP or UDP), which is wrapped by the network layer (IP), which is wrapped by the data link layer (802.11 MAC and LLC), which is transmitted by the physical layer (the PLCP frame, including preamble and PHY header). Only the innermost application data constitutes useful payload; all headers are overhead that must be transmitted but contribute nothing directly to the application.

For a concrete baseline, consider a TCP/IPv4 transfer over wired Ethernet with Maximum Segment Size (MSS) of 1460 bytes. The per-packet overhead is 20 bytes (TCP) + 20 bytes (IPv4) + 38 bytes (Ethernet frame fields including preamble, MAC addresses, type field, FCS, and inter-packet gap), totaling 78 bytes of overhead per 1460 bytes of payload. The resulting efficiency is:

$$\eta = \frac{1460}{1460 + 78} = \frac{1460}{1538} \approx 94.2\%$$

This means Ethernet wastes roughly 6% of capacity on headers. For Wi-Fi the situation is considerably worse, for two reasons. First, the 802.11 MAC header is larger and more complex than the Ethernet header, with up to four MAC addresses and additional fields. Second, an **LLC (Logical Link Control)** sublayer is interposed between the MAC and the IP layer in 802.11 networks, adding 8 bytes per frame to multiplex different upper-layer protocols. Third, and most importantly, different parts of the 802.11 frame are transmitted at different data rates, which means overhead cannot be quantified purely in bytes; it must be computed in the **time domain**.

### Computing the theoretical maximum throughput of 802.11

Because control frames (RTS, CTS, ACK) and the PHY preamble and header are transmitted at the **basic rate** (as low as 1 Mb/s for backward compatibility) while the data portion is transmitted at the negotiated high data rate, each byte of overhead occupies much more channel time than each byte of data. The correct metric is therefore **airtime**, not bytes.

The **Theoretical Maximum Throughput (TMT)** at the 802.11 MAC layer is defined as:

$$TMT = \frac{\text{MSDU size}}{\text{Delay per MSDU}}$$

where the MSDU (MAC Service Data Unit) is the payload delivered to the MAC layer, and the delay per MSDU is the total time consumed by one complete frame exchange cycle:

$$\text{Delay per MSDU} = (T_{DIFS} + T_{SIFS} + T_{BO} + T_{RTS} + T_{CTS} + T_{ACK} + T_{DATA}) \times 10^{-6} \text{ s}$$
Each of these time components is computed by dividing the corresponding number of bits by the rate at which those bits are transmitted. The PHY preamble and header are always sent at the basic rate. The MAC header, data payload, and FCS are sent at the negotiated data rate. The ACK, RTS, and CTS are always sent at the basic rate.

The application-layer goodput is then:

$$TMT_{APP} = \frac{\beta}{\alpha + \beta} \times TMT_{802.11}$$

where $\beta$ is the size of the application datagram (the useful payload) and $\alpha$ is the total overhead above the MAC layer, i.e., the sum of LLC, IP, and transport layer headers.

This computation assumes an ideal scenario: zero bit error rate, no collision losses, no fragmentation, no buffer overflow, and a sender that always has data to transmit. These assumptions represent the **upper bound** on achievable goodput.

### Results for 802.11b and 802.11g

For **802.11b** at its maximum data rate of 11 Mb/s (HR-DSSS modulation), with a payload of 1500 bytes and no RTS/CTS, the efficiency at the 802.11 MAC layer reaches approximately **67.5%**, giving a TMT of roughly **7.4 Mb/s**. When RTS/CTS is enabled, the additional overhead of the RTS and CTS frames reduces both absolute throughput and efficiency slightly, most visibly for small packet sizes.

A key observation in both 802.11b results is that **efficiency grows monotonically with packet size**. Larger packets amortize the fixed overhead (preamble, headers, DIFS, backoff, ACK) over more data bytes. Very small packets (a few hundred bytes) are highly inefficient because the overhead time dominates the exchange cycle.

For **802.11g** at 54 Mb/s (OFDM modulation), the TMT reaches approximately **40 Mb/s** without RTS/CTS at large packet sizes. The efficiency curve is similar in shape to 802.11b but somewhat better at high rates because OFDM PHY overhead is shorter in duration than the DSSS preamble and header used by 802.11b. When 802.11g operates in **mixed mode** (where backward-compatible DSSS devices are present and the basic rate remains 1 Mb/s), the ACK and other control frames take far longer to transmit, dragging efficiency down significantly, to approximately 39.5% even at the 54 Mb/s data rate.

### Impact of ACK rate on efficiency

To isolate the specific cost of the 802.11 ACK frame, consider a data frame of 1500 bytes transmitted at 54 Mb/s:

$$T_{DATA} = \frac{1500 \times 8}{54 \times 10^6} \approx 222 , \mu s$$

The ACK frame is approximately 14 bytes (112 bits). If it is transmitted at 1 Mb/s (legacy mixed mode):

$$T_{ACK} = \frac{112}{10^6} = 112 , \mu s$$

giving an efficiency of $222 / (222 + 112) \approx 66%$. If the ACK is transmitted at 6 Mb/s (the minimum OFDM basic rate in a pure 802.11g network):

$$T_{ACK} \approx 18.7 , \mu s$$

giving an efficiency of $222 / (222 + 18.7) \approx 92\%$.

This analysis shows that the **basic rate at which ACKs are transmitted is one of the most important determinants of Wi-Fi efficiency**. In a legacy or mixed-mode network where the basic rate is 1 Mb/s, ACKs consume nearly as much channel time as the 1500-byte data frames they acknowledge, despite carrying only 14 bytes. Migrating to a pure 802.11g or later network where the basic rate is 6 Mb/s reduces ACK overhead dramatically.

### Full end-to-end goodput with TCP

When TCP is used as the transport protocol, an additional source of overhead appears: **TCP ACKs**. In a half-duplex wireless environment, TCP ACKs travel in the reverse direction on the same shared channel. Because the channel is half-duplex, the TCP ACK frame must itself contend for the medium, wait through DIFS and a backoff period, and be acknowledged by an 802.11 MAC ACK in the reverse direction.

For a complete 802.11b TCP exchange (1500-byte TCP segment, MSS 1452 bytes), including DIFS, average backoff, 802.11 MAC ACK, and the return TCP ACK with its own DIFS and backoff, the maximum achievable TCP application-layer goodput over 802.11b at 11 Mb/s is approximately **4.0 Mb/s**, well below the 7.4 Mb/s MAC-layer TMT and far below the 11 Mb/s physical rate. This confirms the practical rule: **expect less than 50% efficiency from the nominal physical layer link speed** when running TCP over a standard 802.11b network.

For the UDP case with a 1500-byte MTU, the overhead is somewhat lower because UDP does not generate its own ACKs. The protocol overhead above the MAC layer is 8 bytes (UDP) + 20 bytes (IP) + 8 bytes (LLC), so $\alpha = 36$ bytes and $\beta = 1472$ bytes. The efficiency ratio $\beta / (\alpha + \beta) = 1472 / 1508 \approx 97.6\%$ is applied to the MAC-layer TMT. However, if application messages are shorter than 1472 bytes, UDP will not pad them to fill the MTU, and efficiency drops proportionally.

### Improvements in later standards

802.11b and 802.11g are well-characterized by the models above. Newer standards from 802.11n onward introduce several mechanisms specifically designed to reduce the relative cost of protocol overhead:

- **Shorter interframe spaces**: DIFS and SIFS durations are reduced, decreasing idle time between frames.
- **Higher basic rates**: 802.11g and 802.11a already raise the minimum mandatory rate to 6 Mb/s for OFDM networks, reducing ACK transmission time.
- **Channel bonding**: two adjacent 20 MHz channels are combined into a single 40 MHz channel, doubling the available bandwidth for data without doubling the overhead time.
- **Packet bursting**: a station may transmit up to three frames back-to-back after winning channel access, sharing a single DIFS and backoff across multiple frames and thereby amortizing contention overhead over more data.
- **Cumulative ACKs**: a single ACK can acknowledge multiple consecutively transmitted frames in a burst, reducing the number of ACK transmissions required.

As a result of these improvements, the efficiency of modern Wi-Fi networks is substantially better than that of 802.11b or 802.11g. For 802.11n and later standards under favorable conditions, an efficiency of **70 to 80% of the physical layer rate** is a realistic expectation at the application layer.