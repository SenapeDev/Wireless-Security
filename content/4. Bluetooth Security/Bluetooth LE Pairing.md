## Security Manager Protocol
**Bluetooth Low Energy** (_BLE_) handles all security-related functions through a dedicated component called the **Security Manager Protocol** (_SMP_). The SMP is a peer-to-peer protocol responsible for generating and managing the cryptographic keys used to protect BLE communications. It operates over a dedicated fixed **Logical Link Control and Adaptation Protocol** (_L2CAP_) channel and resides in the Host layer of the BLE stack, alongside the **Generic Attribute Profile** (_GATT_), the **Attribute Protocol** (_ATT_), and the **Generic Access Profile** (_GAP_).
![[Pasted image 20260509161118.png|419]]
The SMP is responsible for four core functions: generating encryption keys and identity keys, managing the storage of those keys, generating random device addresses, and resolving random addresses back to known device identities. This last function supports the Bluetooth privacy feature, which allows devices to use rotating addresses to prevent tracking. The SMP block is exclusive to BLE systems; in BR/EDR, equivalent functionality is provided by the Link Manager block in the Controller.

## Security levels and modes
BLE defines security in terms of two orthogonal dimensions: **security levels** and **security modes**. Security levels describe the strength of the cryptographic protection applied to a connection. Security modes describe whether data signing is applied in addition to those levels.

### Security levels
BLE defines four security levels, each building on the previous in terms of the protections provided.

1. **Security Level 1** provides no security. Communication proceeds without any cryptographic protection, making it maximally convenient but vulnerable to all categories of attack. This level applies to any Bluetooth communication.
2. **Security Level 2** requires unauthenticated pairing with encryption. Encryption keys are exchanged during pairing without any user interaction. Encryption uses AES-CMAC (standardized as AES-128 via RFC 4493 and FIPS-compliant). Because pairing involves no user interaction and therefore no out-of-band verification, connections at this level are subject to MITM attacks.
3. **Security Level 3** requires authenticated pairing with encryption. The pairing process involves user interaction, such as numeric comparison or passkey entry, in order to authenticate the connection. This level provides MITM protection, provided that a correctly authenticated association model is used and the user performs the required verification step.
4. **Security Level 4** is the highest level, requiring authenticated LE Secure Connections pairing with a 128-bit encryption key. It uses **Elliptic Curve Diffie-Hellman Ephemeral** (_ECDHE_) key exchange over the P-256 curve, which is FIPS-compliant, to protect the pairing exchange even over an insecure channel. This level is only available when both devices support LE Secure Connections.

### Security modes
A security mode defines the method a device uses to apply security to its communications. Three security modes are defined.

1. **Security Mode 1** covers communications without data signing. It can be combined with any security level from 1 to 4. This is the standard mode for encrypted connections.
2. **Security Mode 2** applies data signing to communications, including both paired and unpaired connections. It adds a **Message Authentication Code** (_MAC_) to each message to verify integrity and authenticity. This mode can be combined with security levels 2 or 3.
3. **Security Mode 3** covers security for broadcast communications, which have different requirements from the unicast connection-oriented model of Modes 1 and 2.

## BLE pairing: overview and key types
BLE pairing is the process of establishing the cryptographic keys needed to secure a link. Two pairing methods exist depending on the Bluetooth version: **LE Legacy Pairing**, used in Bluetooth 4.0 and 4.1, and **LE Secure Connections**, used in Bluetooth 4.2 and later. Both methods share the same three-phase structure but differ in their cryptographic mechanisms and the type of key produced in Phase 2.

Pairing generates keys that serve several distinct purposes beyond link encryption. Keys generated during pairing can be used to encrypt the link in future reconnections, to verify signed data, and to perform random address resolution. The full set of keys involved in BLE pairing and bonding is as follows.

### Pairing keys
- **TK** (_Temporary Key_): a short-lived value determined by the association model in use. Its value is always 0 in Just Works, a 6-digit PIN in Passkey Entry, and a 128-bit value in OOB. The TK is used as the key input to the encryption engine that generates the STK.
- **STK** (_Short Term Key_): used to encrypt the connection during the very first pairing session, specifically for the purpose of distributing the LTK securely. It is derived from the TK and two random numbers contributed by each device: $STK = E_{TK}(Srand || Mrand)$, where $Srand$ is contributed by the peripheral and $Mrand$ by the central. The STK is used only for the initial pairing and LTK distribution; it is not retained for subsequent connections.

### Bonding keys
- **LTK** (_Long Term Key_): distributed once the initial pairing procedure has established an encrypted connection. The LTK is a random number stored in a security database and is derived by both devices during pairing. It is the key used to re-encrypt the link on future reconnections without repeating the full pairing procedure.
- **IRK** (_Identity Resolving Key_): allows a device that knows a peer's IRK to resolve that peer's random address to its true identity. This key is used in the Bluetooth privacy feature.
- **CSRK** (_Connection Signature Resolving Key_): allows a receiving device to verify the signature on a message and thereby authenticate the sender. It is used to sign data sent over unencrypted links, corresponding to Security Mode 2.

## Pairing phases
Both LE Legacy Pairing and LE Secure Connections follow the same three-phase structure.
![[Pasted image 20260509162717.png|608]]
### Phase 1: Pairing Feature Exchange
The initiating and responding devices exchange their security capabilities and requirements. This exchange is carried out using a Pairing Request packet sent by the initiator and a Pairing Response packet sent by the responder. Together, these packets form the basis for selecting the association model and the pairing method to be used.

The pairing request and response packets share the same format. The key fields are:
![[Pasted image 20260509162849.png]]
- **IO Cap** (1 byte): reports the device's input and output capabilities, which determine which association model can be used. Input capabilities are classified as: 
	- No Input, 
	- Yes/No (at least two buttons), 
	- Keyboard (numeric entry 0-9 plus confirmation). 
	
	Output capabilities are classified as: 
	- No Output
	- Numeric Output (ability to display a 6-digit decimal number). 
	
	The combination of local input and output capabilities maps to a specific IO capability value.

- **OOB** (1 byte): indicates whether the device has access to an out-of-band channel such as NFC.

- **AuthReq** (1 byte): an authentication requirements field containing several flags. 
	- The **BF** (Bonding Flags) subfield indicates whether the devices should exchange and store long-term keys after pairing. 
	- The **MITM** flag requests MITM protection. 
	- The **SC** (Secure Connections) flag indicates support for LE Secure Connections; if both devices set this flag, LE Secure Connections is used, otherwise LE Legacy Pairing is used. 
	- The **KP** (Keypress) flag is used in the Passkey Entry protocol to signal keypress notifications.

- **Maximum Encryption Key Size** (1 byte): negotiates the key size, ranging from 7 to 16 bytes.

- **Initiator Key Distribution** and **Responder Key Distribution** (1 byte each): indicate which keys (LTK, CSRK, IRK) each device will distribute in Phase 3.

### Phase 2: pairing and key generation
The content of Phase 2 differs between the two pairing methods. 
- In LE Legacy Pairing, Phase 2 generates the **Short Term Key** (_STK_). 
- In LE Secure Connections, Phase 2 generates the **Long Term Key** (_LTK_) directly, without the intermediate STK step. 

 In both cases, Phase 2 includes an optional authentication step (depending on the association model), followed by key generation and link encryption.

### Phase 3: transport-specific key distribution
After the link is encrypted with the key generated in Phase 2, both devices distribute the bonding keys over the encrypted link. These include the LTK (for link encryption in future sessions), the CSRK (for data signing), and the IRK (for address privacy).

## LE Legacy Pairing: Phase 2 key generation

In LE Legacy Pairing (Bluetooth 4.0 and 4.1), Phase 2 uses the **Temporary Key** (_TK_) as the root secret. The TK is established out-of-band via the association model: it is 0 in Just Works, a user-entered 6-digit PIN in Passkey Entry, or a 128-bit value transferred via OOB.

The STK generation procedure in Phase 2 proceeds as follows:

1. Both devices set the TK value based on the association model. In Passkey Entry, the device with a screen displays the TK to the user, and the user enters it on the other device.
2. Each device independently generates a 128-bit random number: the central generates Mrand and the peripheral generates Srand.
3. Each device computes a confirmation value that commits it to its random number without revealing it:
    - $Mconfirm = c_{1}(TK, Mrand, pairing info, AddrM, AddrS)$
    - $Sconfirm = c_{1}(TK, Srand, pairing info, AddrM, AddrS)$
4. The devices exchange their confirmation values, then reveal their random numbers (Mrand and Srand). Each device verifies that the other's confirmation value is consistent with the revealed random number, confirming that the peer holds the correct TK.
5. The STK is derived as: $STK = S_1(TK, Srand, Mrand) = AES-128(TK, Srand || Mrand)$. The link is then encrypted using the STK.

## LE Secure Connections: Phase 2 key generation with ECDH

LE Secure Connections, available from Bluetooth 4.2, replaces the TK/STK mechanism with an ECDH-based key exchange that generates the LTK directly. The protocol uses the P-256 elliptic curve and employs two dedicated functions: `f4()`, used to compute a cryptographic confirmation value (commitment), and `g2()`, used to generate the 6-digit numeric comparison value displayed to the user.

The full Phase 2 procedure is as follows:

1. Both devices generate ECDH key pairs. Each device holds a private key (SKa or SKb) and a corresponding public key (PKa or PKb). The devices exchange their public keys. Both independently compute the **Diffie-Hellman key**: DHKey = P256(SKa, PKb) = P256(SKb, PKa).
2. Both devices independently generate a 128-bit nonce: the initiator generates Na and the responder generates Nb. The nonces prevent replay attacks.
3. The responder computes a commitment value Cb = f4(PKb, PKa, Nb, 0) and sends Cb to the initiator before revealing Nb. This implements a **commitment scheme**: by sending Cb first, the responder binds itself to Nb and cannot change it after seeing Na. This is a critical security property.
4. The initiator sends Na to the responder.
5. The responder then reveals Nb.
6. The initiator verifies that Cb = f4(PKb, PKa, Nb, 0) using the now-revealed Nb. If the check fails, the pairing is aborted.
7. Both devices compute the 6-digit comparison value: Va = g2(PKb, PKa, Na, Nb) and Vb = g2(PKb, PKa, Na, Nb). The user is shown Va on the initiator and Vb on the responder and confirms that they match.
8. Both devices compute the LTK from the DHKey and the exchanged parameters.

![[Pasted image 20260611175455.png]]
### Why the comparison value cannot be forged by a passive observer

The function `g2()` takes PKa, PKb, Na, and Nb as inputs, all of which are transmitted in plaintext. A passive attacker who records these values can therefore compute the same 6-digit number. However, this does not break the security of the protocol, because the 6-digit value is not a secret: it is a **consistency check** that both devices derived the same ECDH shared secret.

The protection against MITM attacks comes from the fact that an active attacker cannot make both sides compute the same comparison value. In a MITM attack, the attacker must intercept and replace the public keys, establishing two independent ECDH sessions: one with the initiator (using PKa and the attacker's own public key PKt) and one with the responder (using PKt and PKb). Because the inputs to `g2()` differ between the two sessions, the two devices compute different 6-digit values and the user will see a mismatch, detecting the attack.

### Why the commitment must be sent before the nonce

The ordering in which B sends Cb before revealing Nb is essential to the security of the protocol. The commitment Cb = f4(PKb, PKa, Nb, 0) binds the responder to a specific value of Nb before the initiator has sent Na. This ensures that neither the responder nor an attacker can choose Nb adaptively based on Na.

If the responder were to send Nb before Cb, an attacker acting as a MITM could observe Nb and then select their own public key PKt and nonce Nt adaptively to compute a forged confirmation value that is consistent with the observed Nb. The attacker could then craft protocol messages that cause both devices to compute matching confirmation values and display the same g2() output, defeating Numeric Comparison and Passkey Entry entirely. The commitment scheme prevents this by forcing the responder to commit to Nb before the attacker has seen Na and can therefore not adapt their values to both sides simultaneously.