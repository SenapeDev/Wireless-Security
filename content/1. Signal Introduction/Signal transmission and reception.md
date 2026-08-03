## Why we need modulation
When we want to send digital information from one place to another, we face a fundamental mismatch: computers work with discrete binary values (0s and 1s), but the physical world transmits continuous analog signals. A radio channel, a cable, or an optical fiber cannot carry a sequence of abstract 0s and 1s directly. What they carry are physical waveforms: signals that vary continuously in time.

**Modulation** takes digital information and encodes it into the properties of an analog wave, which can then actually travel through a physical medium. At the other end, demodulation reverses the process: it takes the received analog wave and extracts back the digital information.
![[signal-modulation.png]]
A complete communication system can be divided into three main sections. 
- The **user section** is where the digital data originates and where it is ultimately decoded. 
- The **interface section** contains the encoder (which adds structure and redundancy to the bits) and the modulator (which converts those bits into an analog waveform). 
- The **channel section** is the physical medium through which the analog signal travels. 

On the receiving side, the *demodulator* converts the received analog signal back into a sequence of digital samples, and the *decoder* reconstructs the original bits.

The modulator and demodulator together are often called a **modem** (modulator-demodulator). Understanding what happens inside them is the core of this chapter.


## The three basic properties of a wave
Any periodic wave can be described by three properties:
- its **amplitude** (how tall the wave is)
- its **frequency** (how fast it oscillates)
- its **phase** (where in its cycle the wave starts)

Modulation works by varying one of these three properties in response to the information signal. This gives rise to three fundamental types of modulation.
![[Pasted image 20260306111017.png]]
### Amplitude modulation (AM)
In amplitude modulation, the frequency and phase of the carrier wave are kept constant, while the amplitude is made to vary according to the message signal $m(t)$. When the message signal has a large value, the carrier wave becomes taller; when the message signal is small, the carrier wave shrinks. The shape of the carrier's "envelope" mirrors the shape of the message.

### Frequency modulation (FM)
In frequency modulation, the amplitude of the carrier stays constant throughout, while the frequency changes in proportion to the message signal $m(t)$. When $m(t)$ is large, the carrier oscillates faster; when $m(t)$ is small, it oscillates more slowly. With no message at all, the carrier sits at its natural resting frequency. FM is widely known from radio broadcasting and is more robust to noise than AM, because noise tends to corrupt amplitude rather than frequency.

### Phase modulation (PM)
In phase modulation, both the amplitude and frequency of the carrier remain fixed, but the phase shifts in response to the message signal $m(t)$. Phase is essentially the "starting point" of the wave's oscillation cycle. When the message changes, the wave appears to jump forward or backward in its cycle. Phase modulation is closely related to frequency modulation mathematically, and both are widely used in digital communications.

## From analog to digital modulations
Even though the information we want to transmit is digital (a sequence of bits), the transmitted signal is always analog. The key insight is that the same three ideas (varying amplitude, frequency, or phase) can be applied to digital signals. Instead of varying continuously, though, the carrier property switches between a finite set of discrete values, one for each possible bit pattern. This gives rise to three families of digital modulation:

- **Amplitude Shift Keying** (*ASK*): the amplitude switches between discrete levels.
- **Frequency Shift Keying** (*FSK*): the frequency switches between discrete values.
- **Phase Shift Keying** (*PSK*): the phase switches between discrete values.

These are the digital equivalents of AM, FM, and PM respectively.
![[Pasted image 20260306111336.png]]
Another important distinction is between baseband and bandpass signals. 
- A **baseband** signal is one whose frequency content is concentrated around zero frequency, so it has not yet been shifted to any particular part of the radio spectrum. 
- A **bandpass** signal is one whose frequency content is centered around some carrier frequency $f_c$, away from zero. 

In wireless communications, signals must be transmitted as bandpass signals, because different systems share the spectrum by using different carrier frequencies.
Baseband signals are converted to bandpass signals through modulation: by multiplying the baseband signal $x(t)$ by a sinusoid at the carrier frequency, the spectrum shifts from being centered at zero to being centered at $f_c$:

$$y(t) = x(t)\cos(2\pi f_c t)$$

In the frequency domain, this multiplication shifts the entire spectrum of $x(t)$ up to be centered around $\pm f_c$.


## Pulse Amplitude Modulation (PAM)
The simplest way to encode bits into a baseband analog signal is called **Pulse Amplitude Modulation**, or PAM. The idea is straightforward: we define a basic pulse shape $g(t)$, which is a waveform that lasts for a duration $T$ (called the symbol duration). To transmit a bit, we send either $+g(t)$ or $-g(t)$ depending on whether the bit is a 1 or a 0.

More precisely, in binary PAM (or 2-PAM):
$$s(t) = g(t) \quad \Rightarrow \quad \text{"1"}$$
$$s(t) = -g(t) \quad \Rightarrow \quad \text{"0"}$$

The simplest choice for $g(t)$ is a rectangular pulse: it has a constant amplitude $A$ for the entire duration $T$, and is zero everywhere else. Visually, you can think of the set of possible transmitted signals as two points on a line, at $+1$ and $-1$, where the coordinate axis is labeled $g(t)$.
![[Pasted image 20260306113114.png|420]]
This representation, where possible signals are shown as points in a coordinate system whose axes are basis waveforms, is called a **signal constellation** or a signal space diagram. For 2-PAM, the constellation is just two points on a line.

### M-ary PAM: more bits per symbol
Binary PAM transmits exactly one bit per transmission. We can do better by using more than two amplitude levels. In **M-ary PAM**, we use $M$ distinct amplitude levels $A_1, A_2, \ldots, A_M$, and each transmitted pulse represents $\log_2 M$ bits.

For example, with $M = 4$ (called 4-PAM), we use four amplitude levels, say $A_1 = -3$, $A_2 = -1$, $A_3 = +1$, $A_4 = +3$. Each level corresponds to a 2-bit pattern:

$$s_1(t) = -3,g(t) \leftrightarrow \text{"00"}$$ $$\quad s_2(t) = -g(t) \leftrightarrow \text{"01"}$$ $$\quad s_3(t) = +g(t) \leftrightarrow \text{"10"}$$ $$\quad s_4(t) = +3,g(t) \leftrightarrow \text{"11"}$$
![[4PAM-constellation.png]]
The constellation now has four points on a line, equally spaced. Each transmission carries twice as many bits as 2-PAM, at the cost of having symbols that are closer together and therefore easier to confuse when noise is present.

## Signal detection
When a signal travels through a channel, it gets corrupted by noise. The received signal is not exactly what was sent. The receiver's job is to look at the received signal and decide which of the $M$ possible symbols was most likely transmitted. This decision is made by comparing the received value to thresholds placed midway between adjacent constellation points. The result of landing in the wrong region is a **symbol error**, which typically translates into one or more **bit errors**.
### Gray coding
When noise pushes a received symbol just past the threshold, the most likely mistake is to decode the adjacent symbol. If adjacent symbols differ in two or more bits, a single symbol error causes multiple bit errors. To minimize the average number of bit errors, we should assign bit patterns to symbols in such a way that adjacent symbols differ in **only one bit**.

This strategy is called **Gray coding**. Consider 4-PAM with levels at $-3, -1, +1, +3$. A natural assignment might be "00, 01, 10, 11". But notice that the symbols at $-1$ and $+1$ are adjacent, yet "01" and "10" differ in two bits. If the receiver confuses these two adjacent symbols, it makes two bit errors at once.
![[Pasted image 20260307114050.png]]
With Gray coding, the assignment is instead "00, 01, 11, 10". Now every pair of adjacent symbols differs in exactly one bit. A single symbol error caused by noise almost always results in just one bit error, which is the best we can do.

## Energy per symbol and energy per bit
Transmitting a signal costs energy. The energy of a symbol $s_m(t) = A_m \cdot g(t)$ over the duration $T$ is:

$$E_m = \int_0^T \left(s_m(t)\right)^2 dt = A_m^2 \int_0^T \left(g(t)\right)^2 dt = A_m^2 \cdot E_g$$

where $E_g$ is the energy of the basic pulse $g(t)$. Notice that the energy grows with the square of the amplitude: doubling the amplitude level quadruples the energy.

The **average energy per symbol** $E_s$ is just the average of $E_m$ over all $M$ symbols:

$$E_s = \frac{1}{M} \sum_{m=1}^{M} E_m$$

For 4-PAM with levels $-3, -1, +1, +3$:

$$E_s = \frac{(-3)^2 + (-1)^2 + 1^2 + 3^2}{4} \cdot E_g = \frac{9+1+1+9}{4} \cdot E_g = 5 E_g$$

Since each symbol carries $\log_2 M$ bits, the **average energy per bit** is:

$$E_b = \frac{E_s}{\log_2 M}$$

This is a key figure of merit: it measures how much energy is needed per unit of information. The ability to transmit reliably at low $E_b$ is called **energy efficiency**.

An important geometric observation: in the signal constellation, the distance from a symbol to the origin is proportional to $\sqrt{E_m}$, so symbols farther from the origin cost more energy to transmit.


## Bandwidth occupancy and bandwidth efficiency
Every signal occupies some range of frequencies, called its **bandwidth**. A rectangular pulse of duration $T$ has a Fourier transform:

$$G(f) = AT \cdot \text{sinc}(\pi f T) \cdot e^{-j\pi f T}$$

The sinc function decays but never reaches zero, which means a rectangular pulse technically has infinite bandwidth. In practice, most of the energy is contained within the first few lobes, roughly within $\pm 1/T$ of zero frequency.
![[Pasted image 20260307121937.png]]
This highlights a key relationship: **shorter pulses occupy more bandwidth**. A pulse of duration $T$ has a bandwidth of roughly $B = 1/T$, which means the two-sided bandwidth is $BW = 2/T$.

The **symbol rate** (also called the baud rate) is:

$$R_s = \frac{1}{T}$$

It measures how many symbols are transmitted per second. Since each symbol carries $\log_2 M$ bits, the **bit rate** is:

$$R_b = \log_2(M) \cdot R_s = \frac{\log_2 M}{T}$$

The **bandwidth efficiency** measures how many bits per second we can squeeze into each Hz of bandwidth:

$$\eta = \frac{R_b}{BW} = \frac{\log_2(M) / T}{2/T} = \frac{\log_2 M}{2} \quad \text{[bps/Hz]}$$

This tells us that bandwidth efficiency grows with $M$. Examples:
- $M = 2$: $\eta = 0.5$ bps/Hz
- $M = 4$: $\eta = 1$ bps/Hz
- $M = 8$: $\eta = 1.5$ bps/Hz

Larger $M$ means more bits per symbol, so more information per Hz of bandwidth — which sounds great. But there is a cost.


## Bandwidth efficiency vs energy efficiency
When $M$ increases, the $M$ constellation points must share the same range of amplitudes. This means they get closer together. With symbols packed more tightly, a smaller amount of noise is enough to push a received symbol across the wrong decision threshold, causing an error. This is the fundamental tradeoff of digital modulation:

- **Increasing $M$ improves bandwidth efficiency** (more bits per Hz).
- **Increasing $M$ worsens energy efficiency** (more energy needed per bit to keep errors low).
![[Pasted image 20260307124034.png|499]]

Graphically, if you plot bandwidth efficiency and energy efficiency as functions of $M$, they are curves that cross each other: one rises while the other falls. Choosing the right modulation order $M$ for a given system is about finding the right point on this tradeoff curve, given the available power and available bandwidth.
