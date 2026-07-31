## Introduction
Jamming is the simplest and most direct form of intentional GNSS attack. A jammer emits electromagnetic radiation near the victim receiver with the goal of masking the legitimate GNSS signals under noise, preventing the receiver from processing them. The mechanism exploits the extremely low power of GNSS signals: even a modest jammer can raise the effective noise floor at the receiver input to the point where the SNR falls below the threshold required for signal acquisition and tracking.

The effects on the receiver are progressive and well-understood. First, the estimated carrier-to-noise-density ratio (C/N0), which is the primary figure of merit for signal quality reported by GNSS receivers, drops sharply across all visible satellites. As the interference power increases, the receiver loses synchronism with the spreading code and the carrier, first struggling to maintain tracking loops and eventually losing lock entirely. The result is a complete loss of the navigation solution, meaning the receiver can no longer compute position, velocity, or time (PVT). This constitutes a **Denial-of-Service** (*DoS*): the user knows that GNSS is unavailable, because the receiver simply stops providing a position fix.

>Jamming is a relatively transparent attack in the sense that its effect is immediately apparent to the user: navigation fails openly. A jammer does not deceive the user about their location; it simply removes GNSS service entirely.


## Impact on GNSS receiver
To understand detection and mitigation strategies, it is helpful to consider where in the receiver processing chain interference exerts its effects. A GNSS receiver can be conceptually divided into two stages. 
- The first stage, the **front-end**, conditions the incoming RF signal: it passes through a bandpass filter (BPF), is amplified or attenuated by an automatic gain control (AGC) stage, and is then digitized by an analog-to-digital converter (ADC). 
- The second stage performs **signal processing**: it correlates the digitized samples with local code and carrier replicas (tracking loops including phase-locked loops and delay-locked loops), extracts pseudorange and Doppler measurements, and computes the PVT solution.
![[Pasted image 20260318161923.png]]
Interference affects both stages. At the front-end level, a strong interferer causes the AGC to reduce its gain in order to prevent ADC saturation, and it distorts the statistical distribution of the digitized samples. At the signal processing level, interference raises the effective noise in the correlation output, degrading pseudorange accuracy and eventually causing loss of lock.
![[Pasted image 20260319104753.png]]

## Detection methods
###  Carrier-to-noise ratio monitoring
**C/N0 monitoring** is the most universally available detection method, since the carrier-to-noise-density ratio is a standard output of virtually all GNSS receivers. Because interference increases the effective noise power, the denominator of the C/N0 estimate grows, causing the reported C/N0 to drop across all tracked satellites simultaneously. By comparing the observed C/N0 against a statistical threshold established under interference-free conditions, a receiver can declare a jamming event. A practical limitation is that the C/N0 estimation algorithm is proprietary and varies by manufacturer; in some cases, the algorithm may internally compensate for or mask the interference, reducing detection sensitivity.
![[Pasted image 20260319105929.png|565]]

### Automatic Gain Control monitoring
**AGC monitoring** provides a complementary and often more direct indicator. The AGC's role is to amplify or attenuate the input signal so that the ADC (*Analog-to-Digital Converter*) operates within its optimal dynamic range. Under normal conditions, the GNSS signal is buried in thermal noise, and the AGC gain is stable or changes only slowly. When a strong interferer is present, the total received power increases, and the AGC responds by reducing its gain. This reduction in AGC gain is a reliable symptom of increased RF power in the band, whether from a jammer or any other strong source. In a hostile environment, the AGC gain is not only lower on average but also varies more rapidly over time, tracking the fluctuations of the swept interferer.
![[Pasted image 20260319105959.png|500]]

### Spectral analysis 
**Spectral analysis** examines the frequency-domain representation of the digitized signal at the ADC output. Under interference-free conditions, the spectrum shows only the shape of the front-end bandpass filter, with the GNSS signal itself invisible below the noise floor. When interference is present, distinct spectral components appear at frequencies corresponding to the interferer, often as sharp peaks or elevated spectral regions narrower than 1 MHz. Spectral analysis allows interference to be not only detected but also characterized in terms of its frequency, bandwidth, and power.
![[Pasted image 20260319105822.png|431]]

### Goodness-of-fit test
**Goodness-of-fit** testing is a statistical detection method that operates on the samples at the ADC output. Under interference-free conditions, the GNSS signal is dominated by thermal noise, and the samples follow a Gaussian distribution. The GoF test compares the histogram of the observed samples against the expected Gaussian distribution. When an interferer is present, it distorts the amplitude distribution of the samples, causing the histogram to deviate from Gaussian shape. The degree of deviation is quantified by a statistical measure such as the **p-value**, which reflects the probability of observing the measured histogram under the null hypothesis of no interference. A small p-value indicates a significant departure from Gaussian statistics and triggers an interference alarm. The method requires no prior knowledge of the interference signal's characteristics, has a low computational burden, and can achieve detection at low interference power levels. Calibration is performed in a noise-only scenario to establish the reference Gaussian distribution.
![[Pasted image 20260319110120.png]]
### Machine learning
**Machine learning approaches** extend the detection problem to interference classification. Once interference is detected, it is useful to identify its type (e.g., which chirp pattern) to activate the most appropriate mitigation strategy. Supervised machine learning models can be trained on labeled datasets containing examples of different jammer types at various power levels. Features are extracted from the digitized ADC samples in both the time domain and the frequency domain, and these feature vectors are fed to a classifier. This approach treats interference detection and classification as a standard supervised classification task, enabling automated selection of countermeasures.
![[spoofing-machine-learning-detection.png]]

## Mitigation techniques

Mitigation strategies can be applied at different stages of the receiver chain, and the appropriate choice depends on the type and spectral characteristics of the interference.

### Frequency domain excision
**Frequency domain excision** targets narrowband or tonal interferers. The approach involves computing a spectral estimate of the received signal, identifying frequency bins where the power exceeds a threshold (the FDAF threshold), nulling or suppressing those bins, and then reconstructing the time-domain signal via inverse FFT. This removes the spurious spectral components while leaving the broadband GNSS signal largely intact. The effectiveness of this technique depends on the quality of the spectral estimate and the ability to distinguish the interferer's spectral peaks from the noise floor.
![[Pasted image 20260319114330.png]]
A classical implementation of frequency-domain mitigation is the **notch filter**, which places a sharp attenuation notch at the frequency of a continuous wave interferer. The notch filter parameters involve a trade-off between selectivity (how narrow and deep the notch is) and stability (how well-conditioned the filter remains). For swept-frequency jammers whose instantaneous frequency varies over time, a **static notch filter** is insufficient because the interference frequency is not fixed. The **adaptive notch filter** addresses this by continuously estimating the current interference frequency and updating the filter pole position in real time, allowing the notch to track the sweeping tone.

>Frequency-domain excision is a technique that removes interference by analyzing the signal spectrum. It detects frequency components with unusually high power and suppresses or removes them. It is mainly used against narrowband or continuous-wave interference.

![[Pasted image 20260319114345.png]]
### Time-domain pulse blanking
**Time-domain pulse blanking** is the standard mitigation technique for pulsed interference. It operates on the digitized samples: whenever a sample's amplitude exceeds a threshold, indicating the presence of a pulse, the sample is replaced by zero (blanked). This suppresses the pulse energy at the cost of losing the GNSS signal during the blanked intervals. The main drawback is that both the interference and any useful signal present during the pulse are removed, and if the duty cycle of the pulsed interferer is high, a significant fraction of the useful signal is discarded.
>Time-domain pulse blanking is a technique that removes short and powerful interference pulses directly from the received signal. It detects samples with an amplitude above a threshold and replaces them with zero or another estimated value. It is mainly used against impulsive interference.

![[Pasted image 20260319114640.png]]
### Transformed domain methods
**Transformed domain methods** offer a more general framework. These techniques apply transformations such as the Gabor transform, wavelet packet decomposition, or the Karhunen-Loève transform to represent the signal in a domain where the GNSS signal and the interference are more separable. In the transformed domain, a thresholding operation identifies coefficients dominated by interference, which are then suppressed (excised) or used to synthesize and subtract a replica of the interference. The cleaned signal is then reconstructed by applying the inverse transformation. These methods can be effective against a broader variety of interference types but generally involve higher computational complexity.

### Antenna-level mitigation
**Antenna-level mitigation** addresses interference through spatial filtering. Controlled reception pattern antennas (CRPAs) or antenna arrays can steer nulls in the direction of the interfering source while maintaining sensitivity toward the satellites. This approach is particularly effective when the interference arrives from a known or estimable direction, but it requires multi-element antenna hardware that is not available in mass-market receivers.