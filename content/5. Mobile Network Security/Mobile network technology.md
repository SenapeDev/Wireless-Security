## Overview and historical context
Mobile networks allow radio user terminals to connect to global network infrastructure and
services, primarily telephone and internet services. These terminals are referred to as
**User Equipment** (*UE*) or **Mobile Stations** (*MS*), depending on the generation of
technology involved.

The first step toward mobile telephony came in 1960, when Sweden introduced the world's
first automated mobile telephone system, called **Mobile Telephone system A** (*MTA*). The
system allowed automatic connection from a handset mounted in a car, with calls still
forwarded by a human operator. The first truly successful commercial mobile network followed
later, designed specifically for car-mounted terminals and reaching over 35,000 subscribers
by 1986.

From those early systems, mobile networks have evolved through successive generations, each
expanding both the services offered and the data rates available:

- **1G** (around 1980): analog voice calls only, at speeds around 2.4 Kbps.
- **2G** (around 1990): digital voice and text messaging, at speeds up to 64 Kbps.
- **3G** (around 2000): internet access added, at speeds up to 2 Mbps.
- **4G** (around 2010): broadband internet and internet-based applications, at speeds of
  100–1000 Mbps.
- **5G** (around 2020): support for the **Internet of Things** (*IoT*) and service-based
  architecture, at speeds of 1–10 Gbps.
- **6G** (expected around 2030): a fully digital and connected world, targeting speeds of
  around 1 Tbps.

### Why mobile networks are complex
Mobile networks are not complex simply because they involve many protocols. The real reason
is that they must solve several fundamentally hard problems simultaneously, under severe
constraints.

- **Mobility** is the first and most distinctive challenge. Unlike wired networks, the endpoint moves continuously. The network must track the user's location, reroute traffic during movement, maintain active sessions across cell transitions, and support roaming across operators and countries. This alone generates enormous signalling complexity.

- **The wireless medium** is inherently exposed. Radio transmissions are broadcast, interceptable, jammable, and spoofable. As a result, the network must continuously manage authentication, encryption, interference, spectrum sharing, and power control. The radio interface is fundamentally hostile from a security standpoint.

- **Scale** is another source of complexity. Mobile networks operate at national and global scale, serving millions of subscribers with millions of simultaneous sessions, supported by thousands of base stations and billions of signalling events per day. Every function must scale accordingly: authentication, paging, mobility management, billing, lawful interception, and key management.

- **Real-time constraints** add further pressure. The network must react extremely quickly: handovers must complete in tens of milliseconds, voice latency must remain below 150 ms, paging must succeed before call timeout, and radio scheduling in 4G/5G operates on millisecond intervals. This creates a constant trade-off between security and latency.

- **Heterogeneity and backward compatibility** mean that modern networks must often support 2G, 3G, 4G, 5G, and IoT variants simultaneously. Legacy protocols survive for decades, and old trust assumptions remain embedded in the infrastructure.

- Finally, **roaming and distributed trust** require that a mobile user's device functions globally, which in turn requires trust relationships among operators worldwide. One operator must trust signalling and data received from another, a requirement that introduces significant security challenges.

## Network architecture

A mobile network is divided into two main functional parts: the **Radio Access Network**
(*RAN*) and the **Core Network** (*CN*).
![[Pasted image 20260601170621.png|589]]
The RAN handles radio connectivity with user terminals. The CN interconnects the RAN to
external services and infrastructures, and provides connectivity and mobility management
functions.

In 2G and 3G networks, the core network is split into two separate subsystems: a
**circuit-switched** (*CS*) core network that provides access to telephone services, and a
**packet-switched** (*PS*) core network that provides internet access. In 4G and 5G, a
single packet-switched core network provides both voice and data services, eliminating the
need for a dedicated circuit-switched domain.
![[Pasted image 20260601171428.png|453]]
### Base stations

The main architectural elements of the RAN are **Base Transceiver Stations** (*BTS*, also
called *BS*), which connect to UEs through a radio interface. A BTS is composed of three
physical components:

- The **antenna**, which transmits and receives radio signals.
- The **Remote Radio Unit** (*RRU*), which handles radio frequency processing.
- The **Baseband Unit** (*BBU*), which performs digital signal processing and connects the
  station to the rest of the network.

In 4G and 5G, base stations connect directly to core network elements. In 2G and 3G, an
additional **radio controller** element is placed between the base stations and the core
network to coordinate radio resource management across multiple BSs.

![[Pasted image 20260601171639.png|544]]
### The cellular concept

Base stations are deployed across a service area so that UEs in any position can connect to
the network. Each UE connects to the most convenient BS, which is typically the nearest one
or the one providing the strongest signal. The geographic area in which UEs connect to a
specific BS is called a **cell**, and this organization of coverage areas gives mobile
networks their name: cellular networks.

For analytical and planning purposes, cells are traditionally depicted as **hexagons**,
because hexagons tile a plane without gaps and approximate the roughly circular coverage of
an isotropic antenna. In reality, signal propagation is non-uniform and affected by
obstacles such as buildings and terrain, so actual cell shapes are irregular. The idealized
hexagonal model is nonetheless a useful tool for dimensioning systems and reasoning about
the principles of frequency reuse.

### Frequency reuse and the cluster model

Radio spectrum is a limited resource. The same radio frequencies cannot be reserved
exclusively for a single cell across an entire network; they must be reused in different
cells to serve more users. However, reusing the same frequency in nearby cells causes
**co-channel interference**, because a UE in one cell may receive a signal from a distant
BS using the same frequency. Managing this interference is a critical design problem, with a
fundamental trade-off between channel quality and network capacity.
![[Pasted image 20260601172301.png]]
To address this, mobile networks use a **cluster model**. The service area is divided into
groups of K cells, each group called a **cluster**. Within each cluster, every cell is
assigned a distinct set of frequencies. The cluster pattern is then repeated regularly
across the entire service area, so that cells using the same frequencies are separated by
the distance of at least one full cluster. This separation limits interference to an
acceptable level, quantified by the **Signal-to-Interference Ratio** (*SIR*).

Network planning requires solving two related problems:

- **Coverage planning**: where to place antennas to cover a given area.
- **Capacity planning**: which radio resources to assign to each cell.

The amount of frequency resources assigned to each cell directly determines system
capacity. A smaller cluster size K means each cell gets a larger share of the spectrum and
can carry more traffic, but cells using the same frequency are closer together and
interference is higher. A larger K reduces interference but reduces per-cell capacity. The
**reuse efficiency** is expressed as 1/K.
![[Pasted image 20260601172503.png]]
Not all values of K are geometrically admissible for a regular hexagonal grid. Only values
of the form $K = i^{2} + i\cdot j + j^{2}$ for non-negative integers i and j are valid, giving the
sequence K = 1, 3, 4, 7, 9, 12, 13, and so on. In practice, the frequency assignment
problem is equivalent to a **graph coloring problem**, which is known to be NP-complete,
meaning that finding optimal assignments for realistic network topologies requires heuristic
or approximate methods.

### Cellular layout and cell types
To increase capacity in areas with high user density, networks deploy cells of different
sizes. Smaller cells serve more users per unit area by reducing the number of terminals each
base station must handle. The main cell types, from largest to smallest, are:
![[Pasted image 20260601173710.png|487]]
- **Macro cells**: outdoor coverage, transmit power above 10 W, coverage radius on the
  order of kilometers.
- **Micro cells**: outdoor coverage, transmit power of 5–10 W, coverage radius of hundreds
  of meters.
- **Pico cells**: indoor and outdoor, transmit power of 100–250 mW indoors and 1–5 W
  outdoors, coverage radius of tens of meters.
- **Femto cells**: mainly indoor, transmit power of 10–100 mW indoors and 0.2–1 W outdoors,
  coverage radius of tens of meters.

The goal of mixing cell sizes is to regulate the density of terminals that each cell must
handle, concentrating smaller cells in high-traffic areas.

Deploying more and smaller cells brings important disadvantages that must be managed:

- **More handovers**: devices change cells more frequently, increasing signalling overhead
  and the risk of handover failures.
- **Higher co-channel interference**: cells using the same frequency are physically closer,
  requiring more sophisticated radio resource management.
- **Increased infrastructure cost**: more base stations, backhaul links, power supplies, and
  maintenance are required.
- **Greater network complexity**: mobility management, scheduling, synchronization, and
  resource allocation all become harder.
- **Higher signalling load**: more location updates, paging operations, and control-plane
  messages are generated.
- **Increased security exposure**: more network elements and more signalling exchanges
  enlarge the attack surface.

### Radio resource sharing

A key distinction between the RAN and fixed-line access networks (such as copper telephone
networks or fiber-optic point-to-point networks) is that radio resources in the RAN are
**shared** among all users of the same cell and among users of different cells reusing the
same frequencies. In most fixed-line networks, each subscriber has a dedicated physical
link. In a cellular network, all UEs within a cell contend for the same pool of radio
resources, and the base station must schedule transmissions to coordinate access. This
shared medium is one of the fundamental sources of complexity and security exposure in
mobile networks.
![[Pasted image 20260601174931.png]]
