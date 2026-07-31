## GNSS systems overview
A GNSS provides navigation signals from a **constellation of satellites** in orbit, with the goal of achieving near-global or global coverage of the Earth's surface. Several independent systems are currently operational or in development.

- **GPS** (*Global Positioning System*) is owned and operated by the U.S. Government, managed at a national level as a multi-use asset, and operated by the U.S. Air Force. GPS service is a **one-way broadcast**: signals flow from satellites to users, and the system supports an unlimited number of simultaneous users. Access to civilian GPS signals is free of direct user charges. The United States is committed to maintaining at least 24 operational GPS satellites 95% of the time. GPS satellites orbit at approximately 20,186 km altitude. ^2054bc
- **GLONASS** is the Russian counterpart to GPS, with satellites at approximately 19,100 km altitude. ^8a0ef4
- **Galileo** is the European system, developed as an initiative of the European Union (EU) and the European Space Agency (ESA), in collaboration with European industry, funded with European public funds, and operated under civilian control. It offers global coverage with a 30-satellite constellation, is fully operational, and is fully interoperable with GPS. Galileo satellites orbit at approximately 23,925 km altitude. ^55c69f
- **BeiDou** is the Chinese system, with satellites at approximately 21,150 km altitude. ^14402b
- **NAVIC** (India) and **QZSS** (Japan) are **regional systems**, operating at much higher altitudes of approximately 36,000 km and 39,000 km respectively, providing enhanced coverage over specific geographic areas.

All global GNSS constellations operate primarily in **Medium Earth Orbit** (*MEO*), at altitudes between roughly 19,000 and 24,000 km. This orbit is a deliberate design choice: it is high enough to allow each satellite to cover a large portion of the Earth's surface at any given time, and low enough to avoid the extreme signal attenuation associated with geostationary orbits.

## GNSS architecture
Any GNSS is organized around three functional segments: 
- the **space segment**
- the **control segment**
- the **user segment**
![[Pasted image 20260315164037.png]]
### Space segment
The space segment consists of the satellite constellation orbiting the Earth, primarily in Medium Earth Orbit (MEO). The satellites continuously broadcast navigation signals toward the Earth's surface. Each satellite carries highly stable atomic clocks and dedicated signal generation hardware. The orbit altitude is chosen so that each satellite covers a large portion of the Earth at any given time, ensuring that a receiver on the ground can always see several satellites simultaneously, a necessary condition for computing a position.

### Control segment
The control segment is a worldwide network of ground stations responsible for keeping the system running accurately. Monitor stations distributed across the globe continuously receive satellite signals and track any deviations in satellite orbits and clock behavior. This data is sent to a master control station, which processes it and computes corrections. Those corrections are then uploaded to the satellites through dedicated ground antennas, so the satellites can broadcast up-to-date and accurate navigation data to users.
### User segment
The user segment is made up of all the receivers that use the system: from smartphone chipsets to professional surveying equipment. The receiver's job is to pick up signals from multiple satellites, measure how long each signal took to travel from the satellite to the receiver, and use that information to compute its own position, velocity, and time. Because the receiver's internal clock is not perfectly synchronized with the satellite clocks, at least four satellites are needed: three to determine the three spatial coordinates, and one more to solve for the clock offset.