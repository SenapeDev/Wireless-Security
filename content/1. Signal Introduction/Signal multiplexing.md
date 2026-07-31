Efficient use of communication channels is a central problem in wireless systems. In practice, a single physical medium such as a radio frequency band, an optical fibre, or a cable must be shared among many simultaneous users or data streams. Two closely related techniques address this problem: multiplexing and multiple access. Although the terms are sometimes used interchangeably, they refer to distinct aspects of channel sharing.

## Multiplexing and multiple access
### Multiplexing
Multiplexing is the process of combining multiple independent signals into a single composite signal for transmission over a shared medium. At the receiving end, the reverse process, called demultiplexing, separates the composite signal back into its constituent streams. In a multiplexed system, the capacity of the communication channel is partitioned into several logical sub-channels, one for each signal or data stream. The key point is that multiplexing is concerned with combining signals, typically by a single coordinating entity such as a network node or a base station.
![[Pasted image 20260314155526.png]]
### Multiple access
Multiple access, by contrast, refers to mechanisms that allow multiple independent users or devices to share the same communication medium simultaneously without a single entity pre-combining their signals. In a multiple access scenario, each user transmits independently, and the system is designed so that their signals can coexist on the medium and be separated at the receiver. While multiplexing divides the channel capacity at the transmitter, multiple access governs how autonomous users coordinate (or compete) for access to a shared resource.
![[Pasted image 20260314155541.png|543]]
## Different concepts, same mechanism
Despite this conceptual distinction, the underlying technical mechanisms are identical. 
- **Frequency Division Multiple Access** (*FDMA*) uses the same spectral partitioning as **Frequency Division Multiplexing** (*FDM*); 
- **Time Division Multiple Access** (*TDMA*) uses the same time-slot structure as Time **Division Multiplexing** (*TDM*); 
- **Code Division Multiple Access** (*CDMA*) uses the same orthogonal coding scheme as **Code Division Multiplexing** (*CDM*). 
![[Pasted image 20260314162636.png]]
The notation FDM/FDMA, TDM/TDMA, and CDM/CDMA is therefore commonly used to acknowledge that both aspects are embodied in the same technical approach.

### Frequency division multiplexing and multiple access (FDM/FDMA)
In FDM/FDMA, the available bandwidth of the communication channel is divided into a **set of non-overlapping frequency sub-bands**, and each logical channel or user is assigned one of these sub-bands for its exclusive use. Each source signal is modulated onto a distinct carrier frequency, shifting its spectrum into the assigned sub-band. The receiver demultiplexes the composite signal using band-pass filters tuned to each carrier frequency, extracting each sub-channel independently without distortion, provided the sub-bands do not overlap.
![[FDMA.png|502]]
To prevent inter-channel interference caused by spectral leakage and filter imperfections, small unused frequency intervals called **guard bands** are inserted between adjacent sub-channels. The useful bandwidth of the physical medium must therefore exceed the sum of the sub-channel bandwidths by the total guard band overhead. The key design requirement is that the aggregate bandwidth of all sub-channels plus guard bands fits within the available spectrum of the medium.

A notable property of FDM is that each channel occupies its assigned frequency band for the entire duration of the transmission, regardless of whether data is actually being transmitted at any given moment. If a source goes silent, its frequency band remains allocated and is **wasted**. This static allocation policy makes FDM simple to implement and requires no dynamic coordination among users, since each user knows its permanent frequency assignment in advance. The absence of synchronisation requirements also means that FDM works equally well for analogue and digital signals, making it historically the dominant technique in analogue broadcasting.

#### Advantages and disadvantages
The principal advantage of FDM/FDMA is its **simplicity**: no dynamic coordination or synchronisation between senders is required. Because each channel is permanently assigned a fixed portion of the spectrum, frequency planning is done once at design time, and individual channels operate independently. This simplicity also makes FDM inherently compatible with analogue signals, which cannot easily be processed by techniques that require digital timing.

The main disadvantage is the potential for **bandwidth waste**. If the traffic load is unevenly distributed among sub-channels, some channels may carry little or no data while their allocated spectrum goes unused. The guard bands further reduce spectral efficiency. FDM is therefore most efficient when the traffic load is relatively uniform and continuous across all channels.

#### Applications
FDM/FDMA is one of the most widely deployed techniques in communications. It is the basis of AM and FM radio broadcasting, analogue and digital television, traditional telephone networks over coaxial and twisted-pair cables, communication satellites (where uplink and downlink frequency bands are separated and individual transponders occupy fixed frequency slots), and digital subscriber line (DSL) technology. Virtually all wireless communication systems use some form of frequency division, at least at the level of separating different services or bands.

### Time division multiplexing and multiple access (TDM/TDMA)
In TDM/TDMA, the shared channel is **divided in the time** dimension rather than the frequency dimension. The channel is used exclusively by one sender at a time, but different senders take turns in a predetermined, cyclic sequence of time slots. Each logical channel is assigned one or more slots in a repeating frame structure. Within its assigned slot, a sender has access to the full channel bandwidth, and its data is transmitted as a burst. The aggregate data rate of the medium must exceed the data rate of any individual source, since each source only occupies the channel for a fraction of the total time.
![[TDMA.png|465]]
Because all senders share the same frequency band but are separated in time, only a single carrier is present on the medium at any given instant. This eliminates inter-channel interference in the frequency domain, at the cost of requiring **precise timing synchronisation**: all senders must agree on the slot boundaries and frame structure.

#### Synchronous TDM
In synchronous TDM, time slots are **preassigned** to sources and the assignment is fixed regardless of whether a given source has data to send. Each source is assigned its slot in every frame, and the slot is transmitted even if it carries no useful data. Like FDM, synchronous TDM therefore has the drawback that capacity is allocated even when it is not needed, leading to inefficiency when some sources are idle or bursty.

The **advantage** of synchronous TDM is that the slot assignment scheme is fully predictable and requires no additional per-slot signalling or scheduling overhead. Demultiplexing is straightforward: the receiver simply extracts the appropriate slot from each frame based on its known position.

#### Statistical TDM
Statistical TDM (also called *asynchronous TDM* or *packet multiplexing* in some contexts) addresses the inefficiency of synchronous TDM by allocating time slots dynamically based **on demand**. Instead of maintaining fixed slot assignments, the multiplexer scans the input lines and assigns slots only to those sources that have data ready to transmit. When a source goes idle, its slots are reallocated to active sources.

The benefit is a much **higher effective throughput**, since bandwidth is not wasted on silent sources. The trade-off is that the system becomes more complex: because slot assignments are no longer fixed and predictable, each slot must carry an identifier indicating which source it belongs to, adding overhead. Furthermore, the multiplexer must implement scheduling algorithms to decide which sources get slots in each frame, and the data rate on the line may be lower than the aggregate peak rate of all input lines, so buffers are needed to absorb bursts. Statistical TDM is the conceptual foundation of modern packet-switched networks, where bandwidth is shared dynamically among active flows.

#### Advantages, disadvantages, and applications
The main advantage of TDM/TDMA is high throughput: with only one carrier present at a time, there is no inter-channel interference, and with synchronous TDM the system is straightforward to engineer. Statistical TDM additionally avoids capacity waste on idle channels. The main disadvantage is the requirement for precise synchronisation, which adds complexity compared to FDM. TDM/TDMA is used in synchronous optical networking (SONET), the GSM mobile telephony standard (in combination with FDM), and the Integrated Services Digital Network (ISDN), among others.

### Code division multiplexing and multiple access (CDM/CDMA)
CDM/CDMA takes a fundamentally different approach. Rather than separating channels in frequency or time, all channels use the full bandwidth of the medium simultaneously and continuously. Separation is achieved by assigning each channel a unique binary spreading code $c_i(t)$, and by exploiting the mathematical property of orthogonality between these codes.
![[CDMA.png|461]]
#### Spreading codes and orthogonality
Each sender is assigned a unique binary code sequence $c_i(t)$, which is used to modulate (spread) the data signal before transmission. The code sequences are chosen to be mutually orthogonal vectors in the sense that the inner product (scalar product) of any two distinct codes over a code period is zero:

$$\langle c_i(t),\, c_j(t) \rangle = 0 \quad \text{for } i \neq j$$

This orthogonality property is what allows the signals of different users to coexist in the same frequency band at the same time without irreversible interference. It is implemented using spread spectrum technology, where the bandwidth occupied by the transmitted signal is made much larger than the bandwidth of the original data signal. The ratio of the spread bandwidth to the data bandwidth is the processing gain, and it determines how much interference rejection the system provides.

#### Multiplexing and demultiplexing operations
To form the multiplexed signal, each sender multiplies its data signal $s_i(t)$ by its spreading code $c_i(t)$ before transmission. The composite transmitted signal is the sum of all such spread signals:

$$s_{\text{mux}}(t) = s_1(t)\,c_1(t) + s_2(t)\,c_2(t) + \cdots$$

At the receiver, demultiplexing is performed by computing the inner product of the received composite signal with the desired spreading code over one code period. Because the codes are orthogonal, this operation extracts only the contribution of the desired channel and cancels all others:

$$\langle s_{\text{mux}}(t),\, c_1(t) \rangle = s_1(t)$$

The physical intuition is that the inner product operation acts as a matched filter that is sensitive only to signals spread with the code $c_1(t)$, treating all other signals as noise-like interference that averages to zero over the code period.

#### Advantages, disadvantages, and applications
CDMA offers several important advantages. It is bandwidth efficient in the sense that all users share the full spectrum, and the system can accommodate more users by adding more orthogonal codes without requiring additional spectrum allocation. No explicit coordination of access timing or frequency is needed between users; each user simply applies its code continuously. The spreading process also provides inherent robustness against narrowband interference: a narrowband interferer affects only a small portion of the spread spectrum, and after despreading its energy is spread over the wide bandwidth and effectively attenuated relative to the desired signal.

The disadvantages are a lower per-user data rate compared to wideband schemes (since the available bandwidth is shared across many simultaneous users via spreading) and greater complexity in signal regeneration and synchronisation at the receiver. CDMA is applied in the UMTS 3G mobile standard and in **Global Navigation Satellite Systems** (*GNSS*) such as GPS, where multiple satellites simultaneously transmit on the same frequency bands and receivers use the orthogonal satellite codes to distinguish and track each satellite's signal.

## Combined TDM/A and FDM/A
In practice, real communication systems often combine more than one multiplexing dimension to obtain better performance than any single technique alone. A common combination is TDM with FDM, where the available spectrum is divided into frequency sub-bands (as in FDM) and within each sub-band, time is further divided into slots (as in TDM). Each channel is therefore assigned a specific frequency band for a specific duration, after which it may move to a different frequency band in the next time interval.
![[FDMA-with-TDMA.png]]
GSM is a classic example: the available spectrum is divided into 200 kHz carriers (FDM), and each carrier is further divided into eight time slots per frame (TDM), so that each call occupies one time slot on one carrier. This combination offers several advantages over either technique alone. Assigning different frequency-time blocks to different users provides better protection against tapping, since an eavesdropper must know both the frequency and the timing pattern to intercept a channel. The time-varying frequency allocation also provides protection against frequency-selective fading: if one frequency sub-band is temporarily degraded by interference or fading, the affected users move to a different sub-band in the next frame. Combined TDM/FDM also achieves higher data rates than CDMA for the same bandwidth, since there is no spreading overhead. The principal requirement is precise coordination: all users must be synchronised in both time and frequency, which demands accurate clocking and tight frequency planning.