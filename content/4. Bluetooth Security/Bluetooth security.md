## Bluetooth security services and model
Bluetooth provides three core security services at the protocol level: **authentication**, **authorization**, and **confidentiality**.

- **Authentication** in Bluetooth operates at the device level. The protocol verifies the identity of communicating devices, confirming that a remote device is who it claims to be. Native Bluetooth does not provide user authentication; only entity (device) authentication is supported by the standard.
- **Authorization** controls access to resources and services. A device must be explicitly authorized before it can use a specific Bluetooth service, allowing a device to restrict which remote devices can interact with which of its capabilities.
- **Confidentiality** protects user data by encrypting it before transmission. This protection is applied at the link layer and operates in addition to any physical-layer mechanisms such as frequency hopping.

### The Bluetooth security model
The Bluetooth security model is structured around five distinct features that together provide a complete framework for secure communication between devices.

- **Pairing** is the process of generating, distributing, and authenticating the cryptographic keys used for encryption. It is the initial step that establishes a security relationship between two devices.
- **Bonding** refers to storing the keys created during pairing so that they can be reused in future connections. Bonded devices form a trusted pair and do not need to repeat the full pairing process on each reconnection.
- **Device authentication** verifies that both devices share the same keys, confirming that the remote device is the same one that was previously paired.
- **Encryption** provides message confidentiality by ciphering the data exchanged over the link.
- **Message integrity** protects against forgeries, ensuring that messages cannot be altered in transit without detection.

### Pairing: evolution and types
Pairing mechanisms have changed significantly across Bluetooth versions. Three generations can be identified: **legacy pairing**, **Secure Simple Pairing** (_SSP_), and **LE Secure Connections** (_LESC_).

#### Legacy pairing
Legacy pairing applies to Bluetooth 2.0 and earlier. It uses a proprietary stream cipher that is considered broken and cryptographically weak. The security of the pairing depends entirely on a **PIN code** shared between the two devices. This PIN provides the only source of entropy in the key derivation process.

Legacy pairing supports three association models, which are the methods used to verify the PIN between devices:

- **Just Works**: the PIN is fixed at 0000, requiring no user interaction.
- **Passkey entry**: one device displays a 6-digit PIN and the user enters it on the other device, which requires a keyboard.
- **Out-Of-Band** (_OOB_): authentication is performed using a separate communication channel, such as **Near Field Communication** (_NFC_).

Because the entire keyspace is at most one million values (for a 6-digit PIN) or ten thousand (for a 4-digit PIN), an attacker who records a pairing exchange and a subsequent authentication exchange can perform an **offline brute-force attack** to recover the PIN. This is a fundamental weakness of the legacy pairing design.

#### Secure Simple Pairing
**Secure Simple Pairing** (_SSP_) was introduced in Bluetooth 2.1 and is also supported in Bluetooth Low Energy 4.0 and 4.1 for backwards compatibility. Its primary goal is to simplify the pairing procedure for the user, with secondary goals of maintaining or improving the overall security of Bluetooth.

SSP introduces a fourth association model, **numeric comparison**, in which both devices display a 6-digit number and the user confirms that the two numbers match. The full set of association models in SSP is therefore: Just Works, Numeric Comparison, Passkey Entry, and Out-Of-Band.

The pairing procedure in SSP is organized into three phases:

1. Initiate pairing and exchange pairing feature information.
2. Perform pairing: establish an encrypted connection with user authentication via PIN, and generate the cryptographic keys.
3. Distribute the derived keys.

Importantly, in SSP the PIN is used only for the authentication process and is **not** part of the link key calculation. Device authentication and encryption in SSP use the same mechanisms as legacy BR/EDR pairing.

#### LE Secure Connections
**LE Secure Connections** was introduced in Bluetooth 4.2 and applies to both Bluetooth Classic and Bluetooth Low Energy. It replaces SSP as the preferred pairing mechanism and is based on **Elliptic Curve Diffie-Hellman** (_ECDH_) key exchange combined with strong encryption protocols, providing significantly stronger protection for the key distribution process.

