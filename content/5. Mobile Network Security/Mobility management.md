Because users can move freely within the service area, they may connect to different base
stations at different times. The network must continuously track user positions and route
traffic to wherever the user currently is. This overall function is called **mobility
management**.
![[Pasted image 20260601175323.png]]
Mobility management operates in two distinct modes depending on the activity state of the
terminal: **idle mobility** and **active mobility**.

## Identifiers in mobile networks

Mobile networks use a large number of distinct identifiers, each serving a specific
function. This multiplicity is not redundant; it exists because different network functions
require different forms of identity, and no single identifier can efficiently solve all
problems simultaneously. The key requirements are authentication, call routing, mobility
tracking, roaming support, fraud prevention, and user privacy. The main categories of
identifiers are:

**Telephone numbers** are used for routing calls and data sessions to the correct
destination:

- **MSISDN** (*Mobile Station ISDN Number*): the standard public telephone number of a
  mobile subscriber, used to reach the subscriber from any phone.
- **MSRN** (*Mobile Station Roaming Number*): a temporary number assigned during call
  routing to allow the network to reach a roaming subscriber.
- **HN** (*Handover Number*): a temporary number used internally during a handover to
  redirect an active call.

**User and terminal identities** are used for authentication, subscription management, and
device tracking:

- **IMSI** (*International Mobile Subscriber Identity*): a globally unique identifier stored
  on the SIM card that identifies the subscriber to the network. It is used for
  authentication and mobility management.
- **TMSI** (*Temporary Mobile Subscriber Identity*): a temporary identifier assigned by the
  network to replace the IMSI on the radio interface. Using a TMSI instead of the IMSI
  protects subscriber privacy by preventing passive interception of the permanent identity.
- **IMEI** (*International Mobile Equipment Identity*): a globally unique identifier that
  identifies the physical device, independent of the SIM. It is used for device management
  and fraud detection (e.g., blocking stolen handsets).

**Network identities** are used to identify network elements and geographic areas:

- **MCC** (*Mobile Country Code*) and **MNC** (*Mobile Network Code*): together these
  identify a specific mobile network operator in a specific country. They form the basis of
  the **PLMN** (*Public Land Mobile Network*) identifier.
- **LAI** (*Location Area Identity*): identifies a location area within a network, used for
  paging and idle-mode mobility tracking.
- **CGI** (*Cell Global Identity*): identifies an individual cell globally, composed of the
  MCC, MNC, **LAC** (*Location Area Code*), and **CI** (*Cell Identity*).
- **RSZI** (*Regional Subscription Zone Identity*): identifies a regional zone for
  subscription-based restrictions.
- **BSIC** (*Base Station Identity Code*): identifies a base station at the radio level,
  used by UEs to distinguish between neighboring base stations using the same frequency.

On most smartphones, the IMEI can be read by dialing `*#06#`. More detailed radio
parameters such as the current PLMN, cell ID, signal quality metrics, and deployment type
can be accessed through diagnostic modes available on some devices, allowing direct
observation of the identifiers the network uses in practice.

### Real-World Examples of Mobile Network Identifiers 
When a user turns on a smartphone, the device searches for an available network. Suppose the user is subscribed to an Italian operator with MCC = 222 and MNC = 01. Together, these values form the PLMN identifier (222-01), which uniquely identifies the mobile network operator. To authenticate itself, the SIM card provides its IMSI (International Mobile Subscriber Identity), for example 222010123456789. The network may also read the device IMEI (International Mobile Equipment Identity), such as 356789123456789, to identify the physical handset and verify that it has not been reported as stolen.

After successful authentication, the network assigns a Temporary Mobile Subscriber Identity (TMSI), for example A3F91B2C. From this point onward, the TMSI is used instead of the IMSI over the radio interface. This mechanism improves user privacy because an attacker passively monitoring radio communications cannot easily discover the subscriber's permanent identity.

To receive calls, the subscriber uses a public telephone number called the MSISDN, for example +39 347 1234567. When someone calls this number, the network maps the MSISDN to the subscriber's IMSI and determines the current location of the user.

If the subscriber is roaming abroad, for example in France, the visited network temporarily assigns a Mobile Station Roaming Number (MSRN), such as +33 679 555123. This temporary number allows the home network to route incoming calls to the correct visited network. Once the call has been established, the MSRN is no longer needed and can be released.

Mobility management relies on geographic identifiers. A Location Area Identity (LAI), such as 222-01-4500, identifies a specific location area within the network. As long as the user remains inside the same location area, no location update is required. Individual base stations are identified through the Cell Global Identity (CGI), which combines the MCC, MNC, Location Area Code (LAC), and Cell Identity (CI). For example, the CGI 222-01-4500-12345 uniquely identifies a specific cell in the network.

### Idle mobility: cell selection and location update

When a UE is not engaged in an active call or data session, it is in **idle mode**. In this
state, the UE autonomously selects the most convenient base station by listening to a
**broadcast signalling channel** (also called a beacon channel) transmitted continuously by
all base stations. The UE selects the BS it receives with the highest signal power.

Position tracking in idle mode is not done at the level of individual cells, because
updating the network's database every time a UE moves from one cell to the next would
generate excessive signalling traffic. Instead, tracking is based on **Location Areas**
(*LA*). A location area is a group of cells. The network stores the identity of the
currently visited LA for each idle UE in a central database. When a UE moves within the
same LA, no update is required. Only when the UE crosses an LA boundary does it trigger a
**Location Update** procedure, informing the network of the new LA.

The size of a location area involves a fundamental trade-off:

- **Large location areas** mean UEs cross LA boundaries less frequently, reducing the number
  of location update messages. However, when an incoming call must be delivered, the network
  must page all cells within the LA, and a large LA contains many cells, increasing paging
  cost.
- **Small location areas** make paging cheap because fewer cells must be notified. However,
  UEs cross LA boundaries more often, increasing location update signalling overhead.

![[Pasted image 20260601183501.png]]
The optimal LA size depends on terminal mobility patterns and the frequency of incoming
calls. For highly mobile users or users who receive calls frequently, smaller LAs are more
efficient; for stationary or rarely-called users, larger LAs reduce unnecessary signalling.

### Paging

When a call or data session must be routed to an idle UE, the network first looks up the
currently visited LA in its database. It then initiates the **paging procedure**: all base
stations within that LA broadcast a paging message containing the identifier of the called
UE. When the UE receives and responds to the paging message, the network knows which cell
it is in and can route the call accordingly.
![[Pasted image 20260601183433.png]]

### Active mobility: handover

When a UE has an active call or data session and moves from one cell to another, the network
must transfer the connection to the new cell without interrupting the service. This
procedure is called a **handover**.

Unlike idle-mode cell selection, which is controlled autonomously by the UE, handover is
**network-controlled**: the network monitors signal quality, decides when and to which cell
the UE should switch, adapts routing accordingly, and commands the UE to tune to the new
cell. The detailed steps of a GSM handover are as follows:

1. **Neighbor cell monitoring**: the network continuously monitors the signal strength and
   quality of cells neighboring the UE's current cell. The UE sends these measurements to
   its serving BS approximately every 480 ms.
2. **Threshold-based decision**: the network decides to initiate handover if the signal
   quality in the current cell falls below a defined threshold, or if a neighboring cell's
   signal exceeds a higher threshold by a sufficient margin (the hysteresis value h). The
   time window over which the condition must persist is $\Delta t$, which prevents unnecessary
   handovers caused by momentary signal fluctuations.
3. **Handover request**: the network sends a handover request to the new (target) BTS,
   asking it to reserve resources for the incoming connection.
4. **Channel activation**: the target BTS activates a **Traffic Channel** (*TCH*) for the
   handover and acknowledges the reservation.
5. **Handover command**: the **Base Station Controller** (*BSC*) sends a handover command to
   the UE via the current (old) BTS, specifying the target cell's radio frequency and time
   slot (the ARFCN and TS parameters), carried on the **Fast Associated Control Channel**
   (*FACCH*).
6. **Handover access**: the UE tunes to the new frequency and time slot and transmits
   repeated handover access bursts to the new BTS to establish synchronization.
7. **Link establishment**: the new BTS sends an establishment indication to the BSC. The UE
   transmits a SABM (Set Asynchronous Balanced Mode) frame on the FACCH, and the new BTS
   responds with a UA (Unnumbered Acknowledgment) frame, completing the link-layer
   connection.
8. **Connection redirect**: the BSC redirects the active connection (previously on the TCH
   in the old cell) to the TCH in the new cell.
9. **Resource release**: the old BTS releases the channel resources previously allocated to
   the call, and the BSC acknowledges.
10. **Handover confirmed**: the MSC is notified that the handover is complete.
11. **Re-establishment of core network connections**: if the handover involves a change of
    BSC or **Mobile Switching Center** (*MSC*), new connections are established with the new
    controllers, and the old controllers release their resources and update their records
    with the UE's new location.

![[Pasted image 20260601183218.png]]
