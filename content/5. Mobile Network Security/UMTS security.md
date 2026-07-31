**Universal Mobile Telecommunications System** (*UMTS*) is the third-generation (*3G*) mobile cellular standard developed and maintained by the **3rd Generation Partnership Project** (*3GPP*). It is a component of the **International Telecommunications Union** (*ITU*) IMT-2000 standard set. UMTS was designed as an evolution of GSM, extending the existing architecture with a focus on data communications and substantially improving its security model.

The security design of UMTS addressed the most significant structural weaknesses of GSM: it introduced **mutual authentication** between the subscriber and the network, added **integrity protection** for signaling traffic, derived **separate keys** for confidentiality and integrity, and defined a structured framework of security feature groups covering the full system from the radio interface to the application layer.

## System architecture

The UMTS architecture involves three main components: the **User Equipment** (*UE*), the **Radio Access Network** (*RAN*), and the **Core Network** (*CN*). The RAN is connected to the CN through the operator's backbone network.

![[Pasted image 20260603154515.png]]
### User equipment

The UE consists of the mobile terminal and the **Universal Subscriber Identity Module** (*USIM*). The USIM is the UMTS evolution of the GSM SIM card. It stores the subscriber's long-term secret key K, executes the authentication and key derivation functions, and supports a richer set of security operations than its GSM predecessor.

### Radio access network: UTRAN

The UMTS radio access network is called **UMTS Terrestrial Radio Access Network** (*UTRAN*). It is based on **Wideband Code Division Multiple Access** (*W-CDMA*) technology and contains two types of network elements.

The base station, called **NodeB** in 3GPP terminology, is the termination point of the radio interface on the network side. It connects to a **Radio Network Controller** (*RNC*), which is the controlling unit of UTRAN. A UE may be connected to the network through several RNCs simultaneously. The RNC that maintains the connection to the CN for a given UE is called the **Serving RNC** (*SRNC*), while any additional RNCs connected to the same UE are called **Drifting RNCs** (*DRNCs*).

### Core network

The UMTS Core Network includes several components inherited and extended from the GSM NSS:

- **Mobile Switching Controller** (*MSC*) and **Visitor Location Register** (*VLR*): handle circuit-switched mobility and authentication data for visiting subscribers.
- **Gateway MSC** (*GMSC*): the interface between the UMTS core and external telephone networks.
- **Home Location Register** (*HLR*): the permanent subscriber database of the home operator.
- **3G Serving GPRS Support Node** (*SGSN*): handles packet-switched data for subscribers in a given area.
- **Gateway GPRS Support Node** (*GGSN*): the interface between the packet-switched core and external data networks.
- **Authentication Center** (*AuC*): stores subscriber keys and generates authentication vectors.

## Security architecture

The UMTS security architecture, defined in 3GPP TS 33.102, is organized into five feature groups, each addressing a distinct part of the system.
![[Pasted image 20260603154654.png]]
1. **Network access security (I)** provides users with secure access to 3G services. This group protects against attacks on the radio access link and includes user identity confidentiality, entity authentication (both user and network), cipher algorithm and key agreement, confidentiality of user and signaling data, data integrity, and mobile equipment identification.

2. **Network domain security (II)** enables nodes within the provider domain to exchange signaling data securely. This group protects against attacks on the wireline network segments between network nodes.

3. **User domain security (III)** secures access to the mobile station itself. It covers user-to-USIM authentication (ensuring the USIM is only accessible to an authorized user, typically via PIN) and the USIM-terminal link (restricting a terminal to authorized USIMs, such as operator SIM-locking).

4. **Application domain security (IV)** enables applications in the user and provider domains to exchange messages securely. The **USIM Application Toolkit** allows operators and third-party providers to deploy applications resident on the USIM, and this feature group provides the means to secure messages transferred over the network to those applications.

5. **Visibility and configurability of security (V)** gives users the ability to observe and control the operation of security features. This includes indications of whether the access network connection is encrypted and what level of security is active, as well as user-configurable options such as enabling or disabling user-USIM authentication, accepting or rejecting unencrypted incoming calls, and choosing which ciphering algorithms are acceptable.


## Authentication and key agreement

### Design principles

UMTS replaces the GSM challenge-response authentication with a protocol called **Authentication and Key Agreement** (*AKA*). The fundamental improvements over GSM are:

- **Mutual authentication**: not only does the network authenticate the subscriber, but the subscriber also authenticates the network. This directly addresses the fake base station vulnerability.
- **Replay protection**: a sequence number mechanism prevents replayed authentication vectors from being accepted.
- **Key separation**: distinct keys are derived for confidentiality (CK), integrity (IK), and sequence number concealment (AK), rather than relying on a single session key.

Using separate keys for different security functions is a fundamental principle of modern cryptographic design. If a single key were used for authentication, encryption, integrity, and anonymity simultaneously, a compromise or weakness in any one use of that key would affect all others. By deriving independent keys from the same root secret using different functions, UMTS ensures that the exposure of one key does not automatically compromise the others.

### Parameters

The UMTS AKA protocol uses the following parameters:

| Parameter | Description                                                                           |
| --------- | ------------------------------------------------------------------------------------- |
| **K**     | Long-term shared secret key, stored in the USIM and the AuC                           |
| **RAND**  | 128-bit random number, the challenge                                                  |
| **SQN**   | Sequence number, used for freshness and replay protection                             |
| **AMF**   | Authentication and Key Management Field, used to direct authentication vector usage   |
| **MAC**   | Message Authentication Code, computed by the network to prove knowledge of $K$        |
| **XMAC**  | Expected MAC, recomputed by the USIM to verify the network                            |
| **CK**    | Cipher Key, used for radio-link confidentiality                                       |
| **IK**    | Integrity Key, used for signaling integrity protection                                |
| **AK**    | Anonymity Key, used to conceal SQN in transit                                         |
| **XRES**  | Expected Response, the network's expected value of the user's authentication response |
| **RES**   | Response, computed by the USIM and sent to the network                                |
| **AUTN**  | Authentication Token, generated by the network and sent to the UE                     |
| **AV**    | Authentication Vector, the tuple (RAND, XRES, CK, IK, AUTN) prepared by the AuC       |

### Cryptographic functions

The AKA mechanism relies on five cryptographic functions, all derived from the shared key K:

- **f1**: network authentication function, used to compute the MAC included in AUTN.
- **f2**: user authentication function, used to compute RES and XRES.
- **f3**: cipher key derivation function, produces CK.
- **f4**: integrity key derivation function, produces IK.
- **f5**: anonymity key derivation function, produces AK for concealing SQN.

A general security requirement applies to all five functions: it must be computationally infeasible to derive K from knowledge of any function's inputs and outputs.

### Authentication procedure
![[Pasted image 20260715194211.png]]
The AKA protocol proceeds as follows:

**At the HLR/AuC (preparation phase):**

1. The AuC selects a sequence number SQN and a random number RAND, and retrieves the subscriber's key K.
2. It computes MAC = f1(K, SQN, AMF, RAND), AK = f5(K, RAND), XRES = f2(K, RAND), CK = f3(K, RAND), and IK = f4(K, RAND).
3. It constructs the **Authentication Token**: AUTN = (SQN XOR AK) \|\| AMF \|\| MAC. The SQN is concealed under AK so that an eavesdropper observing the air interface cannot track the subscriber via the sequence number.
4. The complete Authentication Vector AV = (RAND, XRES, CK, IK, AUTN) is sent to the VLR/SGSN.

**At the VLR/SGSN:**

5. The VLR/SGSN sends (RAND, AUTN) to the UE as a challenge.

**At the USIM (verification phase):**

6. The USIM computes AK = f5(K, RAND) and recovers SQN = (SQN XOR AK) XOR AK.
7. It verifies the sequence number is within an acceptable range (freshness check, replay protection).
8. It computes XMAC = f1(K, SQN, AMF, RAND) and compares it against the MAC field in AUTN. If XMAC = MAC, the **network is authenticated**: only a party that knows K could have produced the correct MAC.
9. The USIM computes RES = f2(K, RAND), CK = f3(K, RAND), and IK = f4(K, RAND).
10. The UE sends RES to the VLR/SGSN.

**At the VLR/SGSN (completion):**

11. The VLR/SGSN compares RES against XRES. If they match, the **user is authenticated**.
12. CK and IK are passed to the RAN for use in subsequent encrypted and integrity-protected communications.

The AUTN field is the mechanism that enables mutual authentication. It contains a MAC computed over K, SQN, AMF, and RAND. Since RAND and AMF are transmitted in plaintext, the only way for the USIM to reconstruct the correct XMAC is to know K and the correct SQN. A rogue base station that does not know K cannot produce a valid AUTN, so the UE can detect and reject it.
![[Pasted image 20260715194843.png]]
## Confidentiality

### Scope

Like GSM, UMTS encrypts radio-link traffic between the UE and the RAN. However, UMTS uses stronger algorithms and a more carefully designed key management scheme. The cipher key CK is derived independently from the integrity key IK during the AKA process, ensuring that the two keys are never shared.

### Stream cipher operation

The UMTS stream cipher takes the following inputs: the **COUNT-C** (a ciphering sequence number), the **BEARER** identifier (a 5-bit radio bearer identifier that distinguishes between simultaneous logical communication channels for the same user), the transmission **DIRECTION** (uplink or downlink), the **LENGTH** of the keystream block requested, and the **CK**. Including the BEARER identifier ensures that different keystreams are generated for different logical channels even when all other inputs are identical, preventing keystream reuse across bearers.

The algorithm produces a keystream block that is XOR-ed with the plaintext to produce ciphertext, or XOR-ed with the ciphertext to recover plaintext. Encryption and decryption are symmetric.

### Implementation requirements

The UMTS confidentiality algorithm was designed to meet specific implementation constraints: hardware implementations must use no more than 10,000 gates, and the algorithm must achieve at least 2 Mbps throughput (based on a reference clock speed of 20 MHz). In practice, typical clock speeds greatly exceed this reference, so the algorithm must support considerably higher throughput in deployed hardware.

The keystream block size requirements vary by radio link mode. In RLC-transparent mode, a new keystream block is generated per 10 ms frame with a maximum of 5114 bits. In **RLC-UM** (*Unacknowledged Mode*) and **RLC-AM** (*Acknowledged Mode*), new blocks are generated at intervals of at least 156 µs with a maximum of 1016 and 1024 bits respectively.



## Data integrity

UMTS introduces **integrity protection for signaling and control-plane messages**, a feature that was entirely absent from GSM. Integrity protection ensures that signaling messages cannot be modified in transit without detection.

The integrity algorithm takes the following inputs: the **COUNT-I** (an integrity sequence number), a **FRESH** value (a per-connection nonce generated by the network at the start of each connection), the **DIRECTION** of transmission, the **MESSAGE** content, and the **IK**. The algorithm produces a **Message Authentication Code** (*MAC-I*), which is appended to the signaling message. The receiver recomputes the expected MAC (XMAC-I) and compares it against the received MAC-I; a mismatch indicates tampering.

The FRESH value protects the network against replay of signaling messages by the user: since FRESH is chosen by the network at the start of each connection and is unique to that connection, replayed messages from a previous connection will produce a different FRESH value and fail verification. COUNT-I is a synchronized counter maintained by both the UE and the network; both sides increment it consistently for each protected message, ensuring that replayed messages within the same connection are also detected.

Integrity protection applies to signaling and control-plane data. User-plane data (voice and data traffic) is not integrity-protected in UMTS.



## Subscriber identity confidentiality

UMTS, like GSM, uses temporary identities to reduce IMSI exposure over the air interface. Two types of temporary identities are defined:

- **TMSI** (*Temporary Mobile Subscriber Identity*): used in the circuit-switched domain.
- **P-TMSI** (*Packet Temporary Mobile Subscriber Identity*): used in the packet-switched domain.

The same fundamental constraint that applies in GSM also applies in UMTS: the IMSI must be sent in plaintext during the very first contact with a new network, before any session key has been established. This means that an attacker who is present at that moment, or who forces a fresh registration, can still observe the IMSI. The IMEI is also transmitted without cryptographic protection in UMTS and is therefore not a security-grade identifier.



## Remaining vulnerabilities in UMTS

Despite its substantial improvements over GSM, UMTS retains several security limitations.

The **IMSI exposure problem** is not fully solved: the IMSI must still be transmitted in plaintext at initial registration, and any attack that forces a fresh registration (such as a rogue base station that causes the UE to detach and re-register) can capture the IMSI.

A user can be induced to camp on a **false base station** by one that transmits a strong signal. Once the UE associates with the false BS, it is out of reach of the legitimate network's paging signals, effectively achieving a denial-of-service outcome. Although the UE will detect that the rogue network cannot produce a valid AUTN and will refuse to complete authentication, the connection to the legitimate network has already been disrupted.

**Call hijacking** remains possible in network segments where encryption has been disabled. An attacker who can position themselves as a man-in-the-middle between the UE and the network can intercept a call setup and drop the legitimate connection once the call is established, particularly if the network does not enforce encryption.

The most practically significant residual problem, however, is **backward compatibility with GSM**. Modern devices must support older radio technologies to maintain service continuity. A rogue base station can advertise itself as a GSM network and refuse to offer UMTS or LTE, forcing nearby devices to fall back to 2G. Once the device is operating under GSM, all of GSM's weaknesses apply: there is no mutual authentication, the IMSI can be captured, and encryption can be disabled or downgraded. This is why IMSI catchers remain effective against modern devices despite UMTS mutual authentication: the attack does not break UMTS, it bypasses it by forcing a protocol downgrade to a generation that lacks the relevant protections.



## GSM vs. UMTS: a security comparison

The following table summarizes the principal differences between the two generations.

| Security Aspect                 | GSM (2G)                                                 | UMTS (3G)                                                 |
| ------------------------------- | -------------------------------------------------------- | --------------------------------------------------------- |
| **Authentication**              | One-way (network authenticates user only)                | Mutual (network and user authenticate each other)         |
| **Network Authentication**      | Not supported                                            | Supported via AUTN                                        |
| **Replay Protection**           | Weak                                                     | Stronger via SQN                                          |
| **User Identity Protection**    | IMSI frequently exposed                                  | Improved; IMSI still exposed at first registration        |
| **Temporary Identity**          | TMSI                                                     | TMSI (circuit-switched) and P-TMSI (packet-switched)      |
| **Confidentiality**             | Radio link only; 54-bit effective key; broken algorithms | Stronger algorithms; full 128-bit key material            |
| **Integrity Protection**        | Not supported                                            | Supported for signaling traffic                           |
| **User-Plane Integrity**        | No                                                       | No                                                        |
| **Key Derivation**              | Single session key $K_c$                                 | Separate CK and IK                                        |
| **Key Separation**              | None                                                     | Explicit separation of confidentiality and integrity keys |
| **Protection Against Fake BTS** | None                                                     | Much stronger; defeated by downgrade attacks              |
| **IMSI Catcher Resistance**     | Very weak                                                | Improved but not eliminated                               |
| **Core Network Trust Model**    | Trusted core assumed; no protection                      | More security-aware; network domain security defined      |
| **Signaling Security**          | None                                                     | Integrity-protected signaling                             |
| **Session Freshness**           | RAND only                                                | RAND and SQN                                              |
| **SIM/USIM**                    | SIM                                                      | USIM with extended capabilities                           |
| **Cryptographic Philosophy**    | Security through obscurity; proprietary algorithms       | Standardized, open design                                 |
| **Primary Remaining Weakness**  | No mutual authentication                                 | Legacy GSM interworking and downgrade attacks             |