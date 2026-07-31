## Introduction
When information is transmitted over a **wireless channel**, it becomes inherently vulnerable. Unlike wired communication, where physical access to the medium is required to intercept data, wireless transmission relies on radio signals that propagate through open space. 
This means that anyone within range can potentially: 
- **overhear** a transmission 
- **inject** fake messages into the network
- **replay** previously captured signals 
- **interfere** with communications through *jamming*

### Overview of a digital communication system
A digital communication system can be divided into three logical sections:
- the **user section**
- the **interface section**
- the **channel section**

![[digital-communication.png]]
#### User section
The user section is where the information to be transmitted originates. This information is typically digital or converted from an analog source. The goal of this section is simply to produce a sequence of bits that faithfully represents the original information.
#### Interface section
The interface section is responsible for transforming those bits into a physical signal that can actually travel through the channel.
- On the *transmitter side*, this is accomplished by two main components:
	- The **encoder**, that performs two distinct operations: 
		- **Source encoding**, which compresses the data to reduce redundancy and save bandwidth.
		- **Channel encoding**, which adds controlled redundancy to make the transmission more robust against errors and disturbances introduced by the channel. 
	- The **modulator** then takes the encoded digital signal and converts it into an analog waveform suitable for transmission. 
- On the *receiver side*, the process is reversed:
	- the **demodulator** converts the received analog signal back into a sequence of discrete samples. 
	- the **decoder** extracts the original information by performing channel and source decoding in reverse order.
#### Channel section
The channel section represents the physical medium through which the analog signal travels from transmitter to receiver. In wireless systems, this is the radio propagation environment, and it introduces several types of disturbances: 
- *frequency-domain distortion*
- *wireless fading*
- *additive noise*
- *impulsive noise* and various forms of *interference*, both from other frequency bands, from other users on the same frequency, and from malicious actors.

## Signal representation
A **signal** is a mathematical function that conveys information about a physical phenomenon. Signals describe the evolution of physical quantities, such as voltage or current, over time. Mathematically, a signal is represented as a function of a real variable (time) that takes real or complex values.

Signals can be broadly classified into two categories:
- **Analog signals**, that vary continuously over time and can take any value within a range.
- **Digital signals**, by contrast, that take only a discrete set of values at discrete time instants. 

The conversion between these two representations is one of the fundamental operations in a digital communication system.

### Energy and power of signals 
Two key scalar quantities are associated with any signal. 
- The **energy** of a signal is defined as the integral of the squared modulus of the signal over all time.
$$E(x) \triangleq \int_{-\infty}^{\infty} |x(t)|^2 \, dt$$
- The **average power** is the time-average of the instantaneous power, which itself coincides with the squared modulus of the signal at each instant.
  $$P(x) \triangleq \lim_{a \to \infty} \frac{1}{2a}  
\int_{-a}^{a} |x(t)|^2 \, dt$$

Both energy and average power are real scalar numbers and carry an intuitive physical interpretation: they correspond to the energy dissipated and the average power delivered to a unit resistor, respectively.

### Signal representation using basis functions
Rather than describing signals purely as time functions, it is often more useful and efficient to represent them as **linear combinations of simpler, elementary signals**. This is possible thanks to the concept of an **orthonormal basis**, a set of functions that are mutually orthogonal (i.e., their scalar product is zero) and normalized in energy.

The **scalar product** between two signals is defined as the integral of the product of one signal with the complex conjugate of the other. 
$$\langle \mathbf{x}, \mathbf{y} \rangle = \langle x(t), y(t) \rangle \triangleq \int_{-\infty}^{\infty} x(t)\,y^*(t)\,dt$$

It provides a measure of similarity between two signals: two signals with a zero scalar product are said to be **orthogonal**. Given a complete orthonormal basis 
$$w_1(t), \; w_2(t), \; \dots, \; w_M(t)$$
any signal can be written as a weighted sum of basis functions, where each weight (or **coefficient**) is obtained by computing the scalar product of the signal with the corresponding basis function. 
$$x(t) = \sum_{i=1}^{M} \alpha_i \, w_i(t)$$
$$\alpha_i = \langle x(t), w_i(t) \rangle = \int_{-\infty}^{\infty} x(t)\, w_i^*(t)\, dt$$
$$\mathbf{x} = (\alpha_1, \alpha_2, \ldots, \alpha_M)$$

This decomposition allows signals to be represented as vectors of coefficients, which is a powerful tool for analysis and for designing communication schemes.