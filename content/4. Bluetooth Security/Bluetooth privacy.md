## Threat model: device tracking
BLE devices transmit data continuously, and every packet includes the **Media Access Control** (_MAC_) address of the sender and receiver. This address is necessary for peer-to-peer communication but creates a significant privacy problem: a passive attacker who can receive Bluetooth packets can observe the MAC address in every advertisement and use it as a persistent identifier to track a device and, by extension, its owner across time and location without any interaction with the device.

The natural mitigation is to change the MAC address frequently so that successive observations cannot be linked to the same device. This introduces a new problem, however: if a device changes its address arbitrarily, previously paired devices can no longer recognize it, breaking the bonding relationship.

### The privacy feature and resolvable private addresses

The BLE privacy feature addresses the tracking threat by having devices use **private addresses** that are randomly generated and rotated on a regular basis, with a suggested rotation interval of 15 minutes. To solve the recognition problem for bonded devices, BLE introduces **Resolvable Private Addresses** (_RPAs_).

An RPA is generated using the **Identity Resolving Key** (_IRK_), a secret key exchanged during the bonding procedure. Because the IRK is shared only with trusted paired devices, only those devices can verify that a given private address belongs to a known peer. Untrusted observers see only a rotating random-looking address and cannot link successive addresses to the same device.

The address generation and resolution procedure works as follows.

**Address generation (device A):**

1. Generate a 22-bit random value called prand.
2. Compute a 24-bit hash: localHash = ah(IRK, prand), where `ah()` is a keyed hash function defined in the Bluetooth specification.
3. Construct the 48-bit address as: hash (24 bits) || prand (22 bits) || 10 (2-bit type prefix indicating a resolvable private address).

**Address resolution (device B):**

1. Extract the 22-bit prand from the received address.
2. Compute the expected hash: localHash = ah(IRK_A, prand), using the stored IRK of device A.
3. Compare the computed hash with the 24-bit hash field of the received address. A match confirms that the packet originates from device A.

Each device must maintain a local store of IRKs and their associated identities, which is updated during the bonding phase.

### Device address types

BLE supports two main categories of device addresses.

A **public address** is globally unique, fixed, and registered with the IEEE. It never changes and uniquely identifies the device permanently. Registration involves a cost, making public addresses typical for commercial products.

A **random address** requires no registration and can take one of three forms:

- **Static address**: randomly generated at each device boot. Its two most significant bits are set to 11. It uniquely identifies the device within a piconet for a session but may change across reboots.
- **Non-resolvable private address**: a purely random 46-bit value with the two most significant bits set to 00. It cannot be resolved by any peer and therefore does not support bonding. It is used in applications such as beacon broadcasting where no persistent identity is needed.
- **Resolvable private address**: generated using the IRK as described above, with the two most significant bits set to 10. It enables privacy against passive observers while still allowing bonding, since trusted devices holding the IRK can resolve the address.

### Privacy modes

BLE defines two privacy modes that govern how a device handles the addresses of peer devices whose IRKs it has received.

- In **Device Privacy Mode**, a device is concerned only with its own privacy. It accepts advertising packets from peer devices regardless of whether those peers use their identity address or a private address, even if the peer has previously distributed an IRK. This mode is more permissive and suited to scenarios where the local device wants to hide its own identity but does not require peers to do the same.

- In **Network Privacy Mode**, a device enforces a stricter policy. It will not accept advertising packets containing the identity address of a peer that has distributed its IRK. Only packets using a resolvable private address that can be validated against the stored IRK are accepted. This mode provides stronger mutual privacy guarantees within a bonded network.

## Bluetooth confidentiality

Bluetooth defines three encryption modes that control how data traffic is protected.

- **Encryption Mode 1**: no encryption is applied to any traffic.
- **Encryption Mode 2**: only unicast data traffic is encrypted; broadcast traffic is left unencrypted.
- **Encryption Mode 3**: all data traffic, including both unicast and broadcast, is encrypted.

The cipher used in Encryption Modes 2 and 3 depends on the Bluetooth variant. BR/EDR uses the E0 stream cipher. Both BR/EDR (with Secure Connections) and BLE use **AES-CCM** (_Advanced Encryption Standard - Counter with CBC-MAC_), which provides both encryption and message integrity in a single operation.