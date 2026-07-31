### GSM radio interface and multiple access scheme

The GSM radio interface uses a combination of **FDM** (*Frequency Division Multiplexing*) and **TDM** (*Time Division Multiplexing*) to allow multiple users to share the available radio spectrum simultaneously.

- In **FDM**, the total available frequency band is divided into multiple narrow sub-bands, each 200 kHz wide in GSM. Each sub-band can carry one physical channel. Different users or logical channels are assigned different frequency sub-bands and use only their allocated portion of the spectrum continuously over time.
- In **TDM**, a single frequency channel is divided into repeating time slots. Each user transmits only during their assigned time slot and is silent during the others. The full spectrum is available to the transmitting user within their slot, but only for that brief window.

GSM combines both approaches: the spectrum is first divided into 200 kHz sub-bands (FDM), and each sub-band is further divided into time slots (TDM). This combined scheme is referred to as **TDMA/FDMA** (*Time Division Multiple Access / Frequency Division Multiple Access*).

The uplink and downlink directions use **FDD** (*Frequency Division Duplexing*): they operate on separate frequency bands with a 45 MHz separation between uplink and downlink. In the 900 MHz band, the uplink occupies 880–915 MHz and the downlink occupies 925–960 MHz.
![[Pasted image 20260603103944.png]]
Each TDMA frame consists of **8 time slots** and has a total duration of **4.615 ms**, making each individual time slot **577 µs** long. To avoid interference between the uplink and downlink transmissions on the same physical device, a **3-slot offset** is applied: when the BTS transmits on slot N in the downlink, the mobile station transmits on slot N in the uplink 3 slots later. This offset gives the UE time to switch between receive and transmit modes.

![[Pasted image 20260603104221.png]]



#### Modulation and channel coding

GSM uses **GMSK** (*Gaussian Minimum Shift Keying*) as its modulation scheme. GMSK is a form of continuous-phase frequency-shift keying where the phase transitions between symbols are smoothed by a Gaussian filter. This reduces the spectral bandwidth of the transmitted signal and limits interference into adjacent channels, at the cost of some inter-symbol interference. For error correction, GSM applies **convolutional coding** as a forward error correction mechanism, with several different code rates depending on the type of traffic being carried.

At the receiver, **equalization** is used to counteract the distortion introduced by the multipath radio channel. Known bit sequences, called training sequences, are embedded in each physical burst. The receiver uses these sequences to estimate the channel response and synthesise a filter that compensates for the channel distortion.

For voice, GSM supports multiple codecs: the original **RPE** (*Regular Pulse Excitation*) codec operating at 13 kb/s, and the later **CELP** (*Code Excited Linear Prediction*) codec operating at 12.2 kb/s with improved voice quality.

#### Physical layer management

**Frequency hopping** is a mechanism whereby the carrier frequency used by a connection changes from slot to slot according to a defined hopping sequence. This reduces the impact of frequency-selective fading: if a particular carrier frequency is subject to deep fading at a given location, the connection is only affected during the slots transmitted on that frequency before hopping to another.

**Power control** is implemented in both directions. The BTS controls the transmission power of the mobile station, and the mobile station controls the BTS power (for traffic channels only). The mechanism uses a closed-loop scheme in which each side sends power adjustment commands (up or down) to the other based on measured signal quality.

**Synchronisation** is managed at multiple levels:
- Carrier synchronisation is achieved through a broadcast channel.
- Slot synchronisation uses a **timing advance** mechanism: the BTS measures the propagation delay of the UE's transmissions and instructs it to transmit slightly earlier, so that its bursts arrive at the BTS at the correct time within the slot.
- Frame synchronisation tracks the frame numbering.
- Base station synchronisation across different BTSs is optional.

### CDMA: the UMTS radio access scheme

While GSM separates users by assigning them different time slots and frequency sub-bands, UMTS uses a fundamentally different approach called **CDMA** (*Code Division Multiple Access*). In CDMA, all users transmit simultaneously over the same frequency band. User separation is achieved through **spreading codes**: each user's data signal is multiplied by a unique high-rate pseudo-random code before transmission. This spreading process expands the signal across a much wider bandwidth than the original data would occupy, hence the term **spread spectrum**.

At the receiver, the desired signal is recovered by multiplying the received composite signal by the same spreading code used by the transmitter, a process called **despreading**. Because the spreading codes are chosen to have low cross-correlation with one another (ideally zero for orthogonal codes), despreading with the correct code reconstructs the intended signal, while the signals from all other users appear as low-level noise and are effectively filtered out.

A useful analogy: imagine a room in which many people are speaking simultaneously, each in a different language. A listener who knows one of those languages can understand the corresponding speaker, while the other conversations blend into background noise. In CDMA, the spreading code plays the role of the language.

An important distinction from TDM and FDM is that **TDM and FDM require centralised and static allocation** of time slots or frequency bands to users. CDMA codes are also statically assigned, but **access is random**: a user can transmit at any time without waiting for a scheduled slot, and when there is no data to send, the transmitter simply remains silent without holding any resource that would be wasted.

![[Pasted image 20260603105651.png]]
#### CDMA efficiency for data services

For **voice services**, a call between two parties requires two channels (one in each direction), but at any given moment only one party is typically speaking. This means the effective utilisation of each channel is at most approximately 0.5. Accounting for silence periods during speech, the utilisation is even lower. In a TDM or FDM system, the circuit is allocated for the full duration of the call regardless, so the resources consumed during silence are wasted.

For **data services**, the inefficiency is more severe. Data traffic is typically highly bursty: a user downloads a web page at a high data rate for a short time, then is idle for an extended period. The ratio of active transmission time to total session time can be well below 0.1. A TDM or FDM system that allocates a dedicated circuit for a data session wastes the allocated resources during the long idle periods, resulting in an efficiency that is at best around 0.5 for a two-direction circuit.

CDMA improves this significantly. Because a CDMA transmitter simply does not transmit when it has no data to send, it produces no interference with other users during idle periods. The shared medium is not occupied, and no resource is wasted. This gives CDMA an efficiency close to 1 even for bursty data traffic, making it considerably better suited than TDM/FDM for the data-intensive usage patterns that characterise modern mobile services.