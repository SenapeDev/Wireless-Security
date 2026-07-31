## The hidden terminal problem

In a wired network, **CSMA/CD** (*Carrier Sense Multiple Access with Collision Detection*) is effective because any station on the network can detect a collision as it happens. In a wireless network, this approach fails for two reasons.

1. A transmitting station's own signal is far stronger at its own antenna than any incoming signal it might be trying to detect simultaneously, making collision detection effectively impossible during transmission.

2. Not all stations can hear each other. Consider three stations A, B, and C arranged such that A and B are within radio range of each other, and B and C are within radio range of each other, but A and C are **not** within radio range of each other. This situation arises naturally due to **signal attenuation**: radio signal power decreases with distance, so two stations far enough apart may be mutually inaudible even though both are audible to a third station in between. This is the **hidden terminal problem**.

In this scenario, if A is transmitting to B, C cannot hear A's transmission and therefore does not know the channel is busy. C may begin transmitting to B at the same time, causing a collision at B. Neither A nor C can detect this collision because they cannot hear each other. The result is a corrupted frame at B with no way for the senders to know what happened.
![[Pasted image 20260403110735.png|559]]
## CSMA/CA
Because of the hidden terminal problem, 802.11 cannot rely on collision detection. Instead, the protocol uses **CSMA/CA**: Carrier Sense Multiple Access with **Collision Avoidance**. The goal is to prevent collisions from occurring in the first place.

### CSMA/CA operation

The sender behavior in CSMA/CA is defined as follows:

1. The station senses the channel. If the channel has been **idle for a period called DIFS** (*Distributed InterFrame Space*), the station transmits the entire frame immediately.
2. If the channel is **busy**, the station starts a **random backoff timer**. The timer counts down only while the channel is idle. When the timer reaches zero, the station transmits. If no acknowledgment (ACK) is received within a timeout period, the station assumes a collision occurred, increases its backoff window (binary exponential backoff), and repeats the process.

On the receiver side, if a frame is received correctly, the receiver waits for a period called **SIFS** (*Short InterFrame Space*) and then sends an ACK back to the sender. The ACK is mandatory because, due to the hidden terminal problem, the sender has no way of knowing whether its transmission caused a collision at the receiver.

The reason the receiver waits for SIFS before transmitting the ACK, rather than using DIFS, is a deliberate **prioritization mechanism**. SIFS is shorter than DIFS. Because any other station that wants to start a new transmission must wait at least DIFS plus a backoff period, the receiver's ACK transmission, which only requires waiting SIFS, gains priority over all other stations on the channel. This ensures the ACK can be sent immediately after the data frame, without risk of another station winning the channel first. If ACKs were subject to the same contention rules as data frames, another station could begin transmitting before the ACK was sent, causing the ACK to be delayed, collide, or be lost, which would trigger unnecessary retransmissions and significantly degrade efficiency. The SIFS/DIFS asymmetry makes the DATA-ACK exchange effectively an **atomic transaction** from the perspective of channel access.

### RTS/CTS mechanism

The basic CSMA/CA mechanism reduces collisions but does not completely solve the hidden terminal problem for long data frames. A complementary mechanism, **RTS/CTS** (*Request to Send / Clear to Send*), allows a station to explicitly reserve the channel before transmitting a data frame.

The procedure works as follows:

1. The sender transmits a short **RTS frame** to the AP using the standard CSMA/CA procedure. The RTS indicates how long the sender intends to occupy the channel.
2. If the AP receives the RTS without collision, it responds with a **CTS frame**, which is broadcast and heard by all stations in the AP's coverage area.
3. All stations that hear the CTS know the channel is reserved for the announced duration. They set a **NAV** (*Network Allocation Vector*) timer and defer their own transmissions for that duration, going silent without needing to sense the channel.
4. The sender, having received the CTS, transmits the data frame. The exchange concludes with an ACK.

The key advantage is that even if station C (a hidden terminal relative to A) did not hear A's RTS, it will hear the AP's CTS and therefore know to stay silent while A transmits. RTS frames are short, so even if two stations send RTS frames simultaneously and they collide, the cost is small. Long data frame collisions, which are far more wasteful, are avoided entirely.

The two modes of operation, **CSMA/CA without RTS/CTS** and **CSMA/CA with RTS/CTS**, have different overhead profiles. In both cases, a critical rule applies: **all control frames (RTS, CTS, ACK, beacons) are transmitted at the basic rate**, the lowest mandatory data rate supported by all devices in the network. Only the DATA portion of an exchange is transmitted at a higher rate, selected adaptively based on channel conditions.

This rule exists for three reasons: 
1. **Universal decodability**: control frames such as CTS and beacons must be receivable by every station in the network, including legacy devices and those at the edge of coverage, where signal quality is lowest. Using the lowest data rate maximizes the probability of correct reception. 
2. **Robustness**: lower data rates use more conservative modulation and coding schemes, which tolerate higher noise levels and result in lower bit error rates. 
3. **Backward compatibility**: all 802.11 devices, regardless of generation, must be able to decode the basic rate so that MAC coordination mechanisms (NAV, CSMA/CA, beacon processing) function correctly across a heterogeneous network. Data frames, by contrast, are unicast to a specific receiver, and the transmitter can adapt the rate to whatever the channel can support between itself and that receiver.


