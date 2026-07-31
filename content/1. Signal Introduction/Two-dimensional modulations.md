So far, we have only used one dimension: amplitude. But there is no reason to stop at one dimension. We can represent signals as points in a **two-dimensional space**, where the two axes correspond to two orthogonal (independent) basis waveforms, typically a cosine and a sine at the carrier frequency.

A set of such signal points is called a **constellation**. Using two dimensions has a major advantage: for the same number of symbols $M$, a 2D constellation can space symbols farther apart than a 1D one, using less energy to achieve the same error rate. Two-dimensional modulations are therefore more energy efficient than their 1D counterparts.

## Quadrature Amplitude Modulation (QAM)
**QAM** is essentially a PAM scheme applied in two dimensions simultaneously. Each symbol is a point $(A_m^x, A_m^y)$ in the 2D plane, where the $x$-coordinate corresponds to the in-phase (I) component and the $y$-coordinate corresponds to the quadrature (Q) component.

In symmetric M-QAM, $M$ must be a perfect square (e.g., $M = 4, 16, 64, 256$). There are $\sqrt{M}$ amplitude levels on each axis, and the levels are the same as those used in $\sqrt{M}$-PAM. For 16-QAM, for instance, there are 4 levels per axis ($-3, -1, +1, +3$), giving $4 \times 4 = 16$ constellation points arranged in a square grid.
![[Pasted image 20260307125443.png|319]]
The average energy per symbol of M-QAM is lower than that of M-PAM with the same number of symbols, because the 2D spreading of points allows them to be placed more efficiently in space.

## Phase Shift Keying (PSK)
**PSK** is a different kind of 2D constellation. Instead of arranging points on a grid, PSK places all $M$ symbols on a **circle** of radius $\sqrt{E_s}$. This means every symbol has exactly the same energy.

The symbols are equally spaced around the circle, separated by angles of $2\pi/M$ radians. This maximizes the angular distance between adjacent symbols for a given energy level.
![[image_upscayl_4x_digital-art-4x.png]]
Special cases include:

- **Binary PSK (BPSK)**: 2 symbols at angles $0$ and $\pi$ (i.e., at $+\sqrt{E_s}$ and $-\sqrt{E_s}$ on the I axis). This is equivalent to 2-PAM.
- **4-PSK (QPSK)**: 4 symbols at angles $0, \pi/2, \pi, 3\pi/2$. This is identical to 4-QAM.
- **M-PSK**: $M$ equally spaced symbols on a circle, carrying $\log_2 M$ bits each.

Because all PSK symbols have equal energy, PSK constellations are rotationally symmetric. This property turns out to have a very important practical consequence related to power amplifiers.

## Transmitting 2D signals
To actually transmit a 2D symbol through a wireless channel, we use two orthogonal sinusoids as carriers: a cosine for the I component and a sine for the Q component. The transmitted signal for the $m$-th symbol is:

$$U_m(t) = A_m^x \cdot g(t) \cos(2\pi f_c t) + A_m^y \cdot g(t) \sin(2\pi f_c t)$$

The cosine and sine at the same frequency $f_c$ are orthogonal over a symbol duration, meaning they do not interfere with each other. This allows the receiver to recover each component independently.

**Modulation** works as follows: binary data comes in, groups of $\log_2 M$ bits are mapped to a symbol $(A_m^x, A_m^y)$, the I component $A_m^x \cdot g(t)$ is multiplied by $\cos(2\pi f_c t)$, the Q component $A_m^y \cdot g(t)$ is multiplied by $\sin(2\pi f_c t)$, and the two are added together to produce the transmitted waveform $U_m(t)$.

**Demodulation** works in reverse: the received signal $U(t)$ is multiplied separately by $2\cos(2\pi f_c t)$ and $2\sin(2\pi f_c t)$, and each result is passed through a low-pass filter (LPF). The mathematical reason this works is that:

$$U(t) \cdot 2\cos(2\pi f_c t) = S(t) + S(t)\cos(4\pi f_c t)$$

The first term $S(t)$ is the desired baseband signal; the second term oscillates at twice the carrier frequency and is removed by the low-pass filter. Similarly for the sine branch. This cleanly separates the I and Q components.

The M-PSK modulator has essentially the same structure, the only difference being that the constellation points all lie on a circle rather than a grid.

## Power amplifiers
The last block before the antenna in any transmitter is the **power amplifier**, which increases the signal's amplitude (and therefore its power) so it can reach the receiver over the distances involved.

Real power amplifiers have two operating regions:
- In the **linear region**, the output voltage is proportional to the input. The amplifier faithfully scales all signals by the same factor.
- In the **saturation region**, the amplifier reaches its maximum output voltage and can no longer scale the input linearly. Beyond this point, all signals get clipped to the same maximum amplitude.
![[Pasted image 20260307154025.png|465]]

Operating in saturation maximizes power transfer (you get the most output power from the amplifier). But saturation distorts signals that have varying amplitudes, because different amplitudes are no longer scaled proportionally.

### Power amplification in PSK
This is where PSK has a major practical advantage over QAM. In PSK, all constellation points lie on a circle, so all symbols have exactly the same amplitude. Even when the amplifier is driven into saturation, every symbol gets scaled by the same factor (the relative spacing between constellation points is preserved perfectly). A PSK transmitter can operate at maximum power (saturation) without degrading performance.
![[Pasted image 20260307154353.png]]
### Power amplification in QAM
QAM, on the other hand, has symbols at different distances from the origin (different amplitudes). In saturation, symbols at different distances get scaled differently: the outer symbols get clipped more than the inner ones. The constellation gets distorted and this makes it much harder for the receiver to correctly identify which symbol was sent, increasing the error rate.
![[Pasted image 20260307154455.png]]

To avoid this distortion with QAM, the amplifier must operate in the linear region, at a power level deliberately lower than its maximum. This deliberate reduction is called the **input back-off**. The consequence is that the transmitted power is lower than the amplifier's maximum capability, which shortens the communication range or requires a larger (more expensive) amplifier.

