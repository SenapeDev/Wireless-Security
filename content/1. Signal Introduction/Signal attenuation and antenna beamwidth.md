Wireless communication relies on electromagnetic waves propagating through free space. During this propagation, the signal energy spreads over an ever-increasing area, causing the received power to fall with distance.

## Signal attenuation and the link equation
When a transmitter radiates a signal with power $P_T$ into a communication channel, the signal undergoes an attenuation loss characterized by the factor $L$. The received power $P_R$ is accordingly:

$$P_R = \frac{P_T}{L}$$

![[Pasted image 20260314153655.png]]
In free space, where no obstructions or reflections are present, the attenuation arises from the geometric spreading of the wavefront. This is called free-space path loss, and its value depends on the distance $d$ between transmitter and receiver and on the wavelength $\lambda$ of the signal:

$$L = \left(\frac{4\pi d}{\lambda}\right)^2$$

This formula shows that attenuation grows as the square of the distance and inversely as the square of the wavelength. Equivalently, higher-frequency signals (shorter wavelengths) suffer greater free-space loss at the same distance. This is one reason that lower-frequency bands are preferred for long-range communications, while higher frequencies are used in short-range or line-of-sight links where the resulting attenuation can be compensated.

The quality of the received signal is characterised by the signal-to-noise ratio at the receiver. A common formulation expresses this as the ratio $E_b/N_0$, where $E_b$ is the energy per bit received and $N_0$ is the one-sided noise power spectral density. The energy per bit is related to the received power $P_R$ and the bit rate $R_b$ by:

$$E_b = \frac{P_R}{R_b}$$

A lower received power $P_R$ therefore means lower $E_b$ and, for the same noise level, a lower SNR. Since the bit error rate increases steeply as SNR decreases, ensuring adequate received power is a primary concern in link design.

## Using antennas to compensate for attenuation
Antennas provide a practical means to increase received power without raising transmit power. A receiving antenna captures electromagnetic energy from the passing wavefront and concentrates it into the receiver. The key figure of merit is the antenna gain $G$, which measures how effectively an antenna focuses energy in a given direction relative to an isotropic radiator (one that radiates equally in all directions).

When both the transmitting and receiving antennas are directional, with gains $G_T$ and $G_R$ respectively, the received power becomes:

$$P_R = \frac{P_T \cdot G_T \cdot G_R}{L}$$

This expression, commonly known as the Friis transmission equation (in simplified form), shows that antenna gain directly multiplies the received power. Doubling either antenna's gain doubles the received power, which is equivalent to halving the free-space path loss in its effect on the link budget.

The physical interpretation is straightforward for the receiving antenna: a larger, more directive antenna intercepts a greater fraction of the incident wavefront, capturing more energy per unit time. For the transmitting antenna, a higher gain concentrates the radiated power into a narrower beam aimed at the receiver, increasing the power density in that direction at the expense of other directions.

### Antenna beamwidth and directivity
The directivity of an antenna is quantified by its beamwidth, conventionally denoted $\theta_B$. The beamwidth is defined as the angular width of the main radiation lobe, typically measured between the half-power points (the $-3$ dB points) of the radiation pattern. A narrow beamwidth corresponds to a highly directive antenna that concentrates power along a small solid angle; a wide beamwidth corresponds to a more omnidirectional pattern.

For a parabolic reflector antenna, the beamwidth is related to the antenna diameter $D$ and the signal wavelength $\lambda$ by the approximate formula:

$$\theta_B \approx \frac{70\lambda}{D}$$

where $\theta_B$ is expressed in degrees. This relationship captures the wave-optics principle that a larger aperture produces a narrower beam, in the same way that a larger lens focuses light more tightly. A parabolic dish with diameter $D = 1\ \text{m}$ operating at a wavelength of $0.01\ \text{m}$ (30 GHz) would have an approximate beamwidth of $0.7°$, whereas the same dish at a wavelength of $0.1\ \text{m}$ (3 GHz) would produce a beamwidth of $7°$.

#### The relationship between beamwidth and gain
Antenna gain and beamwidth are inversely related: the more concentrated the beam, the higher the gain. Quantitatively, the gain $G_T$ of a lossless antenna is approximately proportional to the reciprocal of the square of the beamwidth:

$$G_T \propto \frac{1}{\theta_B^2}$$

Substituting the parabolic antenna approximation $\theta_B \approx 70\lambda/D$, this gives:

$$G_T \propto \frac{D^2}{\lambda^2}$$

This result has an important practical implication: doubling the diameter $D$ of a parabolic antenna increases the gain by a factor of four (6 dB), because gain scales as the square of the diameter. Conversely, increasing the operating frequency (reducing $\lambda$) also increases gain for the same physical aperture, which is one motivation for using millimetre-wave frequencies in high-capacity links such as satellite communications and 5G backhaul.

Free-space path loss also scales as $1/\lambda^2$, meaning that higher frequencies suffer both greater path loss and greater antenna gain for a fixed aperture. In system design these two effects partially cancel, and the net outcome depends on whether the aperture or the transmit power is the binding constraint.