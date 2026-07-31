## Denial of service attacks on 802.11 WLANs

A DoS attack is any action that prevents legitimate users from accessing a network service. In traditional wired networks, this typically involves flooding a target with more traffic than it can process. In 802.11 WLANs, the attack surface is significantly broader because the medium is **shared and inherently open**: any device within radio range can receive all frames transmitted on the channel, and any device can inject frames without being physically connected to anything.

This openness leads to two fundamental vulnerability classes. **Layer 1 (L1) attacks**, also called RF attacks or jamming, disrupt communication by degrading the signal-to-noise ratio on the wireless channel to a level where legitimate devices can no longer decode frames. **Layer 2 (L2) attacks** exploit weaknesses in the 802.11 protocol itself, specifically in how stations identify each other and coordinate access to the medium.

### Identity vulnerabilities and MAC spoofing

In 802.11, stations are identified at the MAC layer by their MAC address, exactly as in wired Ethernet. However, unlike wired networks where physical access to a port provides some implicit trust, in a WLAN anyone within range can transmit any frame. Critically, **802.11 management frames are not authenticated** in the base standard: there is no cryptographic mechanism that ties a frame to the device that actually sent it. An attacker can configure their wireless interface to use an arbitrary MAC address, a technique called **MAC spoofing**, and the AP or target station has no way to distinguish the spoofed frame from a genuine one. This trust placed in a frame's source address is the root cause of several practical attacks.

The three attack types that directly follow from this identity vulnerability are the **deauthentication attack**, the **disassociation attack**, and the **power saving mode attack**.

### 802.11 management frame types

802.11 defines 12 management frame subtypes used by stations to join and leave a Basic Service Set (BSS). Among the most relevant are:

- Association request / response (subtypes `0x0` / `0x1`)
- Reassociation request / response (subtypes `0x2` / `0x3`)
- Probe request / response (subtypes `0x4` / `0x5`)
- Beacon (subtype `0x8`)
- Disassociation (subtype `0xa`)
- Authentication (subtype `0xb`)
- Deauthentication (subtype `0xc`)

None of these frame types carry cryptographic authentication in the base 802.11 standard, which makes them all potential targets for spoofing-based attacks.

### Deauthentication attack

#### Mechanism

The 802.11 authentication framework includes a **deauthentication frame**, which a station or AP sends to explicitly terminate an authenticated session. This is a legitimate control message: a station sends it when disconnecting gracefully, and an AP sends it when removing a client. Because the frame is unauthenticated, an attacker who knows the MAC addresses of the AP and the target station can inject a forged deauthentication frame with the source address set to either the AP or the victim station.

When the AP receives a deauthentication frame that appears to come from a connected client, it terminates that client's session. Conversely, when a client receives a deauthentication frame that appears to come from its AP, it immediately drops its authenticated state. In both cases, **the victim must complete the full authentication and association procedure again before it can exchange data**, causing a measurable service interruption.

If the attacker **impersonates the AP** and sends a broadcast deauthentication frame (with the destination set to the broadcast address), all clients connected to that AP are simultaneously forced to deauthenticate. By **repeating the attack continuously**, the attacker prevents any client from maintaining a stable connection indefinitely, constituting a sustained DoS.

The attack can thus be directed at a single client or at the entire BSS, and it requires no special hardware, only a wireless interface capable of frame injection (available in standard tools such as `aircrack-ng`).

#### Impact and comparison with disassociation

The deauthentication attack is **more disruptive than the disassociation attack** for one specific reason: recovering from deauthentication requires two full round trips of signaling (the authentication exchange followed by the association exchange), whereas recovering from disassociation only requires one round trip (reassociation, since the station is still authenticated). Additionally, in networks using WPA2 or WPA3, reauthentication triggers a new **EAPOL** (Extensible Authentication Protocol over LAN) four-way handshake to re-establish the session keys, adding further overhead and delay. For this reason, a continuous deauthentication attack is the preferred and most effective tool for an attacker seeking to deny service.

#### Defense against deauthentication attacks

A pragmatic defense, which requires no protocol changes and is backward compatible with existing hardware, exploits a behavioral observation: **legitimate stations do not send deauthentication frames and then immediately continue transmitting data**. A station that genuinely wants to disconnect goes silent. 

The defense works as follows:
- When the AP receives a deauthentication request, it does not honor it immediately. Instead, it waits for a short interval (on the order of 5 to 10 seconds) and monitors whether frames continue to arrive from the source address. If no further frames are received from that address during the interval, the deauthentication is honored. If data frames do arrive from the same address, the deauthentication request is discarded as likely spoofed. This heuristic is effective against attack scenarios where the attacker floods deauthentication frames at high rate, because the victim station continues to transmit data concurrently, making the anomaly detectable.
- A more robust defense creates a **per-client signature** that the AP uses to validate deauthentication requests. This signature incorporates physical-layer observables such as the **Received Signal Strength** (*RSS*) of frames from that client and the **sequence number** continuity of those frames. When a deauthentication frame arrives, the AP checks whether its RSS is consistent with the RSS profile maintained for that client and whether the sequence number fits the expected range. A spoofed frame injected from a different physical location will typically have a significantly different RSS, making it detectable. For example, if a client has been communicating at around -35 dBm and a deauthentication frame arrives at -18 dBm from the same MAC address, the RSS mismatch is a strong indicator of spoofing, and the request should be discarded with an alarm raised.
- The strongest and most principled defense is **Management Frame Protection** (*MFP*), standardized as IEEE 802.11w, which cryptographically authenticates management frames including deauthentication and disassociation. MFP is mandatory in WPA3 and optional in WPA2, and it eliminates the possibility of spoofed management frames for any network where all devices support it.

### Disassociation attack

The disassociation attack is structurally identical to the deauthentication attack but targets the **association state** rather than the authentication state. In 802.11, a client may authenticate with multiple APs in an Extended Service Set but can only be associated with one at a time. The protocol defines an unauthenticated **disassociation frame** that either the client or the AP can send to terminate the current association.

Because disassociation frames are unauthenticated, an attacker can spoof either endpoint's MAC address and inject a forged disassociation frame. The procedure is:

1. Capture frames from the network to learn the MAC addresses of the AP and victim station.
2. Craft a disassociation frame with the source set to either the AP's or the station's MAC address and the destination set to the other party.
3. Transmit the frame over the air.

The AP removes the victim from its association table, and the victim immediately loses the ability to send or receive data. The victim must reassociate (one round trip) before data exchange can resume. By repeatedly injecting such frames, the attacker maintains a continuous DoS. If the attack targets the broadcast address as the destination, all stations in the BSS are simultaneously disassociated, causing a **re-association storm** as every client attempts to reconnect at the same time, further congesting the channel.

The key vulnerability is the same as in the deauthentication case: **no integrity protection for management frames** and **trivial MAC spoofing**. The defenses described for deauthentication apply equally here.

### Attacks on CSMA/CA

The [[Medium Access Control#CSMA/CA|CSMA/CA]] protocol assumes cooperative behavior from all stations. It has no enforcement mechanism: it relies on every device voluntarily respecting the DIFS wait period, the random backoff timer, and the NAV. An attacker who does not follow these rules can exploit this trust to monopolize the channel through several distinct techniques.

#### SIFS/interframe space abuse

In the CSMA/CA exchange, after a data frame is received, the receiver is expected to wait SIFS before sending the ACK, and other stations are expected to wait at least DIFS before starting any new transmission. An attacker can exploit this by **transmitting a garbage** (malformed or arbitrary) **frame immediately before the SIFS window expires**, before the legitimate receiver can send its ACK. When the receiver's ACK is blocked by the garbage frame on the channel, the original sender does not receive the ACK in time, assumes a collision occurred, and begins exponential backoff. If the attacker repeats this at a high enough rate, roughly **50,000 frames per second**, the channel is effectively clogged: legitimate senders are perpetually backing off and retransmitting, and throughput collapses. This attack requires no knowledge of the network topology; it simply requires that the attacker be able to inject frames onto the channel at the required rate.

#### Backoff violation

CSMA/CA requires every station to wait a random backoff period after sensing the channel idle following DIFS, to reduce the probability of simultaneous transmissions. An attacker that **ignores the backoff rule and transmits immediately after DIFS** always wins the contention against all legitimate stations, which are waiting out their respective backoff timers. The attacker effectively starves all other stations on the channel, obtaining unlimited channel access while legitimate traffic is unable to proceed.

#### NAV attack

Every 802.11 frame contains a **Duration** field that specifies how many microseconds the channel is reserved for the ongoing exchange. Stations that receive this field update their local Network Allocation Vector (NAV) and refrain from transmitting until the NAV reaches zero. This mechanism is called **virtual carrier sense** and is the basis of the RTS/CTS reservation system.

An attacker can forge frames carrying an **arbitrarily large Duration value** and inject them into the channel. All stations within radio range that receive such a frame will update their NAV to the forged value and defer all transmission for the corresponding duration. The attacker can repeat this injection just before the NAV expires, effectively locking the channel indefinitely while barely using any channel capacity itself.

When RTS/CTS is enabled, this attack becomes even more potent. The attacker sends a spoofed RTS frame with a large Duration value addressed to the AP. The AP, following the protocol, responds with a CTS frame that also carries the large Duration value and is **broadcast to all stations**. Every station in the BSS that hears the CTS, including those that did not hear the attacker's original RTS, will set their NAV accordingly. The AP itself is also bound by the CTS it sent, so **no station in the entire BSS, including the AP**, can transmit for the forged duration.

The practical defense against NAV attacks is to enforce a **maximum reasonable NAV value** at each node. Legitimate 802.11 exchanges produce Duration values that are predictable and bounded: a single data frame exchange, even at the lowest data rate, will never require a NAV reservation lasting more than a few milliseconds. By discarding or clamping any Duration value that exceeds this maximum, stations can reject forged NAV values without affecting legitimate traffic.

### Attacks on power saving

The 802.11 power management mechanism relies on unauthenticated management frames and is therefore vulnerable to three categories of attack:

1. **Spoofed power-save notification**: the attacker impersonates the victim station and sends a **null data frame with the Power Management bit set to 1**, telling the AP that the victim has entered sleep mode. The AP believes the victim is sleeping and begins buffering all frames destined for it. The victim station, which is actually awake and operating normally, does not receive any of its incoming traffic. The AP periodically sends beacon frames containing the TIM with the victim's AID, but since the victim is not in power-save mode, it ignores those TIMs as irrelevant to itself. The buffered frames age and are eventually discarded by the AP. To maintain the attack, the attacker only needs to continue injecting fake power-save frames; only the AP and victim MAC addresses are needed.
    
2. **Spoofed TIM**: the attacker forges beacon frames containing a modified TIM that does not include the victim's AID, even when the AP actually has frames buffered for it. A client that wakes up, reads the TIM, and does not find its AID listed will go back to sleep without polling the AP, and its buffered frames will never be delivered.
    
3. **Forged beacon injection**: the attacker injects fake beacon frames, disrupting the timing synchronization between the station and the AP. Since the power-save wake/sleep cycle is tied to the beacon interval, a client that synchronizes to a forged beacon will wake up at the wrong time, miss the real beacon, and fail to receive the TIM.
    

All three attacks leverage the same root vulnerability: **power management state is controlled by unauthenticated frames**, and MAC address spoofing is trivial. Management Frame Protection (802.11w) addresses all of them by requiring cryptographic authentication of the relevant frame types.
