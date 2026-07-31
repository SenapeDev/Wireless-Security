## Evolution of WLAN security standards
Rather than patching WEP's individual flaws, **802.11i** redesigned the security model from the ground up, introducing a layered architecture that separates authentication, access control, key management, and data protection into distinct, well-defined components.

The evolution of WLAN security can be summarized chronologically: 
- In 1997, the original IEEE 802.11 standard introduced **WEP**, which used RC4 with a shared key and is now completely broken. 
- In 2003, **WPA** (*Wi-Fi Protected Access*) was introduced as a transitional measure, retaining RC4 but adding **TKIP** (*Temporal Key Integrity Protocol*) on top, and supporting both **pre-shared key** (*PSK*) and 802.1X-based authentication. 
- In 2004, WPA2 formalized the IEEE 802.11i standard, replacing RC4 with AES in CCMP mode and providing strong security. 
- In 2018, **WPA3** introduced **SAE** (*Simultaneous Authentication of Equals*), a Diffie-Hellman-based authentication mechanism that provides stronger password-based security and forward secrecy.

The industrial naming convention maps as follows: TKIP-based operation is called WPA, while the Robust Security Network (RSN) using AES-CCMP is called WPA2. Both fall under the 802.11i umbrella.

## The 802.11i security architecture
The 802.11i architecture addresses each of WEP's documented failures through specific, targeted design choices. The key improvements over WEP are:

- **Authentication** is no longer based on a shared secret alone. Instead, 802.11i adopts the 802.1X access control model with the **Extensible Authentication Protocol** (*EAP*) as a flexible carrier for upper-layer authentication protocols such as TLS.
- **Integrity** is no longer based on CRC-32. TKIP uses the Michael keyed hash function, and WPA2 uses CBC-MAC as part of AES-CCMP, both of which are cryptographically sound.
- **Encryption** is improved: TKIP applies per-packet key derivation on top of RC4 to eliminate weak-key and IV-reuse problems; WPA2 replaces RC4 entirely with AES in counter mode.
- **Key management** uses a hierarchical derivation model. No single static key is shared and used directly for both authentication and encryption. Instead, a master key is established through authentication and all operational keys are derived from it using one-way pseudorandom functions.
- **Replay protection** is implemented through sequence counters associated with each packet.

The overall flow of 802.11i proceeds through four phases: 
1. **authentication** (establishing who the client is)
2. **access control** (deciding whether to allow entry)
3. **key management** (deriving session keys through the four-way handshake)
4. **data protection** (encrypting and integrity-protecting frames using TKIP or CCMP).

## IEEE 802.1X authentication model

### Overview of 802.1X
IEEE 802.1X is a standard originally defined for Ethernet (IEEE 802.3) in 2001 and later clarified to cover IEEE 802.11 wireless networks. It defines the encapsulation of the Extensible Authentication Protocol (EAP) over LAN protocols, known as EAPoL (EAP over LAN). In the context of WLANs, 802.1X provides the access control framework that gates network access based on the outcome of an authentication exchange.

The 802.1X model involves three roles:

- The **supplicant** is the device seeking access to the network (the STA in WLAN terms).
- The **authenticator** is the device that controls access to the network (the AP in WLAN terms). It enforces a logical port that starts in a blocked state and is opened only after successful authentication.
- The **authentication server** is the entity that actually verifies the supplicant's credentials and authorizes access. In practice, this is typically a RADIUS server.

The authentication flow works as follows: the supplicant authenticates itself to the authentication server through EAP messages relayed by the authenticator. If authentication succeeds, the authentication server instructs the authenticator to open the controlled port, and the supplicant is informed that access is granted. The authenticator itself does not interpret the content of EAP messages; it only recognizes EAP success and failure signals.

![[Pasted image 20260423114056.png]]

An important extension in 802.11i is that successful authentication produces not just a port-open signal, but also a **session key** shared between the supplicant and the authentication server. This key is then securely delivered to the AP, allowing it to participate in subsequent key derivation. The channel between the AP and the authentication server for key transport typically relies on a pre-configured shared key established manually by the network administrator.

### Protocols: EAP, EAPoL, and RADIUS
**EAP** *(Extensible Authentication Protocol*, RFC 3748) is a carrier protocol designed to transport the messages of concrete authentication protocols. It is intentionally generic and defines only four message types: 
- request (from the authentication server to the supplicant)
- response (from the supplicant to the authentication server)
- success
- failure

EAP does not specify a particular authentication algorithm; instead, it encapsulates whatever authentication protocol is negotiated, such as TLS. The authenticator (AP) acts as a transparent relay for EAP messages and only needs to recognize success and failure outcomes.

- **EAPoL** (EAP over LAN, defined in 802.1X) encapsulates EAP messages for transport over LAN protocols such as Ethernet or 802.11. EAPoL is used on the segment between the supplicant (STA) and the authenticator (AP).

- **RADIUS** (Remote Authentication Dial-In User Service, RFC 2865-2869) carries EAP messages between the AP and the authentication server. The MS-MPPE-Recv-Key attribute in RADIUS is used to transport the session key from the authentication server to the AP. RADIUS is mandated by WPA and is optional in RSN.

![[Pasted image 20260423113655.png]]
### EAP authentication methods

Several concrete authentication protocols can be carried over EAP:

- **LEAP** (*Lightweight EAP*) was developed by Cisco. It is similar to MS-CHAP extended with session key transport. LEAP has known weaknesses and is no longer recommended.

- **EAP-TLS** (*TLS over EAP*) uses the TLS Handshake Protocol to provide mutual authentication between the client and the server and to establish a shared master secret. Only the handshake portion of TLS is used. The TLS master secret becomes the session key. EAP-TLS is mandated by WPA and optional in RSN, and it requires both the server and the client to have a certificate.

- **PEAP** (*Protected EAP*) operates in two phases. In phase 1, a TLS tunnel is established using only server-side authentication, creating a protected channel. In phase 2, the client authenticates itself within the protection of that tunnel. This allows weaker client authentication mechanisms to be used without exposing credentials on the wire.

- **EAP-SIM** extends the GSM authentication mechanism to the WiFi context. The STA identifies itself by its IMSI (or a pseudonym), and the AP retrieves authentication triplets from the mobile operator's Authentication Center (AuC). The AP sends two RAND values along with a MIC and optionally a new pseudonym, and the STA responds with the corresponding SRES values.

### WPA-Personal vs. WPA-Enterprise
- WPA supports two authenticated key management modes. **WPA-Personal** (also called **WPA-PSK**) is designed for home and small office environments. It uses a manually configured **pre-shared key** (PSK) for authentication. No authentication server is required. 
- **WPA-Enterprise** (also called WPA-802.1X) requires a centralized RADIUS authentication server and enforces mutual authentication. Enterprise mode is used in organizational networks such as university eduroam deployments, where individual user credentials are verified against a central directory.

## Key hierarchy and derivation

A central design improvement in 802.11i over WEP is **key separation**: different derived keys are used for different cryptographic purposes, and no single long-term secret is ever used directly for data encryption.

The key hierarchy proceeds through several levels:

- **PMK** (*Pairwise Master Key*) is a 256-bit long-term key that serves as the root of the per-client key hierarchy. It is never used directly for data protection. 
  - In WPA-Personal, the PMK is derived from the pre-shared password using `PBKDF2` with the SSID as a salt, iterated 4096 times (RFC 2898). 
  - In WPA-Enterprise, the PMK is derived from the Master Session Key produced by the EAP authentication exchange.

- **PTK** (*Pairwise Transient Key*) is the per-session key used to protect unicast traffic between a specific STA and the AP. The PTK is derived from the PMK by applying a pseudorandom function (PRF) over the following inputs:
	- the PMK
	- a nonce generated by the AP (**ANonce**)
	- a nonce generated by the STA (**SNonce**)
	- the AP's MAC address
	- the STA's MAC address
	
	Including both nonces and MAC addresses ensures that the PTK is unique to each session and each pair of devices, even if the PMK is the same. The PTK is transient because a new one is derived every time a client associates with the AP. 
	In CCMP mode the PTK is 384 bits long, and in TKIP mode it is 512 bits. 
	The PTK is divided into three sub-keys: 
	- the **KCK** (EAPOL *Key Confirmation Key*, 128 bits) used to compute MICs over handshake messages 
	- the **KEK** (EAPOL *Key Encryption Key*, 128 bits) used to encrypt the GTK during the handshake 
	- the **TK** (*Temporal Key*, 128 bits for CCMP or 256 bits for TKIP) used for data encryption and integrity
	
	![[Pasted image 20260423145513.png|414]]

- **GTK** (*Group Transient Key*) is the shared key used to protect broadcast and multicast traffic addressed to all stations in the network. The GTK is generated by the AP and distributed to all authenticated clients during the handshake. It is changed whenever a client disassociates or deauthenticates, since the departing client should no longer be able to decrypt group traffic.

- **GMK** (*Group Master Key*) is a 256-bit key generated by the authentication server and used as the root for deriving the GTK. It is changed periodically or when compromised.

## The four-way handshake
The **four-way handshake** is the key management protocol used in 802.11i to accomplish several goals simultaneously: prove that both the STA and the AP possess the same PMK (**mutual proof of key knowledge**), exchange random nonces needed to derive the PTK, distribute the GTK to the STA, and confirm that both parties have installed their keys correctly before data transmission begins.

All four messages are EAPOL Key frames. The MIC fields are computed using the KCK, which is derived as part of the PTK. Because the PTK includes the PMK, a correct MIC serves as proof that both parties hold the same PMK without ever transmitting it.

1. Message 1 (**AP to STA**): The AP generates a random value called ANonce and sends it to the STA in cleartext with no integrity protection. If this message is tampered with, the handshake will simply fail because the derived PTKs will not match. The STA, upon receiving ANonce, now has all inputs needed to compute the PTK: its own SNonce (which it generates locally), the ANonce from message 1, its own MAC address, and the AP's MAC address.

2. Message 2 (**STA to AP**): The STA sends its SNonce to the AP along with a MIC computed over the message using the KCK. This message is not encrypted but is integrity-protected. When the AP receives it, it can compute the PTK for the first time (now that it has the SNonce), derive the KCK, and verify the MIC. A correct MIC confirms that the STA possesses the same PMK.

3. Message 3 (**AP to STA**): The AP sends a key installation request to the STA, which includes the GTK (encrypted with the KEK) and a MIC computed with the KCK. The STA verifies the MIC, decrypts the GTK, and upon successful verification has confirmation that the AP also possesses the correct PMK.

4. Message 4 (**STA to AP**): The STA sends an acknowledgment with a MIC. Upon receiving and verifying this message, the AP installs the PTK and GTK and opens the controlled port, authorizing data traffic. The STA installs its keys upon sending message 4.

![[Pasted image 20260423150545.png]]
### Offline dictionary attack on WPA-PSK
The four-way handshake, while sound in its design, introduces a significant vulnerability in WPA-Personal mode: **a passive attacker who captures the handshake can perform a fully offline dictionary or brute-force attack to recover the password**.

The attack works because all the information needed to verify a password guess is transmitted in cleartext during the handshake. The attacker observes the SSID, the ANonce, the SNonce, the MAC addresses of both parties, and the MIC from message 2 or message 3. Given a candidate password, the attacker can compute the PMK using PBKDF2, derive the PTK from the PMK and the observed nonces and MAC addresses, compute the KCK, and then compute the expected MIC. If it matches the captured MIC, the password is correct.

This attack is entirely offline, requires no further interaction with the network, and can be accelerated significantly using GPU-based tools. The attacker can capture the handshake passively by waiting for a legitimate client to connect, or can force a reconnection by sending a spoofed deauthentication frame to an associated client.

The security of WPA-Personal therefore depends entirely on the entropy of the password. A directly entered 256-bit PSK provides $2^{256}$ combinations. An 8-character alphanumeric password provides approximately $2^{48}$ combinations. Dictionary words and common password patterns reduce the search space further, sometimes to millions of candidates.

To capture the handshake in practice, an attacker places the wireless adapter in monitor mode using a tool such as `airodump-ng`, then forces a reconnection by sending a deauthentication frame using `aireplay-ng`. The captured handshake file is then submitted to a cracking tool such as Aircrack-ng or Hashcat, with the latter supporting GPU acceleration.

## TKIP: transitional integrity and confidentiality

TKIP was designed as a backward-compatible fix for WEP, intended to run on legacy hardware after a firmware upgrade. It retains RC4 as the underlying stream cipher but corrects all of WEP's specific design flaws.

TKIP introduces four improvements over WEP:

- **Per-packet key derivation:** Instead of concatenating the IV with the shared secret as WEP does, TKIP applies a two-phase key mixing function that combines the PTK's temporal key with the sender's MAC address and the 48-bit IV to produce a unique 104-bit per-packet RC4 key. This eliminates the weak-key vulnerability because the relationship between the IV and the RC4 seed is cryptographically obscured.

- **Enlarged IV space:** The IV is expanded from 24 bits to 48 bits, providing approximately $2^{48} \approx 281$ trillion unique values. This makes IV exhaustion infeasible in practice.

- **Replay protection:** The 48-bit IV doubles as a packet sequence counter (TSC). The receiver rejects any packet whose sequence counter is not strictly greater than the last accepted value, preventing replay attacks.

- **Michael MIC:** A 64-bit Message Integrity Code (MIC) computed by the Michael algorithm is appended to each frame before encryption. Michael is a keyed hash function, unlike CRC-32, and its output depends on a secret key (derived from the PTK) as well as the plaintext. This closes the malleability vulnerability that allowed bit-flipping attacks in WEP. CRC-32 is still computed as a frame check sequence for error detection at the link layer, but it no longer serves as the security integrity check.

![[Pasted image 20260423160346.png]]

>[!danger] TKIP countermeasure
>If an attacker attempts a modified ChopChop-style attack against TKIP, they can still exploit the linearity of CRC-32 to test a single byte guess. However, TKIP imposes a countermeasure: if two incorrect Michael MIC values are received within 60 seconds, the AP triggers a rekeying of the TKIP session key, changing the keystream for all subsequent packets. This rate-limiting degrades the attack's effectiveness significantly.

Despite these improvements, TKIP inherits the fundamental structural limitations of RC4. It is considered a **transitional solution** and is not secure for long-term use. The 2-byte WPA frame counter introduces biases in the RC4 keystream, enabling statistical plaintext-recovery attacks when the same plaintext is encrypted in many different frames.

## WPA2

WPA2 replaces RC4 with AES operating in **CCMP** (*Counter Mode with CBC-MAC Protocol*) mode. This provides **authenticated encryption**, meaning both confidentiality and integrity are guaranteed by a single cryptographic construction.

CCMP uses AES with a 128-bit key and 128-bit block size. The protocol name encodes two AES modes of operation:

- **CTR mode** provides data confidentiality. A counter value is encrypted with the AES block cipher to produce a keystream, which is XORed with the plaintext. Each block uses a different counter value, ensuring that the same plaintext block encrypts to a different ciphertext in each position.

- **CBC-MAC** provides integrity and authentication. The MAC header fields, CCMP header, and the plaintext data are processed through a chain of AES encryptions in CBC mode. The final 128-bit CBC output is truncated to the upper 64 bits to produce the MIC. Mutable header fields are set to zero before CBC-MAC computation. If the input length is not a multiple of 128 bits, it is padded with zeros.

Together, the combination of CTR and CBC-MAC in the CCM construction provides strong assurance against both eavesdropping and tampering. WPA2 is the current standard for WLAN security and requires hardware that supports AES; it cannot be deployed through a firmware upgrade on WEP-era hardware.

### KRACK: key reinstallation attacks on WPA2

The most significant known vulnerability in WPA2 is the **KRACK** (*Key Reinstallation Attack*) class of attacks, published by Vanhoef and Piessens in 2017. KRACK does not break AES-CCMP cryptographically. Instead, it exploits a flaw in the state machine of the four-way handshake protocol.

The root vulnerability is that the 802.11i standard allows message 3 of the four-way handshake to be retransmitted if the AP does not receive the acknowledgment (message 4). This is a legitimate reliability mechanism for lossy wireless links. However, the standard also specifies that the STA installs the PTK upon receiving message 3 and resets its nonce counters to their initial values each time it installs a key. An adversary can exploit this by forcing repeated key reinstallations, which reset the nonces used by the data-confidentiality protocol.

Nonce reuse is **catastrophic** for stream-cipher-like constructions. In CTR mode (used by AES-CCMP) and in RC4 (used by TKIP), reusing a nonce with the same key produces the same keystream. An attacker who causes the victim to encrypt two different plaintexts with the same keystream can XOR the ciphertexts to obtain the XOR of the plaintexts, which can be used to recover both. In TKIP, nonce reuse additionally enables forgery because the authentication key used by GCMP is the same in both communication directions.

The attack proceeds as follows:
1. The adversary positions themselves as a man-in-the-middle (MitM) between the STA and the AP using a channel-based technique. They block message 4 from reaching the AP.
2. After sending message 4, the STA installs the PTK and GTK, resets its nonces, opens the 802.1X port, and begins transmitting encrypted data frames.
3. Because the AP never received message 4, it retransmits message 3. The adversary forwards this retransmitted message 3 to the STA, causing the STA to reinstall the PTK and GTK and **reset its nonce and replay counter to their initial values**.
4. To complete the handshake on the AP side, the adversary transmits an older unencrypted message 4 (using a previously valid replay counter), which many AP implementations will accept.
5. When the STA transmits its next data frame, the nonce has been reset and the data-confidentiality protocol reuses the keystream. The adversary can now replay, decrypt, and potentially forge packets.

KRACK can also be launched against the group key handshake, and against other handshake types such as Fast BSS Transition (FT) and PeerKey. The practical impact includes the ability to decrypt packets sent by clients (including sensitive data such as passwords or cookies), perform TCP connection hijacking, and inject malicious content into unencrypted HTTP connections. The severity is highest when the TKIP or GCMP encryption protocol is used instead of AES-CCMP.

The fix for KRACK requires ensuring that key installation is idempotent: a key should only be installed once, and reinstalling the same key should not reset the nonce. Patches were issued for most operating systems and access point firmware in 2017.

## WPA3
### Diffie-Hellman key agreement

WPA3 and associated extensions are built around **Diffie-Hellman** (*DH*) key exchange, a public-key technique that allows two parties to establish a shared secret over an untrusted channel without any prior shared secret. The two parties agree on a public generator `g` and a modulus `p`. Each party picks a private random value, computes a public value ($g^x$ and $g^y$ respectively), and exchanges these publicly. Each party then computes the shared secret $s = g^{xy}$, which cannot be derived from $g^x$ and $g^y$ alone without solving the discrete logarithm problem. Symmetric keys for encryption, authentication, and integrity are then derived by hashing `s` along with context labels.

A critical property of Diffie-Hellman key exchange is **forward secrecy**: if both parties delete their private values and the shared secret after deriving the session keys, then a future compromise of any long-term secret (such as the password) cannot be used to decrypt previously recorded sessions. This is because there is no long-term secret that could be used to recompute the session key.

### Opportunistic Wireless Encryption (OWE)
**OWE** (*Opportunistic Wireless Encryption*, RFC 8110) addresses a longstanding gap in WLAN security: open public networks (such as those in cafes and airports) that transmit all traffic in cleartext. OWE provides encryption of wireless traffic without requiring any pre-shared password or user credentials.

OWE uses **Elliptic Curve Diffie-Hellman** (*ECDH*). During the association process, the STA includes its ECDH public key in the Association Request frame, and the AP includes its ECDH public key in the Association Response. Both parties independently compute the shared secret `s`, from which the PMK is derived using **HKDF** (*HMAC-based Extract-and-Expand Key Derivation Function*). The PMK then feeds into the standard EAPOL four-way handshake to derive the PTK and GTK for data protection using CCMP. Both elliptic curve and finite field cryptography are supported; Group 19 (P-256 curve) is mandatory.
![[Pasted image 20260423165753.png]]
OWE replaces the concept of an open wireless network. It provides per-client encryption so that one client cannot decrypt another's traffic, and it provides forward secrecy. However, OWE does not authenticate the AP: a rogue AP can still perform an OWE handshake with a client and impersonate a legitimate network. OWE is certified by the Wi-Fi Alliance under the name Enhanced Open.

### WPA3-Personal: Simultaneous Authentication of Equals (SAE)

**SAE** (*Simultaneous Authentication of Equals*) is the major new authentication mechanism introduced in WPA3-Personal. It replaces the PSK-based four-way handshake of WPA2 with a **password-authenticated key exchange** (*PAKE*) protocol based on elliptic-curve Diffie-Hellman.

The fundamental difference from WPA2-PSK is that SAE does not transmit any value derived directly from the password over the air. Instead, the password is used to derive a group-specific generator point called the **PWE** (*Password Element*) on the elliptic curve. The PWE is a function of both the password and the MAC addresses of the two parties. The modulus `p` is taken from the standard set of elliptic curve parameters.

In the SAE handshake, both parties simultaneously send commitment messages containing their ECDH public keys (computed using the PWE as the generator), a scalar, and an element. Neither party is designated as requester or authenticator; both contribute authentication material independently and symmetrically. After exchanging commitments, both sides compute the same shared secret `ss`, from which the PMK and a **Confirmation Key** (*CK*) are derived. Each party then sends a confirmation message containing an HMAC computed over the CK and context labels. Both parties verify the peer's confirmation before considering authentication complete.
![[Pasted image 20260610123804.png]]
SAE provides several security improvements over WPA2-PSK:

- **Resistance to offline dictionary attacks:** Because no value derivable from the password alone is transmitted, a passive attacker who captures the SAE exchange cannot perform an offline password search. The attacker would need to interact with the network for every password guess (an online attack), which can be rate-limited.
- **Forward secrecy:** The PMK generated by SAE is used only for authentication purposes and is freshly derived for each connection. Even if the password is later revealed, previously recorded sessions cannot be decrypted.
- **Resistance to KRACK:** SAE replaces the PSK-based derivation step that precedes the four-way handshake, eliminating the nonce-reuse vulnerability that KRACK targets at that phase.
- **Resistance to brute-force attacks:** WPA3-SAE ensures an effective PMK combination space of at least $2^{128}$ regardless of the length or quality of the password, because the security does not reduce to a direct search over password guesses as in WPA2.

SAE does not, however, prevent **online dictionary attacks**, in which an attacker tries passwords one at a time by actually performing handshakes with the AP. Countermeasures against this include rate-limiting authentication attempts by introducing delays after failures, alerting on multiple consecutive failures, and avoiding trivially guessable passwords.

The SAE message flow in WPA3 proceeds as follows: the STA and AP perform an Open System Authentication exchange, then exchange Auth Commit messages containing their ECDH public keys, then exchange Auth Confirm messages containing HMACs of the CK and context labels. After mutual authentication is confirmed, the standard EAPOL four-way handshake follows to derive the PTK and distribute the GTK. Data protection uses CCMP with 128-bit TK and GTK, and BIP-CMAC with 128-bit IGTK for management frame protection.