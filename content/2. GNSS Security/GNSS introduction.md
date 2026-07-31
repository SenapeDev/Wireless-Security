## Introduction
**Global Navigation Satellite Systems** (*GNSS*) are a family of satellite-based technologies that allow a receiver anywhere on or near the Earth's surface to determine its position, velocity, and time. The most widely known system is **GPS** (*Global Positioning System*), operated by the United States, but several other independent systems exist and are in active use today.
### Applications
GNSS is a critical infrastructure component in an extraordinarily wide range of applications: transportation and personal mobility, precision agriculture, information and communications technology, emergency services, and many others.

### GNSS insecurity
GNSS is particularly sensitive to attacks at the **physical layer**. Because the system relies on the broadcast of radio signals from satellites, a malicious actor who can replay those signals (even without modifying them) may succeed in deceiving a receiver into computing a wrong position. This class of attack, known as **meaconing**, consists of intercepting GNSS signals and retransmitting them with a time delay. The receiver, unable to distinguish the replayed signal from the original, will calculate an incorrect travel time and therefore an incorrect position. The broadcast nature of GNSS, combined with the extreme weakness of the received signals, makes such attacks feasible with relatively simple equipment.
![[Pasted image 20260315160005.png]]

## The concept of position
A position is only meaningful when it is defined relative to a **reference system** (also called a *reference frame*). Without a shared reference, coordinates have no absolute meaning. In three-dimensional space, a position is described by exactly three numbers, its **coordinates**, with respect to a chosen coordinate system. The most familiar geodetic parameterization uses **latitude**, **longitude**, and **altitude**.
![[Pasted image 20260315160137.png]]
- Latitude measures angular distance north or south of the equator, ranging from $-90°$ (South Pole) to $+90°$ (North Pole). 
- Longitude measures angular distance east or west of the prime meridian (by international convention, the meridian passing through Greenwich, England), ranging from $-180°$ to $+180°$. 
- Altitude provides the vertical dimension, typically expressed as height above a reference ellipsoid.

### Accuracy and precision of position
An important distinction in positioning is between accuracy and precision. 
- **Accuracy** describes how close a measured position is to the true position. 
- **Precision** describes how repeatable a measurement is across multiple observations. 

A system can be precise but inaccurate (consistently offset from the truth), or accurate on average but imprecise (scattered around the true value). In nominal GNSS-only single-point positioning, errors on the order of 10 meters are typical, while more advanced techniques such as Precise Point Positioning (PPP) can reduce this to centimeter-level accuracy.

### Position computation
In mass-market terminals such as smartphones, the position reported to the user is not produced by a single sensor but by a **fusion of multiple sources**. These typically include a satellite navigation chipset (the GNSS receiver proper), inertial measurement units (gyroscopes and accelerometers), electronic compasses, barometers, and information derived from the communication network (e.g., cell tower positions or Wi-Fi fingerprinting).
**Data fusion algorithms** combine all these inputs, and additional techniques are applied to improve the result.

A complete **positioning terminal** can be understood as a pipeline with two main stages: a sensor layer and a localization layer. 
- The *sensor layer* collects raw measurements from all available sources, including GNSS, inertial measurement units (IMUs), odometers, lidar or video, and digital maps. 
- The *localization layer* processes these measurements through fault detection and exclusion, data fusion, and quality indicator computation. 

The outputs of the terminal are not just position coordinates, but a full set of **position quantities**: position, velocity, time, a protection level (a statistical bound on the position error), and an integrity risk measure.