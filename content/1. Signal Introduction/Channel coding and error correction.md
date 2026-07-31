After [[Source coding and data compression#Source coding|source coding]] has reduced the data to a compact representation, the resulting bit sequence must be transmitted reliably over a channel that is inherently imperfect. Noise, interference, and fading can all flip bits during transmission, so the received sequence may differ from what was sent. Channel coding is the set of techniques used to detect and correct these errors, ensuring that the original data can be recovered at the receiver despite channel impairments.

## The error control problem
The fundamental goal of channel coding is reliable delivery of digital data over unreliable communication channels. Once source coding has been applied, every bit in the resulting sequence carries useful information, so any undetected bit error directly corrupts the reconstructed source data. Channel coding addresses this by adding controlled redundancy to the transmitted message: extra bits that carry no new information but whose values are determined by the information bits according to a known rule. The receiver uses this structure to detect inconsistencies in the received sequence and, where the code permits, to identify and correct the corrupted bits.

The redundancy added by channel coding increases the number of bits that must be transmitted, consuming bandwidth and power. There is therefore a fundamental **trade-off** between the level of error protection provided and the bandwidth efficiency of the system. A code that corrects many errors requires a large amount of redundancy; a code that adds little redundancy offers weaker protection. The design of a channel code is a matter of choosing the appropriate point on this trade-off for the requirements of the application.

### Approaches to error control
Two broad approaches exist for dealing with transmission errors.
- **Automatic Repeat reQuest** (*ARQ*) relies on feedback from the receiver to the transmitter. The receiver checks each received block of data for errors using a detection code. If an error is detected, the receiver sends a negative acknowledgement and the transmitter retransmits the affected block. If no error is detected, the receiver sends a positive acknowledgement and transmission proceeds. ARQ requires a backward channel from receiver to transmitter and introduces latency due to retransmission. The main variants are *Stop-and-Wait ARQ*, *Go-Back-N ARQ*, and *Selective Repeat ARQ*, which differ in how many frames can be outstanding simultaneously and how retransmissions are managed.
  ![[Pasted image 20260314184835.png|509]]

- **Forward Error Correction** (*FEC*), also called channel coding in the narrow sense, takes a different approach: the transmitter adds enough redundancy that the receiver can correct errors entirely on its own, without requesting retransmission. Because no backward channel is required, FEC is applicable in unidirectional communication scenarios such as broadcast, satellite links, and deep-space communications where a return path is unavailable or has prohibitively long round-trip delays. The two principal families of FEC codes are block codes and convolutional codes.
  ![[Pasted image 20260314184935.png|499]]

## Channel coding: general principles

Channel coding operates by mapping each block or stream of $k$ information bits to a longer sequence of $n$ coded bits, where $n > k$. The ratio $R = k/n$ is called the code rate and quantifies the fraction of the transmitted bits that carry information. A code rate of $R = 1/2$, for example, means that half the transmitted bits are redundancy. The additional $n - k$ bits are called parity bits or check bits, and their values are computed as a deterministic function of the $k$ information bits.

The effectiveness of a channel code is characterised by its error correction capability, which specifies the maximum number of bit errors within a single codeword that the decoder can correct with certainty. This capability is determined by the minimum Hamming distance $d_{\min}$ of the code, defined as the smallest number of bit positions in which any two valid codewords differ. A code with minimum distance $d_{\min}$ can detect up to $d_{\min} - 1$ errors and correct up to $\lfloor (d_{\min} - 1)/2 \rfloor$ errors per codeword.

Channel coding is used across virtually all modern communication systems, including wireless networks, satellite links, digital television, optical fibre systems, and data storage devices such as solid-state drives and optical discs.

## Block codes

A block code processes the input data as a sequence of fixed-size blocks. Each block of $k$ information bits is independently encoded into a codeword of $n$ bits, giving an $(n, k)$ block code. The encoder applies a fixed mapping from the $2^k$ possible input blocks to $2^k$ selected codewords out of the $2^n$ possible $n$-bit sequences. The remaining $2^n - 2^k$ sequences are not valid codewords; if the receiver observes one of them, it knows that at least one error has occurred.

![[Pasted image 20260314190327.png]]

Linear block codes are the most important subclass. In a linear block code, any linear combination (bitwise XOR) of two valid codewords is itself a valid codeword. This linearity property greatly simplifies both the encoding and decoding operations. Well-known linear block codes include Hamming codes, Reed-Solomon codes, Reed-Muller codes, Hadamard codes, Golay codes, and expander codes. Reed-Solomon codes are particularly widely deployed because they operate over symbols rather than individual bits, making them effective against burst errors, and they are used in applications ranging from CD and DVD error correction to deep-space communications.

![[Pasted image 20260314190249.png]]
A simple but instructive example is the repetition code, in which each information bit is repeated $n$ times. For $n = 3$, the codewords are $000$ for a $0$ bit and $111$ for a $1$ bit, giving a $(3,1)$ code with rate $R = 1/3$. The decoder applies a majority vote: it outputs the bit value that appears most frequently in the received codeword. This code can correct any single bit error per codeword ($d_{\min} = 3$, so $\lfloor 2/2 \rfloor = 1$ correctable error), at the cost of tripling the number of transmitted bits.

## Convolutional codes

Convolutional codes differ from block codes in that they process the input data as a continuous stream rather than as independent fixed-size blocks. The encoder maintains a shift register of memory length $m$ and computes each output bit as a linear function (specifically, a convolution) of the current input bit and the $m$ most recently input bits. Because the output at any given time depends on a window of past inputs, errors in one part of the stream are spread across the decoded output, and the decoder can exploit this structure to correct them.

The optimal decoding algorithm for convolutional codes is the Viterbi algorithm, which performs maximum likelihood sequence detection by efficiently searching the trellis of all possible encoder state sequences. The Viterbi algorithm has complexity that is linear in the length of the input sequence and exponential in the memory length $m$, making it practical for moderate values of $m$. Convolutional codes are widely used in applications that require low-latency decoding of continuous data streams, including mobile telephony and satellite communications.