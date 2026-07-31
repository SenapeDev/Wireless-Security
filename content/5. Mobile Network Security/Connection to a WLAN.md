## Connection process: joining a WLAN

Before a station can exchange data through an AP, it must complete a structured **join process** consisting of three phases: **discovery**, **authentication**, and **association**. Data exchange is only possible once all three phases are complete.

### Discovery: beacons and probes

APs periodically broadcast **beacon frames** at a fixed interval (typically every 100 ms). A beacon contains information about the network, including the **SSID** (Service Set Identifier, the network name), supported data rates, the beacon interval, capability information, and security parameters such as the supported WPA version. Beacons allow nearby stations to discover which networks are available without actively scanning.

A station looking to join a network can also actively search by sending **probe request frames** on multiple channels. A probe request may include a specific SSID if the station is looking for a known network, or it may be sent with no SSID specified, in which case all APs that receive it will respond, except those configured to suppress broadcast SSID responses. The AP replies with a **probe response** containing the same information carried in a beacon: SSID, supported data rates, security standard, and other parameters. The probe request itself carries information about the station's capabilities: the SSID it wants to join, the bit rates it supports, security features it supports, and so on.

### Authentication

**Authentication** is the first formal step in establishing a connection. At this stage, the station establishes its identity with the AP. There are two basic approaches defined in 802.11.

- **Open system authentication** is the simplest form. The station sends an authentication request containing its MAC address, and the AP responds with either success or failure. There is no secret involved and no cryptographic verification of identity. Open system authentication by itself provides no security; it is simply a signaling step that must occur before association.
- **Shared key authentication** involves a pre-shared secret (a passphrase) configured on both the station and the AP. This is the basis for the following widely used security schemes:

- **WEP** (*Wired Equivalent Privacy*): the original shared-key mechanism, now broken and deprecated.
- **WPA** (*Wi-Fi Protected Access*): introduced as an interim improvement over WEP.
- **WPA2**: the dominant standard for many years, based on the IEEE 802.11i amendment and using AES-CCMP for encryption.
- **WPA3**: the current standard, offering stronger protections including Simultaneous Authentication of Equals (SAE) to replace the Pre-Shared Key handshake.

In infrastructure networks with multiple APs forming an **Extended Service Set** (*ESS*), a station may authenticate with more than one AP before associating. This is common in large deployments such as university campus networks (e.g., eduroam), where a station roaming across the campus may pre-authenticate with neighboring APs to speed up future handovers.

### Association

Once authentication is complete, the station sends an **Association Request** to a single AP. The AP evaluates the request and, if it accepts the station, responds with a status code of 0 (success) and an **Association ID** (*AID*). The AID is used to identify the station when the AP needs to buffer frames for it during power-saving periods. If the association fails, the AP returns only a failure status code.

A station can be associated with **only one AP at a time**. Association registers the station with the AP so that frames can be properly delivered to it. After association, the AP forwards frames to and from the station. Association does not occur in ad-hoc (peer-to-peer) mode; it is specific to infrastructure networks.