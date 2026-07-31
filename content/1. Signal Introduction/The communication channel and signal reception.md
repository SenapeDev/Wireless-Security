## What happens between transmitter and receiver
Once a signal leaves the transmitter, it enters the physical world, which is far from perfect. The channel, meaning the medium through which the signal travels, does not simply deliver a perfect copy of what was sent. It corrupts, distorts, and weakens the signal in several ways before it reaches the receiver.

### What the channel does to a signal
The channel is the physical medium through which the analog signal travels between transmitter and receiver. In an ideal world, the channel would deliver the signal exactly as it was sent. In reality, several types of disturbance act on the signal simultaneously.

- **Frequency-domain distortion** means the channel does not treat all frequencies equally. Some frequency components of the signal are attenuated more than others, so the shape of the signal's spectrum is altered. 
- **Wireless fading** refers to variations in the channel's behavior over time and frequency, caused by the physical environment (reflections off buildings, movement of the user, and so on).
- **Additive noise** is a random disturbance that adds itself on top of the signal at the receiver.
- **Impulsive noise** consists of sudden, short-duration spikes of energy that can severely corrupt individual symbols.

Beyond these, there are two important types of interference. 
- **Interchannel interference** comes from signals transmitted on neighboring frequency channels, which leak into the channel of interest. 
- **Cochannel interference** comes from other transmitters using the same frequency channel (for instance, a base station in a distant cell of a cellular network operating at the same frequency). 
- Finally, **intentional interference** (*jamming*) refers to deliberate attempts by an adversary to disrupt communication

## The two major sources of error
While the list of channel impairments is long, two phenomena dominate the analysis of most communication systems.
### Additive White Gaussian Noise (AWGN)
The most fundamental and universal source of degradation is **thermal noise**, which arises from the random motion of electrons in any electronic component. This type of noise has three key properties that together give it the name AWGN:
1. It is **additive**, meaning it simply adds itself to the transmitted signal. The received signal $r(t)$ is the sum of the transmitted signal $s_i(t)$ and the noise $n(t)$:

$$r(t)=si​(t)+n(t)$$

2. It is **white**, meaning its power is spread equally across all frequencies. Just as white light contains all colors equally, white noise contains all frequencies equally. This is a mathematical idealization, but it is an excellent approximation for thermal noise across the frequency ranges used in communications.
3. It is modeled as **Gaussian noise**, meaning that at any given instant, the noise value follows a Gaussian (bell-curve) probability distribution. The width of this distribution is characterized by the **noise density** $N_0$​: a higher $N_0$ means wider, more spread-out noise and more disruption to the signal.

The practical effect of AWGN can be seen clearly by comparing a transmitted and a received signal. A clean rectangular pulse sequence, for example, arrives at the receiver covered in rapid random fluctuations. The overall shape is still recognizable, but the exact amplitude at any moment is uncertain.
![[Pasted image 20260314101307.png]]

### Inter-Symbol Interference (ISI)
The second major source of error is **Inter-Symbol Interference**, or *ISI*. This arises because any real communication channel behaves like a filter: it has a limited bandwidth and a non-flat frequency response. When a signal passes through such a channel, each transmitted pulse is spread out in time. As a result, the tail of one pulse overlaps with the beginning of the next, causing adjacent symbols to interfere with each other.

ISI can be understood by looking at the channel as a system with an **impulse response** $h_c(t)$ (or equivalently, a frequency response $H_c(f)$). When the transmitted signal $s_i(t)$ passes through the channel, the received signal is the convolution of $s_i(t)$ with $h_c(t)$, plus the additive noise:

$$r(t) = s_i(t) * h_c(t) + n(t)$$

The convolution operation (denoted by $*$) is what causes the *smearing*: it mixes together the signal at different time instants, creating interference between neighboring symbols.

In the frequency domain, the channel's response $H_c(f)$ can be written as:
$$H_c(f) = |H_c(f)| \cdot e^{j\theta_c(f)}$$
The magnitude $|H_c(f)|$ varies with frequency, causing **amplitude distortion** (different frequency components of the signal are attenuated by different amounts). The phase term $\theta_c(f)$ is non-linear in frequency, causing **phase distortion** (different frequency components arrive at the receiver with different delays). Both effects contribute to ISI.

## What the receiver must do
Given that the received signal has been corrupted by both noise and ISI, the receiver faces two distinct tasks, which are handled in sequence.

1. The first task is **demodulation and sampling**: the receiver must take the incoming analog waveform $r(t)$ and process it to prepare a clean, reliable sample for the second stage. This involves three sub-steps: improving the *signal-to-noise ratio* (SNR) as much as possible, reducing the ISI caused by the channel, and then sampling the processed waveform at the right moment to obtain a single numerical value per symbol.
2. The second task is **detection**: given the sample value, the receiver must decide which symbol was most likely transmitted. This is a decision-making step, comparing the sample to thresholds and selecting the nearest constellation point.

The full receiver chain therefore looks like this: the received waveform $r(t)$ enters a **frequency down-conversion** stage (which shifts the bandpass signal back to baseband), then passes through a **receiving filter** (designed to maximize SNR), then an **equalizing filter** (designed to reduce ISI), and finally a **threshold comparator** that outputs the estimated symbol $\hat{m}_i$.

### Maximizing the SNR: the matched filter

The question of how to choose the receiving filter to maximize SNR has a precise and elegant answer. In the simplified AWGN model where the received signal is $r(t) = s_i(t) + n(t)$, the noise $n(t)$ is a random process whose variance is proportional to the noise density $N_0$​. The goal is to find the filter impulse response $h(t)$ that, when applied to $r(t)$, gives the highest possible ratio of signal power to noise power at the sampling instant $t=T$.

The optimal filter is called the **matched filter**, and its impulse response is:

$$h(t) = g(T - t)$$

where $g(t)$ is the pulse shape used by the transmitter. This formula says that the matched filter is a time-reversed and delayed version of the transmitted pulse. For a simple rectangular pulse of duration $T$ and amplitude $A$, the matched filter is another rectangular pulse of the same shape; the time reversal of a symmetric pulse leaves it unchanged.

The intuition behind the matched filter is that it "correlates" the received signal with the known pulse shape. It is accumulating evidence over the entire symbol duration and concentrating all of that energy into a single sample at time $T$. In doing so, it squeezes out as much signal as possible while limiting the noise contribution, achieving the best possible SNR at the decision instant.

### Minimizing ISI: equalization and channel estimation

While the matched filter addresses noise, the equalizer addresses ISI. The idea is conceptually straightforward: if the channel has distorted the signal by applying a frequency response $Hc​(f)$, the receiver can attempt to undo this distortion by applying the inverse response. The ideal equalizer would have a frequency response:

$$H_e(f) = \frac{1}{H_c(f)}$$​

Passing the received signal through this equalizer would perfectly cancel the channel's effect, recovering an approximation $\hat{s}_i(t)$ of the original transmitted signal. In practice, a perfect inversion is not always possible (for instance, if $H_c(f) = 0$ at some frequency, the inverse is undefined), so equalizers are designed to find the best approximation.

A critical prerequisite for equalization is that the receiver must actually know $H_c(f)$, the channel's frequency response. This is the problem of **channel estimation**. The channel transfer function cannot be assumed to be known in advance; it depends on the physical environment and changes over time. Channel estimation is performed by transmitting **known reference signals** and observing how they are distorted. By comparing what was sent with what was received for these known sequences, the receiver can infer $H_c(f)$.

Channel estimation strategies differ in how much prior knowledge they use.
- In **blind channel estimation**, the receiver attempts to infer the channel purely from the statistics of the received data, without any dedicated reference signals. 
- In **semi-blind estimation**, a small number of known reference symbols are combined with statistical methods. 
- In **pilot-assisted channel estimation**, regularly spaced known symbols (called *pilot symbols* or *pilots*) are inserted into the transmission stream. The receiver uses these pilots to estimate the channel, and then interpolates between pilot positions to reconstruct the channel at all other time-frequency points.

## Fading
One of the defining characteristics of wireless channels, as opposed to wired ones, is that the channel is not static. As the user moves, as objects in the environment move, and as propagation conditions change, the impulse response $h_c(t)$ itself varies over time. This phenomenon is called **fading**.

Fading has two important dimensions. The first is how rapidly the channel changes, which is described by the terms *slow* and *fast fading*. The second is whether the channel affects all frequencies equally (*flat fading*) or different frequencies differently (*frequency-selective fading*). 

### Slow fading
In a **slow fading** channel, the channel response changes slowly relative to the symbol duration. The channel essentially stays constant for many consecutive symbol periods, then gradually shifts. This means the receiver does not need to re-estimate the channel very often, so pilot symbols can be inserted sparsely in time. The 3D plot of a slow fading channel shows the channel amplitude (in dB) as a surface over frequency and time: the surface is smooth and changes gradually along the time axis.
![[Pasted image 20260314115051.png]]
### Fast fading
In a **fast fading** channel, the channel response changes rapidly potentially varying significantly within the span of just a few symbols). The channel must be tracked much more frequently, requiring pilots to be inserted more densely. The corresponding 3D plot shows a much more irregular surface, with sharp peaks and deep nulls (near $−50 dB$) that appear and disappear rapidly along the time axis. These deep nulls are particularly dangerous: when the channel amplitude drops near zero at a given frequency and time, any signal energy in that region is essentially lost.
![[Pasted image 20260314115117.png]]

The density and arrangement of pilot symbols must match the fading rate. In systems like **OFDM** (*Orthogonal Frequency Division Multiplexing*), pilots can be arranged across both time and frequency in a grid. 
- For a slowly fading channel, a **block-type** arrangement is used: pilots occupy entire OFDM symbols at widely spaced time intervals, since the channel changes slowly enough that a single estimate remains valid for a long time. 
- For a fast fading channel, a **comb-type** arrangement is more appropriate: pilots are spread across every OFDM symbol but on only a subset of frequency subcarriers, providing continuous tracking of the channel's time evolution. 

In both cases, the underlying principle is the same: sample the channel frequently enough to track its variation, without wasting too much transmission capacity on pilots that carry no user data.

![[Pasted image 20260314143701.png]]