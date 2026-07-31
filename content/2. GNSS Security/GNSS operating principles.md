## Positioning through multilateration
GNSS positioning relies on a technique called **multilateration**, which determines the location of a receiver by measuring its distance from multiple satellites whose positions are known. Each satellite continuously transmits a signal that contains two pieces of information: the satellite's own position and the time at which the signal was sent, denoted $T_{TX}$. When the receiver captures the signal, it records the time of arrival $T_{RX}$ and computes the distance to that satellite as:

$$R = (T_{TX} - T_{RX}) \cdot c$$

where $c$ is the speed of light. This distance is called a **range**, and it places the receiver somewhere on the surface of a sphere centered on the satellite with radius $R$.
![[Pasted image 20260316163306.png|418]]
With only one satellite, the receiver could be anywhere on that sphere. With two satellites, the two spheres intersect along a circle, reducing the possible locations to that ring. Adding a third satellite narrows the intersection to two discrete points. In practice, one of these two points is usually physically implausible (for example, deep underground or far from Earth), so it can be discarded. In principle, three ranges are sufficient to compute a 3D position through multilateration. However, a practical complication requires a fourth satellite.

## Functional basics and pseudorange
The distance computation assumes that the clocks of the satellite and the receiver are perfectly synchronized. In reality, this is not the case. Satellites carry high-quality **atomic clocks** that are kept closely aligned with a common reference called the **GNSS time scale** through a network of ground control stations. Any residual offset of the satellite clock from this reference, denoted $\delta t^S$, is small, stable, and continuously monitored by the [[GNSS architecture#Control segment|control segment]], which broadcasts corrections. This offset can therefore be treated as effectively zero.

The receiver, on the other hand, uses a low-cost clock that is not synchronized with the GNSS time scale. This introduces an unknown **user clock bias** $\delta t_u$. Because the receiver uses its own biased clock to record the arrival time $T_{RX}$, the computed distance is not the true geometric range but an erroneous value inflated by the clock offset. This corrupted distance is called a **pseudorange** and is expressed as:

$$\rho = c \cdot \tau + c \cdot \delta t_u$$

where $\tau$ is the true time of flight of the signal. The term $c \cdot \delta t_u$ is the **clock bias expressed in distance units**, often written as $b_{ut}$. The pseudorange is what the receiver actually measures; it differs from the true range by this bias term.

## The pseudorange equation
For each visible satellite $j$ at known position $(x_j, y_j, z_j)$, the pseudorange equation relates the measurement to the unknown user position $(x_u, y_u, z_u)$ and the unknown clock bias $b_{ut}$:

$$\rho_j = \sqrt{(x_j - x_u)^2 + (y_j - y_u)^2 + (z_j - z_u)^2} + b_{ut}$$

In this equation, the satellite position is **known** because it is derived from orbital data broadcast by the satellite itself. The pseudorange $\rho_j$ is **measured** directly by the receiver. The user position and the clock bias are both **unknown**. This gives a system with four unknowns: the three spatial coordinates $x_u$, $y_u$, $z_u$ and the scalar bias $b_{ut}$. To solve for four unknowns, at least four independent equations are needed, which means a minimum of **four satellites** must be in view simultaneously. This is why GNSS requires four satellites rather than the three that pure geometric multilateration would suggest.
![[GNSS-4th-satellite.png]]
## The navigation solution
The pseudorange equation is nonlinear because the unknowns appear inside a square root. To make it tractable, it is **linearized using a first-order Taylor expansion** around an approximate known position $(\hat{x}_u, \hat{y}_u, \hat{z}_u, \hat{b}_{ut})$. The approximated pseudorange from this initial guess to satellite $j$ is:

$$\hat{\rho}_j = \sqrt{(x_j - \hat{x}_u)^2 + (y_j - \hat{y}_u)^2 + (z_j - \hat{z}_u)^2} + \hat{b}_{ut}$$

The difference between the measured pseudorange and this approximated value is:

$$\Delta\rho_j = \rho_j - \hat{\rho}_j$$

At first order, this residual can be written as a linear combination of the corrections to the approximate position:

$$\Delta\rho_j = a_{xj}\Delta x_u + a_{yj}\Delta y_u + a_{zj}\Delta z_u - \Delta b_{ut}$$

where $\Delta x_u = x_u - \hat{x}_u$, $\Delta y_u = y_u - \hat{y}_u$, $\Delta z_u = z_u - \hat{z}_u$, and $\Delta b_{ut} = b_{ut} - \hat{b}_{ut}$ are the corrections to be estimated. The coefficients $a_{xj}$, $a_{yj}$, $a_{zj}$ are the components of the **unit vector pointing from the approximation point toward satellite $j$**:

$$a_{xj} = \frac{x_j - \hat{x}_u}{\hat{r}_j}, \quad a_{yj} = \frac{y_j - \hat{y}_u}{\hat{r}_j}, \quad a_{zj} = \frac{z_j - \hat{z}_u}{\hat{r}_j}$$

where $\hat{r}_j$ is the geometric distance between the linearization point and satellite $j$:

$$\hat{r}_j = \sqrt{(x_j - \hat{x}_u)^2 + (y_j - \hat{y}_u)^2 + (z_j - \hat{z}_u)^2}$$

Writing one such equation for each satellite and collecting them into matrix form gives:

$$\Delta\boldsymbol{\rho} = \mathbf{H} \Delta\mathbf{x}$$

where $\Delta\boldsymbol{\rho}$ is the vector of pseudorange residuals, $\Delta\mathbf{x}$ is the vector of corrections to be estimated, and $\mathbf{H}$ is the **geometry matrix**, whose rows contain the unit vector components for each satellite plus a column of ones for the clock bias term.

### The least squares solution
When exactly four satellites are available, $\mathbf{H}$ is a square $4 \times 4$ matrix and, provided it is invertible, the solution is simply:

$$\Delta\mathbf{x} = \mathbf{H}^{-1} \Delta\boldsymbol{\rho}$$

In practice, modern receivers track many more than four satellites simultaneously, taking advantage of multiple constellations (such as [[GNSS architecture#^2054bc|GPS]], [[GNSS architecture#^55c69f|Galileo]], [[GNSS architecture#^8a0ef4|GLONASS]], and [[GNSS architecture#^14402b|BeiDou]]) and multiple frequency bands. When more than four satellites are in view, the system is **overdetermined**: there are more equations than unknowns, and $\mathbf{H}$ is no longer square. In this case the standard approach is the **least squares solution**, which minimizes the sum of squared residuals:

$$\Delta\mathbf{x} = \left(\mathbf{H}^T \mathbf{H}\right)^{-1} \mathbf{H}^T \Delta\boldsymbol{\rho}$$

This solution exists as long as $\mathbf{H}^T \mathbf{H}$ is non-singular, a condition that is satisfied when the satellites are not all clustered in the same region of the sky. The expression $(\mathbf{H}^T \mathbf{H})^{-1} \mathbf{H}^T$ is the **Moore-Penrose pseudoinverse** of $\mathbf{H}$ and yields the best linear unbiased estimate of the position correction under standard assumptions.

Because the linearization is only an approximation, the process is applied **iteratively**: the estimated correction $\Delta\mathbf{x}$ is added to the current approximation point, and the linearization is repeated from the updated position until the corrections become negligibly small. Alternatively, advanced receivers may use a **Kalman filter** or other Bayesian estimation methods, which are particularly well suited to dynamic scenarios where the user is moving and position estimates must be updated continuously over time.

## Positioning errors

The pseudorange equation introduced assumes that the only unknown beyond the user position is the clock bias. In practice, every pseudorange measurement is also affected by a residual error term $\epsilon$, so the full equation becomes:

$$\rho_j = \sqrt{(x_j - x_u)^2 + (y_j - y_u)^2 + (z_j - z_u)^2} + b_{ut} + \epsilon$$

This error term aggregates contributions from multiple sources, which are described in detail below. Because the positioning solution is computed from pseudorange measurements, any error in those measurements propagates directly into an error in the estimated position.

When measurement errors are present, the linearized system becomes:

$$\Delta\boldsymbol{\rho} + \delta\boldsymbol{\rho} = \mathbf{H}(\Delta\mathbf{x} + \delta\mathbf{x})$$

where $\delta\boldsymbol{\rho}$ is the vector of pseudorange measurement errors and $\delta\mathbf{x}$ is the resulting error in the estimated position and clock bias. Applying the least squares framework to this noisy system yields:

$$\delta\mathbf{x} = \left(\mathbf{H}^T\mathbf{H}\right)^{-1}\mathbf{H}^T , \delta\boldsymbol{\rho}$$

This expression makes the structure of the positioning error explicit: the error in the solution is the product of a factor that depends only on the **satellite geometry**, captured by the matrix $(\mathbf{H}^T\mathbf{H})^{-1}\mathbf{H}^T$, and a factor that depends on the **magnitude of the pseudorange errors**, captured by $\delta\boldsymbol{\rho}$. These two contributions are independent of each other and can therefore be analyzed separately.

## Sources of pseudorange error

The total pseudorange error $\epsilon$ is the sum of several physical contributions that arise at different points along the signal path from satellite to receiver.

- **Satellite clock offset** is the residual misalignment between the satellite clock and the GNSS time scale after corrections have been applied. Although the control segment monitors and corrects this offset, any unmodeled residual translates directly into a range error. The equivalent distance error can reach up to hundreds of kilometers if uncorrected, though in normal operation it is kept to negligible levels.

- **Relativistic clock correction** arises because the atomic clocks on board the satellites run at a slightly different rate than clocks on the ground, due to the combined effects of special and general relativity. The satellites move fast and are located at high altitude, both of which affect the clock rate. The uncorrected effect corresponds to an equivalent range error of up to approximately 13 meters and must be accounted for in the signal processing.

- **Satellite instrumental delays** are hardware-dependent timing biases introduced by the electronic components inside the satellite's signal generation chain. These delays are on the order of meters in equivalent range and are typically estimated and broadcast as part of the navigation message.

- **Ionospheric delay** is caused by the dispersive effect of the ionosphere, the ionized upper layer of the atmosphere, on the GNSS signal. The free electrons in this layer slow the signal's propagation, adding an extra apparent path length that depends on the frequency of the signal and the total electron content along the path. The equivalent range error is typically between 2 and 50 meters. Because the ionospheric delay is frequency-dependent, receivers that track signals on two or more frequencies can largely eliminate this effect by combining measurements.

- **Tropospheric delay** is caused by the neutral lower atmosphere. Unlike the ionosphere, the troposphere is non-dispersive, meaning the delay does not depend on frequency. It depends instead on temperature, pressure, and humidity along the signal path. The equivalent range error is also in the range of 2 to 50 meters and is commonly mitigated using empirical atmospheric models.

- **Receiver clock offset** is the bias of the user's local clock with respect to the GNSS time scale. As discussed earlier, this is treated as an explicit unknown in the positioning problem rather than a correctable error, but any residual after estimation contributes to the final position error. The uncorrected equivalent range error can be as large as hundreds of kilometers, underlining why accurate clock modeling is critical.

- **Receiver instrumental delays** are analogous to satellite instrumental delays but occur in the receiver hardware. They are on the order of meters and may be estimated through calibration.

- **Multipath effects** occur when the GNSS signal reaches the receiver via one or more reflected paths in addition to the direct line-of-sight path. Reflections from buildings, terrain, or other surfaces cause the receiver to track a superposition of signals, distorting the pseudorange measurement. Multipath is particularly severe in urban environments and is one of the hardest error sources to model or correct because it depends strongly on the local geometry.

The aggregate of all these contributions, after predictable components have been removed through corrections and models, is quantified as the **User Equivalent Range Error (UERE)**. The UERE is the standard deviation $\sigma_\text{UERE}$ of the residual pseudorange error and serves as the baseline noise figure for assessing positioning accuracy.

## Dilution of precision

Even with a fixed pseudorange error level, the accuracy of the position solution depends on how the visible satellites are distributed across the sky. This geometric dependence is captured by a scalar quantity called the **Dilution of Precision (DOP)**. The overall positioning error, expressed as a standard deviation over all four estimated unknowns (three spatial coordinates plus clock bias), is:

$$\sigma_x = \sqrt{\sigma_{x_u}^2 + \sigma_{y_u}^2 + \sigma_{z_u}^2 + \sigma_{b_{ut}}^2} = \text{GDOP} \cdot \sigma_\text{UERE}$$

The **Geometric Dilution of Precision (GDOP)** is defined as:

$$\text{GDOP} = \sqrt{\text{tr}{(\mathbf{H}^T\mathbf{H})^{-1}}}$$

where $\text{tr}{\cdot}$ denotes the trace of the matrix. Since $\mathbf{H}$ depends only on the directions from the receiver to the satellites, GDOP is a purely geometric quantity. A **low GDOP** value means the satellites are well spread across the sky, so their combined ranging information tightly constrains the position estimate. A **high GDOP** value means the satellites are clustered in a narrow region of the sky, which produces a poorly conditioned geometry and amplifies pseudorange errors into large position errors.

This situation is common in dense urban environments, often referred to as **urban canyons**, where tall buildings block large portions of the sky and only satellites visible from a limited angular sector can be tracked. In such conditions the satellite geometry is unfavorable even when the signals themselves are strong.

Several specialized DOP variants are used in practice depending on which coordinates are of interest. **HDOP** (Horizontal DOP) quantifies the geometric amplification affecting only the horizontal plane, which is most relevant for ground navigation. **PDOP** (Position DOP) considers only the three spatial coordinates, excluding the clock component, and is the most commonly reported DOP figure for evaluating three-dimensional positioning quality.

## GNSS security threats

The pseudorange error model described above covers unintentional sources of degradation. However, because GNSS signals are radio frequency transmissions received from satellites at very low power levels, they are inherently vulnerable to intentional interference. Two primary attack categories are recognized: **jamming** and **spoofing**.

**Jamming** is a denial-of-service attack in which an adversary transmits a high-power radio frequency signal in the GNSS frequency band with the intent of overwhelming the legitimate satellite signals at the receiver. Because GNSS signals arrive at the Earth's surface extremely weak, having traveled approximately 20,000 km from medium Earth orbit, a relatively low-power jammer in proximity to the target receiver is sufficient to raise the noise floor to a level at which the receiver can no longer acquire or track any satellite. The result is a complete loss of positioning capability. Jamming does not require knowledge of the GNSS signal structure and is therefore technically straightforward, which makes it a common and serious threat to GNSS-dependent systems.

**Spoofing** is a more sophisticated attack in which an adversary generates counterfeit GNSS signals that mimic the structure of legitimate satellite transmissions. The receiver, unable to distinguish the fake signals from real ones, locks onto the spoofed signals and computes a position that the attacker controls. Unlike jamming, spoofing does not necessarily prevent the receiver from producing a position fix; instead, it silently corrupts the output, potentially directing a target to a wrong location or manipulating a timing receiver without triggering any obvious alarm. Spoofing therefore poses a qualitatively different and in many contexts more dangerous threat than jamming, particularly for safety-critical or security-critical applications.