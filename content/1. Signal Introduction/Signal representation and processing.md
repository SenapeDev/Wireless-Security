## From time domain to frequency domain
We have seen that any signal can be described as a function of time. However, this description alone is often not the most useful one in practice. A much more powerful perspective is obtained by asking: what frequencies make up a given signal, and how strongly is each frequency present?

To answer this, we start from a well-known mathematical object: the **complex exponential**. Using Euler's formula, a complex exponential at frequency $f$ can be written as:

$$e^{j2\pi ft} = \cos(2\pi ft) + j\sin(2\pi ft)$$

This tells us that a complex exponential is simply a combination of a cosine (the **real part**) and a sine (the **imaginary part**), both oscillating at frequency $f$. These sinusoidal functions, taken at a discrete set of frequencies $f_n = n/T$ (where $n$ is an integer and $T$ is the duration of the signal), form an **orthonormal basis** (meaning they are mutually orthogonal and have unit energy). It can be shown mathematically that any signal defined over a finite interval $[-T/2, T/2]$, or any periodic signal, can be written exactly as a weighted sum of these basis functions:

$$x(t) = \frac{1}{\sqrt{T}} \sum_{n=-\infty}^{\infty} c_n , e^{j\frac{2\pi}{T}nt}$$

The coefficients $c_n$ are computed via the scalar product between the signal and each basis function:

$$c_n = \frac{1}{\sqrt{T}} \int_{-T/2}^{T/2} x(t) , e^{-j\frac{2\pi}{T}nt} , dt$$

Each coefficient $c_n$ tells us how much the sinusoidal component at frequency $f_n = n/T$ (called the **$n$-th harmonic**) contributes to the signal $x(t)$. The modulus $|c_n|$ gives the amplitude of that contribution.

## The Fourier transform
The representation above works for periodic or finite-duration signals with discrete frequencies $f_n = n/T$. A natural question is: can we generalize this to any signal and to all possible frequencies, not just the discrete set $n/T$?

The answer is yes, and the result is the **Fourier transform**. Given an arbitrary signal $x(t)$, its Fourier transform is defined as:

$$X(f) = \int_{-\infty}^{\infty} x(t) , e^{-j2\pi ft} , dt$$

The function $X(f)$ is in general complex-valued, and it tells us the "weight"  (both amplitude and phase) of the sinusoidal component at each continuous frequency $f$. This is the **frequency-domain** or **spectral** representation of the signal.

The original signal can always be recovered from its Fourier transform via the **inverse Fourier transform**:

$$x(t) = \int_{-\infty}^{\infty} X(f) , e^{j2\pi ft} , df$$

This formula confirms that any signal can be decomposed into a continuous superposition of sinusoidal components at all frequencies, each weighted by $X(f)$.

There are three important observations to keep in mind:
1. Every signal has a unique spectral representation: knowing $X(f)$ is completely equivalent to knowing $x(t)$. The two are simply two different ways of describing the same object.
2. Every operation applied to a signal in the time domain has a precise equivalent effect in the frequency domain. This makes spectral analysis an extremely powerful tool for signal processing.
3. Perhaps counterintuitively, **a signal of finite duration has a spectrum that extends over an infinite range of frequencies**. A classic example is the rectangular pulse (a signal that is constant for a finite time and zero elsewhere): its Fourier transform is a **sinc function**, which has side lobes extending to infinity in the frequency domain. This means that perfectly time-limited signals cannot also be perfectly band-limited, a fundamental constraint with practical implications in all communication systems.

## Bandwidth
The **bandwidth** of a signal is the range of frequencies that the signal meaningfully occupies. Since most real signals have a spectrum that extends, at least in principle, to infinity, the definition of bandwidth requires some care.

The most common practical definition is the **3 dB bandwidth**, which is the width of the frequency interval over which the **squared magnitude of the spectrum** $|X(f)|^2$ remains above half its peak value. The factor of one half corresponds to a reduction of 3 dB on a logarithmic scale, hence the name.
![[Pasted image 20260308110937.png|387]]
Bandwidth can be expressed in two ways: the **one-sided bandwidth** measures only the positive-frequency half of the spectrum (used when the signal is defined as a real-valued baseband signal), while the **two-sided bandwidth** accounts for both positive and negative frequencies (used when working with complex or passband signals). The two are simply related by a factor of two.
![[Pasted image 20260308112942.png]]
## Linear systems and filters
In communications, signals are constantly being processed: they are amplified, attenuated, shaped, and filtered. All such processing operations can be modeled as **systems**. A particularly important class is that of **linear time-invariant** (*LTI*) systems, which are systems whose behavior does not change over time and that satisfy the superposition principle.

An LTI system is fully characterized in the frequency domain by its **frequency response** $H(f)$. When a signal $x(t)$ passes through such a system, the output $y(t)$ has a Fourier transform given by the simple product:

$$Y(f) = X(f) \cdot H(f)$$

This is one of the most important results in signal processing: what would be a complex convolution integral in the time domain becomes a simple pointwise multiplication in the frequency domain.

When an LTI system is designed to selectively pass some frequencies while blocking others, it is called a **filter**. The most common types are the **low-pass filter** (passes low frequencies, blocks high ones), the **high-pass filter** (the opposite), and the **band-pass filter** (passes only a selected range of frequencies). The relationship between signal bandwidth and filter bandwidth is critical: if the signal bandwidth is narrower than the filter bandwidth, the signal passes through largely undistorted. If the signal bandwidth is wider than the filter bandwidth, the filter clips the outer frequency components and distorts the signal.
![[Pasted image 20260308113015.png]]
In the context of wireless communications, filters serve multiple roles. They are used to shape the transmitted signal so that it occupies only its assigned frequency band; they are used at the receiver to eliminate out-of-band noise and interference; and they are used to model the distortion introduced by the wireless channel itself. Devices that reverse channel distortion at the receiver are called **equalizers**, and they can also be modeled as filters with a frequency response designed to compensate for $H(f)$ of the channel.

## Signal modulation

### The modulation property
One of the most practically important consequences of the Fourier transform is the **modulation property**. When a signal $x(t)$ is multiplied by a sinusoidal carrier $\cos(2\pi f_0 t)$ at frequency $f_0$, the spectrum of the resulting signal $y(t) = x(t)\cos(2\pi f_0 t)$ is:

$$Y(f) = \frac{1}{2}\left[X(f - f_0) + X(f + f_0)\right]$$

In plain words: multiplying a signal by a sinusoid **shifts its spectrum** by $\pm f_0$. The original spectrum, which was centered at zero (a **baseband signal**), now appears as two copies centered at $+f_0$ and $-f_0$.

This operation is called **modulation**, and $f_0$ is the **carrier frequency**. Its importance in wireless communications cannot be overstated. Radio channels do not transmit all frequencies equally well: different frequency bands have different propagation characteristics, are subject to different regulations, and are allocated to different services. Modulation allows a baseband signal (such as the output of a microphone, a data encoder, or a GPS chip) to be translated to whatever frequency band is appropriate for transmission. The signal is then said to be a **passband signal**.

### Demodulation
At the receiver, the original baseband signal must be recovered from the passband signal. This process is called **demodulation**, and it is achieved in two steps.
1. The received signal $y(t)$ is multiplied again by the same carrier $\cos(2\pi f_0 t)$. Applying the modulation property a second time, this shifts the spectrum again by $\pm f_0$, bringing the baseband content back to the vicinity of zero frequency. However, this operation also creates additional unwanted spectral copies at $\pm 2f_0$.
2. A **low-pass filter** is applied to the result. This eliminates all frequency content above a certain cutoff, removing the unwanted copies at $2f_0$ while retaining the reconstructed baseband signal. The output is proportional to the original signal $x(t)$, completing the demodulation.

A critical requirement for this process to work correctly is that the receiver must know the carrier frequency $f_0$ with sufficient accuracy, and ideally also the phase of the carrier. If the receiver uses a slightly different frequency or phase, errors are introduced into the reconstructed signal.

## Frequency division multiplexing (FDM)
Modulation enables not only the transmission of a single signal over a channel, but also the simultaneous transmission of multiple independent signals over the same medium without mutual interference. This is achieved through **Frequency Division Multiplexing** (*FDM*).

The principle is straightforward. Suppose we have three signals $x_1(t)$, $x_2(t)$, and $x_3(t)$, each with its own bandwidth $B_1$, $B_2$, $B_3$. Each signal is modulated onto a different carrier frequency $f_1$, $f_2$, $f_3$, chosen so that the shifted spectra do not overlap. Specifically, each carrier frequency must be large enough to ensure adequate spectral separation from the adjacent channels:

$$f_1 > B_1, \quad f_2 > f_1 + B_1 + B_2, \quad f_3 > f_2 + B_2 + B_3$$

The three modulated signals are then summed and transmitted simultaneously over the shared channel. At the receiver, each individual signal is extracted by applying a **band-pass filter** centered on the corresponding carrier frequency, followed by demodulation. Provided the spectral regions do not overlap, the signals can be separated without distortion.
![[Pasted image 20260308113716.png]]
FDM is the foundational principle behind many everyday wireless systems. AM and FM radio stations, television broadcasts, mobile telephony channels, and satellite navigation signals all coexist in the radio spectrum by occupying different, non-overlapping frequency bands.


## Analog-to-digital Conversion (ADC)
**Analog-to-Digital Conversion (ADC)** proceeds in two distinct stages: **sampling** and **quantization**.

### Sampling
Sampling is the operation of measuring the value of a continuous-time analog signal $x(t)$ at regular, equally spaced instants of time. The time between two consecutive measurements is called the **sampling interval** $T_c$, and the number of measurements taken per second is the **sampling frequency** $f_c$, where:

$$f_c = \frac{1}{T_c}$$

![[signal-samping.png|531]]

The result of sampling is a **discrete-time signal**: a sequence of numbers $x(0), x(T_c), x(2T_c), \ldots$, each representing the signal's value at a specific instant. The continuous, smooth waveform has been replaced by a series of individual measurements taken at a regular rhythm.

### The Nyquist-Shannon sampling theorem

> [!success] Nyquist-Shannon theorem
> A continuous-time signal with one-sided bandwidth $B$ can be perfectly reconstructed from its samples if and only if the sampling frequency satisfies: $$f_c > 2B \quad \Longleftrightarrow \quad T_c < \frac{1}{2B}$$

The minimum acceptable sampling rate, $2B$, is called the **Nyquist rate**. Sampling at or above this rate guarantees that no information is lost: the original continuous signal can be recovered exactly from the discrete sequence of samples using an appropriate reconstruction formula (essentially, a low-pass filter applied to the samples).

### Quantization
Sampling produces a discrete-time signal, but each sample is still a continuous-valued number. To represent it digitally, each sample must be approximated by one of a finite number of discrete levels — this process is called **quantization**.

In a typical $n$-bit quantizer, the range of possible signal values is divided into $2^n$ equal intervals, and each sample is rounded to the nearest level. Each level is then encoded as a binary word of $n$ bits. For example, a 4-bit quantizer ($n = 4$) produces $2^4 = 16$ discrete levels, and represents each sample as one of 16 possible 4-bit codes (from 0000 to 1111).

Quantization inevitably introduces a small error: the difference between the true sample value and the nearest discrete level. This error is called **quantization noise**. It behaves approximately as a random noise source, and its magnitude decreases as the number of bits $n$ increases — each additional bit roughly halves the quantization error and thus improves the signal quality. In practice, the trade-off between precision and the number of bits (and thus the data rate) is an important design parameter in any digital communication system.

### From samples to bits
After sampling and quantization, the analog signal has been transformed into a sequence of $n$-bit binary words, one for each sample. This bitstream is the digital representation of the original signal and can now be processed, compressed, encrypted, encoded for error correction, and ultimately transmitted over a digital communication system.
![[Pasted image 20260308124059.png]]
To give a concrete sense of scale: an audio signal with a bandwidth of approximately 4 kHz (sufficient for telephone-quality speech) requires a sampling rate of at least $f_c = 2 \times 4000 = 8000$ samples per second. If each sample is quantized to 8 bits, the resulting bitstream has a rate of $8000 \times 8 = 64{,}000$ bits per second, or 64 kbps. This is precisely the bit rate of the standard G.711 telephone codec, one of the oldest and most widely used digital voice standards.
