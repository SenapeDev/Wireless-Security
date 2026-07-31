## Denial of service attacks

A **denial of service** (_DoS_) attack against Bluetooth targets device availability rather than confidentiality or authentication. The general approach is to flood a victim device with pairing requests or advertising packets to disrupt its normal operation.

A notable example was demonstrated at DEF CON 31 in 2023. Because BLE advertising packets do not require a pairing relationship to be sent or received, an attacker can transmit spoofed advertising packets at high volume without any prior interaction with the target. In this case, a device based on a Raspberry Pi was used to impersonate the BLE advertising signals normally emitted by Apple TVs, causing nearby Apple devices to repeatedly display unsolicited system-level connection prompts. Comparable tools have been implemented on consumer hardware such as the Flipper Zero. Beyond being disruptive, this class of attack can cause real harm: reported cases include interference with Bluetooth-connected medical devices such as insulin pumps.

An earlier, simpler variant of Bluetooth-based unsolicited messaging is **bluejacking**, first documented in 2001. Bluejacking exploits the **Object Exchange** (_OBEX_) protocol to send an unsolicited vCard to any discoverable Bluetooth device within range. The attacker places an arbitrary message in the name field of the vCard. The technique was originally used for novelty contact sharing (sometimes called "bluedating") but the same mechanism can be used to deliver phishing messages or prompt the recipient to interact with a malicious device.

## Bluesnarfing

**Bluesnarfing** is a more serious attack in which an attacker exploits a Bluetooth connection to gain unauthorized access to data stored on a target device, such as contacts, messages, calendars, or files. The attack targets devices that expose file-transfer profiles without adequate authentication. First publicly disclosed in 2003, bluesnarfing is considered a privacy violation and is illegal in most jurisdictions. A related variant, **bluesniping**, uses specialized directional antenna equipment to carry out the same attack at distances significantly greater than the standard Bluetooth range.

## BIAS: Bluetooth Impersonation AttackS

A structurally important class of attacks against the Bluetooth authentication model is the **Bluetooth Impersonation AttackS** (_BIAS_), documented by Antonioli, Tippenhauer, and Rasmussen at the IEEE Symposium on Security and Privacy in 2020.

The root cause is that the legacy BR/EDR authentication procedure provides only **unilateral authentication**: only one device in the connection proves knowledge of the long-term key to the other, not both. Secure Connections remedied this by providing a mutual authentication procedure. However, the Bluetooth standard does not require two devices that previously paired using Secure Connections to also use Secure Connections for every subsequent connection establishment. This means an attacker can force a **downgrade** to the legacy unilateral authentication procedure, even between two devices that both support Secure Connections.

In the BIAS attack, an attacker (Charlie) who knows that Alice and Bob share a long-term key attempts to impersonate one of them to the other. Charlie initiates a connection with Alice while claiming to be Bob. Because the legacy authentication protocol does not require Charlie to prove knowledge of the key symmetrically, and because the Bluetooth standard permits the secure connection establishment to use the legacy procedure even when Secure Connections was used for pairing, Alice does not detect that she is not talking to Bob. The attacker can then complete session key negotiation and activate a secure link without ever having authenticated correctly.

The downgrade variant of the attack proceeds during the feature exchange phase: Charlie, connecting as Bob, declares that Secure Connections is not supported, while Alice truthfully declares that it is. The standard permits this mismatch to result in a fallback to Legacy Secure Connections, which is neither encrypted nor integrity-protected during the feature exchange itself, allowing the attacker to complete the impersonation.

## Relay attacks

A **relay attack** exploits Bluetooth-based proximity authentication systems. Many devices, such as keyless entry systems for vehicles, use Bluetooth signal presence as a proxy for physical proximity: the assumption is that a credential stored on a phone can only be transmitted when that phone is within Bluetooth range of the vehicle. A relay attack defeats this assumption by extending the effective range of the Bluetooth link through a transparent tunnel between two colluding attackers.

The attack requires two attackers operating cooperatively. Attacker 1 is positioned near the target vehicle but out of range of the legitimate phone. Attacker 2 is positioned near the legitimate phone. The two attackers share an internet connection or other high-bandwidth channel.

The attack proceeds as follows:

1. Attacker 1 sends a signal to the vehicle while impersonating the legitimate phone.
2. The vehicle replies with an authentication request.
3. Attacker 1 captures this request and forwards it to Attacker 2.
4. Attacker 2 forwards the request to the legitimate phone, which is within range.
5. The phone responds with its credential.
6. Attacker 2 captures the credential and relays it back to Attacker 1.
7. Attacker 1 sends the credential to the vehicle, which accepts it and unlocks.

The attack is effectively a **remote replay** of the authentication exchange. The vehicle accepts the credential because it is cryptographically valid; it has no means of detecting that the exchange was relayed across a long physical distance.

Proposed mitigations include measuring round-trip latency (since relaying introduces measurable delay), automatically disabling the key on the phone when it has been stationary for more than a defined threshold such as 30 seconds, and requiring explicit user interaction before transmitting credentials.

## Brute-forcing the Temporary Key in LE Legacy Pairing

LE Legacy Pairing (Bluetooth 4.0 and 4.1) was acknowledged to be broken by design. The Bluetooth Core Specification for versions prior to 4.2 explicitly states that none of the LE legacy pairing methods provide protection against a passive eavesdropper.

The attack proceeds as a cascading key recovery. An attacker (Trudy) who observes the pairing exchange between Alice and her BLE device can recover all session keys from the recorded traffic:

1. **Recover the TK**: the TK has a very small keyspace. In Just Works it is always 0. In Passkey Entry it is a 6-digit integer, giving at most 1,000,000 possible values. Trudy can enumerate all of them and identify the correct one by checking consistency with the observed confirmation values, which are computed as AES(TK, AES(TK, rand XOR p1) XOR p2). The confirmation value structure means that the correct TK can be verified offline against the captured pairing exchange.
2. **Recover the STK**: with the TK and the pairing data (including the exchanged random numbers), Trudy can recompute the STK = AES-128(TK, Srand || Mrand).
3. **Recover the LTK**: with the STK, Trudy can decrypt the encrypted LTK distribution that follows in Phase 3, obtaining the long-term key and gaining the ability to decrypt all future sessions between the two devices.

This full attack chain is implemented in publicly available tools such as crackle. The fundamental fix, implemented in Bluetooth 4.2 with LE Secure Connections, is to replace the low-entropy TK with an ECDH-based key exchange so that no small keyspace is available for offline enumeration.