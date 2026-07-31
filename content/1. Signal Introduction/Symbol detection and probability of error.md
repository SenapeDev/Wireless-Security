In any digital communication system, the receiver must determine which symbol was transmitted based on a received signal that has been corrupted by noise. This process, known as symbol detection, is fundamental to the correct operation of the physical layer.

## The detection problem
After a signal passes through the channel and is processed by the receiving filter (commonly called a matched filter or receiving filter), the receiver obtains a sample value $r$ that can be modeled as:

$$r = S_m + n$$

where $S_m$ is the symbol that was transmitted, drawn from a finite alphabet $\{S_1, S_2, \ldots, S_M\}$ of $M$ possible symbols, and $n$ is a noise sample. In practice, $n$ is modelled as a zero-mean Gaussian random variable, a consequence of thermal noise being well-described by an [[The communication channel and signal reception#Additive White Gaussian Noise (AWGN)|Additive White Gaussian Noise]] model. Because the noise can displace the received sample away from the transmitted symbol, the receiver cannot directly read off which symbol was sent. Instead it must make a decision based on the value of $r$.

The detection task can be stated precisely as a hypothesis testing problem: given the observed value $r$, choose among the $M$ hypotheses $H_1, H_2, \ldots, H_M$, where hypothesis $H_m$ is that symbol $S_m$ was sent. The goal is to design a decision rule that minimizes the probability of choosing the wrong hypothesis.

### The MAP decision rule
The optimal decision rule under the criterion of minimum error probability is the **Maximum a Posteriori** (*MAP*) rule. The MAP rule selects the symbol $S_m$ that maximizes the posterior probability of having been sent, given the received value:

$$\hat{m} = \underset{m}{\arg\max} \; P(S_m \text{ sent} \mid r \text{ received})$$

By Bayes' theorem, this posterior probability is proportional to the product of the likelihood of receiving $r$ given that $S_m$ was sent, and the prior probability of $S_m$. When all symbols are equally likely a priori, the prior probabilities are uniform and the MAP rule reduces to the **Maximum Likelihood** (*ML*) rule, which simply selects the symbol that makes the observed $r$ most probable.

Under the AWGN model, the conditional density of $r$ given that $S_m$ was sent is a Gaussian centered at $S_m$. Maximizing this Gaussian likelihood is equivalent to minimizing the squared distance between $r$ and each candidate symbol. The ML rule therefore reduces to minimum distance decoding: the receiver picks the symbol $S_m$ that is closest to $r$ in the sense of minimizing the squared Euclidean distance

$$d(r, S_m) = (r - S_m)^2$$

This geometric interpretation is intuitive: the received value $r$ is placed in a one-dimensional space, and the receiver assigns it to the nearest symbol point.

#### Example: 2-PAM detection

Two-level pulse amplitude modulation (2-PAM) is the simplest case and illustrates the MAP rule clearly. The two symbols are $S_1 = +\sqrt{E_b}$ and $S_2 = -\sqrt{E_b}$, where $E_b$ denotes the energy per bit. If $S_1$ was transmitted, the received sample is $r = +\sqrt{E_b} + n$; if $S_2$ was transmitted, $r = -\sqrt{E_b} + n$. The two conditional distributions are Gaussian curves of equal width centered at $+\sqrt{E_b}$ and $-\sqrt{E_b}$ respectively. They intersect at $r = 0$, which is the decision threshold. The minimum distance rule then gives: if $r > 0$, decide $S_1$ was sent; if $r < 0$, decide $S_2$ was sent.
![[Pasted image 20260314152403.png]]
An error occurs whenever the noise term $n$ is large enough in magnitude to push $r$ across the threshold. The probability of this happening depends on the ratio of the symbol separation to the noise level, captured by the signal-to-noise ratio $E_b/N_0$.

## Probability of error

The probability of error $P_e$ between two symbols separated by a distance $d$ in signal space is given by:

$$P_e(d) = Q\!\left(\sqrt{\frac{d^2}{2N_0}}\right)$$

where $N_0$ is the one-sided noise power spectral density (noise density), and $Q(\cdot)$ is the Gaussian Q-function, defined as the probability that a standard normal random variable exceeds its argument. The argument $\sqrt{d^2 / 2N_0}$ is a normalised measure of how far apart the two symbols are relative to the noise level: larger values correspond to lower error probabilities.

The **signal-to-noise ratio** (*SNR*) appears through the received energy per bit $E_b$ and the noise density $N_0$. Specifically, SNR is proportional to the received power, which is in turn determined by the transmission power, the channel attenuation, and the data rate. Higher received power increases the effective symbol separation relative to the noise, reducing the error probability.

### Bit error rate and modulation order

In practice, the performance of a modulation scheme is characterised by the **bit error rate** (*BER*) rather than the symbol error probability, because bits are the fundamental unit of information. For an $M$-ary modulation scheme, each symbol carries $\log_2 M$ bits. Under the assumption of [[Signal transmission and reception#Gray coding|Gray coding]], where adjacent symbols differ by exactly one bit, most symbol errors produce only a single bit error. In this case the BER is approximately:

$$\text{BER} \approx \frac{P_e}{\log_2 M}$$

This relationship reveals a fundamental trade-off in the design of modulation schemes. Increasing $M$ allows more bits to be transmitted per symbol, which improves spectral efficiency. However, for a fixed total power, a larger $M$ means the symbols must be packed more closely together in signal space, reducing the minimum distance $d$ between neighbouring symbols and therefore increasing $P_e$. As a result, higher-order modulations such as 256-QAM or 256-PAM require a substantially larger $E_b/N_0$ to achieve the same BER as lower-order schemes such as 2-PAM or 4-QAM.
![[Pasted image 20260314152542.png]]
This performance degradation for increasing modulation order is clearly visible when BER curves are plotted against $E_b/N_0$ expressed in decibels. For both QAM and PAM families, the curves shift to the right as $M$ increases, meaning that more SNR is needed to achieve a given BER target. The curves are steep in the region of practical interest, so even a small reduction in received SNR can cause the BER to increase by several orders of magnitude. This sensitivity underlines the importance of accurate power control and channel estimation in real communication systems.