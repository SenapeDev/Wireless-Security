## Overview and security goals

The primary security requirement of GSM is **subscriber authentication**: the network must verify that the entity attempting to connect is a legitimate subscriber before granting access, both to prevent unauthorized use and to support accurate billing. Authentication is achieved through a challenge-response protocol that relies on a long-term secret key shared between the subscriber and the home network operator. A key design goal is that this long-term key is never revealed to visited networks during roaming.

Beyond authentication, GSM provides two additional security services:

- **Confidentiality of communications and signaling over the wireless interface**, implemented via a session encryption key established during authentication with the involvement of the home network.
- **Subscriber identity protection**, achieved by using short-term temporary identifiers over the air interface so that a passive eavesdropper cannot link transmissions to a permanent subscriber identity.

### Trust model

The GSM security model is built around a specific set of trust assumptions. The network trusts the **SIM card** but not the mobile equipment itself, since SIM cards are issued and controlled by the operator. The subscriber trusts the home operator but not necessarily any visited network encountered during roaming. The wireless channel is considered untrusted and therefore requires protection. The core network of the home operator is assumed to be a trusted, physically protected infrastructure.

The practical consequence of this model is that authentication is performed between the SIM and the home network's infrastructure, and the resulting session key is then shared with the visited network to enable encryption. Crucially, this model involves **no mutual authentication**: the network authenticates the subscriber, but the subscriber has no mechanism to verify the authenticity of the network it is connecting to. This is the single most important security weakness in GSM, and it is discussed in detail in the authentication section below.


## System architecture

A GSM network is organized into three main domains: the **Mobile Station**, the **Radio Access Network**, and the **Network Subsystem** (also called the Core Network).
![[Pasted image 20260603150419.png]]
### Mobile station

The **Mobile Station** (*MS*) is the combination of the user's **Mobile Equipment** (*ME*), which is the physical handset, and the **Subscriber Identity Module** (*SIM*) card. The ME performs voice encoding, user-side ciphering, and communication with the GSM infrastructure. Critically, the ME is only hardware: without a SIM card, it cannot authenticate to or access any operator network.

![[Pasted image 20260603150535.png]]

The SIM card is a tamper-resistant smart card issued by the operator. It stores network-specific information used to identify and authenticate the subscriber, including:

- **ICCID** (*Integrated Circuit Card Identification*): the unique identifier of the physical card.
- **IMSI** (*International Mobile Subscriber Identity*): the permanent, globally unique identifier of the subscriber.
- **$K_i$**: the 128-bit authentication key, which is the long-term shared secret.
- Operator-specific data such as the emergency number, service provider name (*SPN*), service dialing numbers (*SDN*), **SMSC** (*Short Message Service Centre*) number, advice-of-charge parameters, and **VAS** (*Value-Added Service*) applications.

The SIM also stores and executes the A3 and A8 cryptographic algorithms. Because the authentication key $K_i$ never leaves the SIM, compromising the handset alone is not sufficient to impersonate the subscriber.

### Radio access network

The **Radio Access Network** (*RAN*) connects mobile stations to the core network over the air interface. It is composed of **Base Transceiver Stations** (*BTS*) and **Base Station Controllers** (*BSC*).

The BTS is the physical radio equipment that communicates directly with mobile stations. It is responsible for implementing the A5 stream cipher, performing encryption and decryption of radio-link traffic toward and from the ME.

The BSC manages a group of BTSs and is responsible for radio resource management, including the handover process. When an MS moves from one BTS to another, the BSC transfers the session encryption key $K_c$ to the new BTS so that encrypted communication can continue without interruption.

### Network subsystem

The **Network Subsystem** (*NSS*), or Core Network, provides the central functions of the GSM architecture: telephone switching, subscriber profile management, and mobility management. The security-relevant components are:

- **Authentication Center** (*AuC*): stores the secret keys $K_i$ of all subscribers, generates random challenges, and computes the authentication and encryption parameters. It is the root of trust for all subscriber authentication in the home network.
- **Home Location Register** (*HLR*): the permanent database of a home operator's subscribers. It provides the **Mobile Switching Center** (*MSC*) with authentication triplets (RAND, SRES, $K_c$) and tracks subscriber location.
- **Visitor Location Register** (*VLR*): a temporary database in the visited network that stores authentication triplets received from the HLR when a subscriber is roaming. This design ensures that visited network operators never need direct access to the subscriber's secret key.
- **Equipment Identity Register** (*EIR*): a database used to track mobile equipment by its **IMEI** (*International Mobile Equipment Identity*), described further in the section on stolen equipment detection.


## Authentication

### Protocol overview

GSM authentication is a **one-way challenge-response protocol**. The network authenticates the subscriber (via the SIM), but the subscriber does not authenticate the network. The protocol involves the following parameters:

- **$K_i$**: the 128-bit authentication key, stored in both the AuC and the SIM. It is never transmitted over any interface.
- **RAND**: a 128-bit random number generated by the AuC, used as the challenge.
- **SRES** (*Signed Response*): a 32-bit value computed by applying the A3 algorithm to $K_i$ and RAND. It is used to verify the subscriber's knowledge of $K_i$.
- **$K_c$**: a 64-bit cipher key generated by applying the A8 algorithm to $K_i$ and RAND. It is used to encrypt subsequent radio-link traffic.
- **A3**: the authentication algorithm, stored in both the AuC and the SIM.
- **A8**: the cipher key generation algorithm, stored in both the AuC and the SIM.
- **PRNG**: a pseudo-random number generator used by the AuC to produce RAND values.
![[Pasted image 20260603151039.png]]
The AuC pre-computes sets of triplets (RAND, SRES, $K_c$) for each subscriber and stores them in the HLR. When the VLR needs to authenticate a subscriber, it requests a batch of these triplets from the HLR rather than contacting the AuC for each individual authentication event.

### Authentication procedure

The authentication proceeds as follows:

1. The MS sends its **IMSI** to the network subsystem to initiate the authentication procedure.
2. The VLR receives the IMSI and, if it does not already hold unused triplets for that subscriber, requests triplets from the HLR/AuC.
3. The HLR/AuC returns one or more triplets (RAND, SRES, $K_c$) to the VLR.
4. The VLR forwards the **RAND** to the MS as a challenge.
5. The MS passes RAND and $K_i$ to the A3 algorithm inside the SIM, producing a local response **SRES'**, and to A8, producing a local copy of **$K_c$**.
6. The MS sends **SRES'** to the VLR.
7. The VLR compares SRES' against the SRES from the triplet. If they match, the subscriber is authenticated and the session proceeds using $K_c$ for encryption.

Note that A3 and A8 are **never disclosed** by the operator: each operator may use a proprietary implementation, and the algorithms are specified only in terms of their inputs and outputs. This approach relied on security through obscurity, a philosophy that was later shown to be inadequate.

### The one-way authentication weakness

The most significant structural weakness of the GSM authentication scheme is that **only the subscriber is authenticated to the network, not the network to the subscriber**. A mobile station has no way to verify whether the BTS it is connecting to is a legitimate network node or an attacker-controlled device.

This enables **fake base station** (or rogue BTS) attacks. An attacker who operates a device that mimics a legitimate BTS can cause nearby mobile stations to associate with it, because the phone cannot distinguish it from a real network. Once associated, the attacker can intercept calls and messages, perform traffic downgrade attacks (forcing the phone to use no encryption or a weak cipher), or capture the subscriber's IMSI. Devices used for this purpose are commercially known as **IMSI catchers** or **Stingrays**. This class of attack was not addressed in GSM and was only remedied in UMTS, which introduced mutual authentication.

### VLR transitions and triplet transfer

When a subscriber moves to a new VLR area, the new VLR needs to establish the subscriber's identity before it can request fresh triplets from the HLR/AuC. To speed up this process, the new VLR requests the subscriber's IMSI from the old VLR. The old VLR transfers the IMSI together with any unused triplets it still holds. This allows the new VLR to proceed with authentication immediately, without first having to obtain the IMSI and then separately request triplets from the home network.



## Cryptographic algorithms

### A3 and A8

**A3** is the authentication algorithm responsible for computing the SRES from a 128-bit RAND and a 128-bit $K_i$. The output is 32 bits. The algorithm must execute within 500 ms (a significant constraint given the hardware capabilities of 1990s-era SIM cards) and runs entirely inside the SIM.
![[Pasted image 20260603151539.png|481]]

**A8** is the cipher key generation algorithm. It takes the same inputs as A3 (128-bit RAND and 128-bit $K_i$) and produces the 64-bit cipher key $K_c$. In practice, A3 and A8 are typically implemented as a single combined function, since they share the same inputs and can be computed in one pass.

![[Pasted image 20260603151602.png|481]]
### COMP128

In most GSM deployments, A3 and A8 are implemented using a single algorithm called **COMP128**, which is a **keyed hash function**. It takes 128-bit $K_i$ and 128-bit RAND as inputs and produces a 96-bit output, of which the first 32 bits form the SRES and the remaining 64 bits form $K_c$.

COMP128 went through several versions:

| **Version**   | Description                                                                                                                    |
| ------------- | ------------------------------------------------------------------------------------------------------------------------------ |
| **COMP128-1** | Original algorithm. Generates a 54-bit effective $$K_c$$ (the last 10 bits are set to zero, yielding only 54 bits of entropy). |
| **COMP128-2** | Strengthened design, but $$K_c$$ is still intentionally limited to 54 effective bits.                                          |
| **COMP128-3** | Same algorithm as COMP128-2, but produces a full 64-bit $$K_c$$.                                                               |
| **COMP128-4** | Redesigned based on the 3GPP Milenage algorithm, using AES as the underlying primitive.                                        |

Internally, COMP128-1 operates on a 32-byte vector initialized with $K_i$ in the first 16 bytes and RAND in the second 16 bytes. It applies 8 iterative rounds, each consisting of a compression step structured as a five-level butterfly with table lookups, followed (in all rounds except the last) by a permutation. The 16-byte result of each round's compression is written back into the second half of the vector, while $K_i$ is reloaded into the first half. After 8 rounds, the 128-bit state is compressed to 12 bytes to produce the final output.

The specifications of A3 and A8 were never made public. The designers relied on security through obscurity, partly due to telecom industry culture of the era, partly due to fears that publishing the algorithm would make SIM cloning easier, and partly because of export-control restrictions on cryptography that were politically sensitive at the time. This approach contradicts **Kerckhoffs' principle**, which states that a cryptosystem should remain secure even if everything about it except the key is public knowledge. Modern cryptographic practice assumes that algorithms are published and only keys remain secret.

In 1997, a leaked internal document led to the publication and partial reverse-engineering of COMP128-1. In 1998, researchers from the Smartcard Developer Association and UC Berkeley (Wagner and Goldberg) published a practical attack. The attack exploits a structural weakness in the compression function known as a **narrow pipe**: because certain intermediate values are only 4 bits wide, the birthday paradox guarantees a collision after approximately $2^{14}$ challenges. Each collision reveals one byte of $K_i$, so full key recovery requires roughly 131,000 queries. Using a smartcard reader capable of submitting about 6 queries per second, recovering the complete $K_i$ takes approximately 6 hours of physical access to the SIM. This enables **SIM cloning**: once $K_i$ is known, a new SIM can be programmed with the same identity and key, allowing an attacker to impersonate the subscriber. The researchers noted that their techniques were not particularly novel, highlighting how weak the original design was.

### A5 variants

**A5** is the stream cipher used to encrypt radio-link traffic between the MS and the BTS. Encryption applies only on the wireless segment; traffic within the core network is carried in plaintext. The rationale behind this design choice was that the wireless channel was considered the only vulnerable medium: radio transmissions are broadcast over the air and can be intercepted by anyone with a receiver, while the core network was assumed to be physically protected, operator-owned, and connected through trusted infrastructure. Additional practical motivations included the limited computational resources of early 1990s equipment and lawful interception requirements, which needed traffic to remain accessible inside the network. Today this architecture is considered a significant weakness, since attackers who compromise operator infrastructure, exploit signaling protocols, or mount insider attacks can access plaintext traffic.

Seven versions of A5 were defined, all initially kept secret. Through leaks and reverse engineering, the main versions became public. The encryption process is symmetric: the same algorithm and key are used for both encryption and decryption. The inputs to A5 are the 64-bit session key $K_c$ and a 22-bit **frame number** (*FN*). The frame number serves as an implicit, synchronized initialization value that ensures a different keystream is generated for each GSM radio burst (frame), without requiring any additional signaling. Since both the MS and the BTS are already synchronized on the TDMA frame structure, the FN is inherently available to both parties at all times and costs no additional bandwidth. The cipher produces a 114-bit keystream, which is XOR-ed with the 114-bit data payload. Using a predictable counter rather than a random nonce is not inherently insecure, since the security should derive entirely from the secrecy of $K_c$, not from the unpredictability of the frame number. However, predictable initialization values can simplify cryptanalysis of ciphers that have structural weaknesses, which is relevant for A5/1.

#### A5/1

**A5/1** is the main encryption algorithm, intended for use in countries without severe cryptographic export restrictions. It is based on three **linear feedback shift registers** (*LFSRs*): R1 (19 bits), R2 (22 bits), and R3 (23 bits), with total state of 64 bits. Each LFSR has a characteristic polynomial defining which bit positions are XOR-ed to produce the feedback bit on each clock cycle.

The three registers are not clocked uniformly. Instead, A5/1 uses an **irregular (majority) clocking mechanism**: at each step, each register's designated middle bit is compared against the majority value of the three middle bits. A register is advanced only if its middle bit agrees with the majority. This means that at any given step, at least two of the three registers advance and at most one is held still. The output of A5/1 at each step is the XOR of the most significant bits of R1, R2, and R3.

Initialization proceeds in three phases. First, the three LFSRs are set to zero and the 64 bits of $K_c$ are clocked in bit by bit, each bit being XOR-ed into the lowest-order stage of all three registers and then advancing all three unconditionally. Second, the registers are reset to zero again and the 22 bits of FN are similarly clocked in. Third, the cipher runs 100 additional mixing steps (discarding output) to mix the state thoroughly before keystream generation begins. The keystream is then produced 228 bits per frame (114 bits for uplink, 114 bits for downlink).

A5/1 has been subject to numerous attacks. The historical key length was the result of a political compromise during the 1982 standardization process: an original proposal of 128-bit keys was overruled in favor of a shorter key to accommodate intelligence agency access requirements. Multiple published attacks, including ciphertext-only attacks, have demonstrated that A5/1 can be broken in minutes using precomputed rainbow tables. An attack published in 2006 demonstrated real-time or offline decryption of A5/1-protected GSM calls. Documents released through government transparency disclosures have confirmed that intelligence agencies can routinely decrypt A5/1-protected communications.

#### A5/2

**A5/2** was designed as a deliberately weaker export cipher for use in regions subject to Western cryptographic export restrictions, including Eastern European states. It extends the LFSR structure to four registers (R1 through R4, with lengths 19, 22, 23, and 17 bits respectively) and uses a non-linear output combiner, but is structurally simpler and significantly weaker than A5/1. Cryptographic weaknesses were identified in 1999, and by 2003 it was shown that A5/2 is vulnerable to a real-time **man-in-the-middle** (*MITM*) attack. Since 2006, the GSM standards explicitly prohibit implementing A5/2 in mobile stations. The current requirement is that mobile stations must implement A5/1; if the network does not support A5/1, an unencrypted connection may be used.



## Subscriber identity protection

### IMSI and TMSI

When a mobile station initiates contact with the network, it must transmit its permanent identity, the IMSI, so that the network can retrieve the corresponding $K_i$ from the AuC and proceed with authentication. However, transmitting the IMSI in plaintext over the air interface on every connection would allow a passive eavesdropper to build a persistent record linking a subscriber identity to their location and activities.

The reason the IMSI cannot simply be transmitted over an encrypted channel is that encryption requires a session key $K_c$, which can only be derived after authentication has completed. Before authentication, no shared key exists between the MS and the network, so no encrypted channel is available. The IMSI is therefore unavoidably exposed in plaintext at least once, during the very first contact with a new network.

To limit this exposure, GSM uses **Temporary Mobile Subscriber Identity** (*TMSI*): a 4-byte random number generated by the VLR and assigned to the MS after successful authentication and ciphering activation. From that point on, the MS uses the TMSI instead of the IMSI in all subsequent over-the-air communications. The IMSI is only transmitted in plaintext when no TMSI is available, for example during the very first registration or after a TMSI becomes invalid. At each location update, the VLR may allocate a new TMSI to the subscriber, limiting the window during which a given TMSI can be linked to a specific location.

### Ciphering mode and TMSI assignment procedure

After the authentication exchange is complete, the network activates encryption and assigns a TMSI through the following sequence:

1. A signaling connection is set up between the UE, BTS, BSC, and MSC.
2. User authentication is performed (challenge-response exchange as described above).
3. The MSC sends a **Cipher Mode Command** to the BSC, which forwards an **Encryption Command** to the BTS and a **Cipher Mode Command** to the MS. From this point, all radio traffic is encrypted using $K_c$ and A5.
4. The MS confirms with a **Cipher Mode Complete** message, which is relayed back to the MSC.
5. The VLR sends a **TMSI Reallocation Command** to the MS (now over the encrypted channel), assigning a new TMSI.
6. The MS confirms the reallocation with a **TMSI Reallocation Complete** message.
7. The signaling procedure continues with all traffic encrypted and the new TMSI in use.

![[Pasted image 20260603152038.png]]

The key design point here is that **TMSI assignment and reallocation always occur over an already-encrypted channel**, ensuring that the new TMSI is never exposed in plaintext.



## Detection of stolen or compromised equipment

Each mobile equipment unit carries a globally unique **IMEI** (*International Mobile Equipment Identity*). When a handset is reported lost or stolen, the owner can notify the operator, which adds the IMEI to a blacklist stored in the **EIR** (*Equipment Identity Register*). If mandated by law in the operator's jurisdiction, the operator may also propagate the blacklist entry to a centralized shared EIR.

In practice, maintaining an effective global blacklist has been difficult. Historically, the absence of a worldwide shared system made international trafficking of stolen handsets highly profitable, since a blacklisted device in one country could be used freely in another. The situation has improved as more operators participate in the **GSMA** (*GSM Association*) global IMEI database and international blacklist sharing systems.

A residual weakness is that the IMEI itself is not cryptographically protected. On older or cheaper devices, attackers can modify or spoof the IMEI, making blacklist-based detection unreliable.



## Attacks against GSM security

GSM's vulnerabilities span four categories: attacks against anonymity, attacks against authenticity, attacks against confidentiality, and attacks against the cryptographic algorithms themselves.

### Attacks against anonymity

The use of TMSI substantially reduces IMSI exposure, but does not eliminate it entirely. The IMSI must be transmitted in plaintext during the first registration with a new network, or whenever the TMSI is unavailable or has expired. An attacker who controls a fake base station can force this condition by presenting itself as a new network or by causing the MS to discard its current TMSI, prompting the device to re-identify itself using the IMSI in plaintext.

### Attacks against authenticity: fake base stations and IMSI catchers

The absence of network authentication is the root cause of the most operationally significant class of attacks against GSM. Because the MS has no way to verify the legitimacy of a BTS, an attacker can deploy a **rogue BTS** that advertises itself with a strong signal, causing nearby devices to associate with it. Once a device connects to the rogue BTS, the attacker can:

- Request the subscriber's IMSI, which the device discloses without any proof of network authenticity.
- Force the device into an unencrypted mode by simply not initiating the ciphering procedure, since the MS cannot reject a network decision to disable encryption in GSM.
- Intercept outgoing and incoming calls and messages.
- Perform **downgrade attacks** by advertising only weak cipher modes or no encryption.

Devices used to carry out these attacks are commercially known as **IMSI catchers** or **Stingrays**, and have been used by law enforcement and intelligence agencies worldwide.

A related attack is **call hijacking**: when a network segment has encryption disabled, an attacker positioned as a man-in-the-middle can intercept a call setup and then drop the legitimate user from the connection once the call is established.

### Attacks against confidentiality: over-the-air interception

Even where encryption is nominally in use, GSM confidentiality is limited in two structural ways. First, encryption only covers the radio link between the MS and the BTS; traffic within the core network travels in plaintext. Second, the effective key length of $K_c$ is only 54 bits in COMP128-1 and COMP128-2 deployments (the last 10 bits are set to zero), which is far below the theoretical 64-bit size of $K_c$. Multiple attacks against A5/1 have been demonstrated, including ciphertext-only attacks and real-time decryption using precomputed tables. The 54-bit effective key length was the direct result of deliberate weakening, and even the nominally stronger A5/1 was broken in practice.

The absence of **message authentication and integrity protection** is a further weakness. GSM provides no mechanism to detect whether encrypted traffic has been tampered with in transit, making bit-flipping attacks on the ciphertext feasible.

### Attacks against the cryptographic algorithms

The COMP128-1 attack described earlier demonstrates that the A3/A8 implementation was vulnerable to key recovery with physical access to the SIM, enabling SIM cloning. Tools such as SIM scanners and SIM editors, which are commercially available, can be used to read and write SIM card data, further lowering the barrier to SIM duplication.

A5/1, while stronger than A5/2, has been comprehensively broken. A5/2 was deprecated in 2006 following the demonstration of a real-time MITM attack.

### Denial of service

GSM provides no effective protection against **jamming**: an attacker who transmits on the frequencies used by a cell can prevent mobile stations in the affected area from communicating with the legitimate network. Additionally, a rogue BTS that attracts a device's association effectively removes the device from the legitimate network's paging reach, achieving a denial-of-service outcome without any radio jamming.

### The limits of cryptographic improvements

An important conceptual point is that stronger encryption alone would not have fixed GSM's security problems. Many of the most significant attacks do not depend on breaking A5 at all. A rogue BTS can impersonate the network, request the IMSI, disable encryption, and intercept traffic regardless of how strong the cipher is, because the underlying problem is the absence of mutual authentication. GSM trusted the network unconditionally: the phone had no means to authenticate the BTS, and no recourse when the network instructed it to operate without encryption. The core weaknesses of GSM were therefore **architectural**, not merely cryptographic, and resolving them required a redesign of the authentication model rather than a stronger cipher.
