`Lastest update:` [Dec 18] Uploaded code, Updated section 2.3

# 2022 Fall QO Research Notes
We explore the properties of states undetected by $\lbrace W \rbrace$ and look for a method to choose the correct triplet with higher success rate. For the density matrices, see `Data` and `Data/README.md`. For more background information see `Summer2022-QO-writeup`.

## 1.1 Density matrices
We did not find significant patterns in the density matrices of the states undetected by $\lbrace W \rbrace$. Then we turned our attention to exploring the states they are closest to. Figure see `Figures/(PNG) density matrix of undetected states/`, code see `Code/exploreRho.m`.

## 1.2 Fidelity to base cases
We suggested 6 pure-state test cases, all of which are undetected by $\lbrace W \rbrace$:
$$|t_1\rangle = \frac{1}{\sqrt{2}}(|\psi^+\rangle+e^{i\alpha_1}|\psi^-\rangle)$$
$$|t_2\rangle = \frac{1}{\sqrt{2}}(|\phi^+\rangle+e^{i\alpha_2}|\phi^-\rangle)$$
$$|t_3\rangle = \frac{1}{\sqrt{2}}(|\phi^-\rangle+e^{i\alpha_3}|\psi^-\rangle)$$
$$|t_4\rangle = \frac{1}{\sqrt{2}}(|\phi^+\rangle+e^{i\alpha_4}|\psi^+\rangle)$$
$$|t_5\rangle = \frac{1}{\sqrt{2}}(|\phi^+\rangle+e^{i\alpha_5}|\psi^-\rangle)$$
$$|t_6\rangle = \frac{1}{\sqrt{2}}(|\phi^-\rangle+e^{i\alpha_6}|\psi^+\rangle)$$

The maximum fidelity of the states undetected by $\lbrace W \rbrace$ to

$$\ket{T} = \cos\theta \ket{t_i} + e^{i\beta}\sin\theta\ket{t_j}$$

where $(i,j)=(1,2)$ or $(3,4)$ or $(5,6)$ (let's call them $\ket{T_1}$, $\ket{T_2}$, and $\ket{T_3}$) is very close to the theoretical limit:

<p align="center">
  <img width="450" height="370" src="https://user-images.githubusercontent.com/105842371/198216553-4fcbd8cc-ed38-4f14-ab7c-c5400bb33ea3.png">
</p>

$\lambda_{max}$ is the theoretical limit of fidelity of a mixed state to a pure state. Matlab figure available in `Figure/maxFidToT.fig`, code see `Code/checkFid.m`.

## 1.3 Testing assumption
The min-max method could be justified if the following assuption holds: if an incoming state undetected by $\lbrace W \rbrace$ is closest to $\ket{T_i}$, it is most likely to be detected by Triplet $i$. We tested this assumption and called it the preprocessed max-fid method.

|  | min-max method | max-fid method (preprocessed) |
| :---         |     :---:      |       :---:   |
| Description  | maximize witness expressions and choose the smallest one, e.g., $\lbrace W_1, W_2\rbrace\to$ Triplet 1 | the state that has maximum fidelity of the incoming state to $\cos\theta\ket{t_i} + e^{i\beta}\sin\theta\ket{t_j}$, e.g., $\ket{T_1}\to$ Triplet 1
| Undetected states (limit = $20.67$%) | $31.62$% | $29.40$% |

The results of the max-fid method show that $\ket{T_i}$ and Triplet $i$ are not perfectly correlated. $29.40$% is probably the best we can get. Code see `Code/maxFidMethod.m`. (Note: if we choose the triplet in a completely random manner, the undetected states cover $41.73$%.)

## 1.4 Interpreting the results
We first visualized the fail-to-predict states on the fidelity plot.
<p align="center">
  <img width="350" height="280" src="https://user-images.githubusercontent.com/105842371/198401355-9a6bdb53-5b41-4fe6-95e3-d91903389cef.png">
</p>

The concurrence of the fail-to-predict states follows the same distribution.
<p align="center">
  <img width="350" height="280" src="https://user-images.githubusercontent.com/105842371/198408434-a68a0fcd-63fd-4e81-9fac-bbc02e68edbb.png">
</p>

If we take the sum of the fidelity of $\ket{t_i}$ and $\ket{t_j}$, fail-to-detect rate increases to 31.30%.
<p align="center">
  <img width="350" height="280" src="https://user-images.githubusercontent.com/105842371/200099318-7017bf7c-a71f-4169-b3a9-1f1459ab956e.png">
</p>

For all the fail-to-predict states, we check the closeness of fidelity values:
<p align="center">
  <img width="500" height="400" src="https://user-images.githubusercontent.com/105842371/200099370-a6f7692c-8032-4be3-a8ad-8e39dfc513f3.png">
</p>

## 2.1 Rotate bases
We performed basis transformation on the witness operators. In specific,
$$\text{Transformation 1: } \sigma_i \otimes \sigma_x \to \sigma_i \otimes \sigma_y, \qquad \sigma_i \otimes \sigma_y \to \sigma_i \otimes -\sigma_x, \qquad \sigma_i \otimes \sigma_z \to \sigma_i \otimes \sigma_z$$
$$\text{Transformation 2: }  \sigma_i \otimes \sigma_x \to \sigma_i \otimes \sigma_x, \qquad \sigma_i \otimes \sigma_y \to \sigma_i \otimes \sigma_z, \qquad \sigma_i \otimes \sigma_z \to -\sigma_i \otimes \sigma_y$$
$$\text{Transformation 3: } \sigma_i \otimes \sigma_x \to \sigma_i \otimes -\sigma_z, \qquad \sigma_i \otimes \sigma_y \to \sigma_i \otimes \sigma_y, \qquad \sigma_i \otimes \sigma_z \to \sigma_i \otimes \sigma_x$$
For the density matrices of the detected and undetected states after basis transformation, see `Data/Basis Rotation`.
After transformation 1, $\lbrace W \rbrace$ detects about the same number of states ( $35$% ). However, both transformation 2 and transformation 3 detect $5$% fewer states. We tested a few hypotheses in the following sections.

## 2.2 Density matrices under different bases
First we tested the explicit randomness of all density matrices. We calculate the average density matrix $\bar{\rho}$ of the 10,000 sample states in $\ket{HV}\ket{HV}$, $\ket{DA}\ket{DA}$, $\ket{RL}\ket{RL}$, $\ket{HV}\ket{DA}$, and $\ket{HV}\ket{RL}$ bases. Then we subtract $\frac{1}{4}\mathbb{I}$ from $\bar{\rho}$ and plot it in 3D.

<p align="center">
  <img width="560" height="400" src="https://user-images.githubusercontent.com/105842371/206581478-c8c6cd0f-c445-4e07-a08f-2545ab94524d.png">
</p>

We also checked the density matrices of states detected by $\lbrace W \rbrace$ in different bases before and after transformation. Similar to the figure above, the magnitude of each entry in the density matrix is around $10^{-3}$, so there is no significant imbalance. Data see `Data/basis rotation`, code see `Code/plotRho.m`.

## 2.3 Anti-correlation
Then we checked the degree of anti-correlation under several bases, hoping that as we rotated the space, the pair of bases that have the strongst anti-correlation will change. The historgram below shows the number of times that $\ket{HV}\ket{VH}$, $\ket{DA}\ket{AD}$ and $\ket{HV}\ket{VH}$ appear to be the pair that has the strongest anti-correlation for transformation 1. The distributions for transformation 2 and 3 do not make much difference.

<p align="center">
  <img width="350" height="250" src="https://user-images.githubusercontent.com/105842371/206586225-8f4eb005-92e3-4cee-80df-3cd074302b91.png">
  <img width="350" height="250" src="https://user-images.githubusercontent.com/105842371/206586306-0ff3d2cd-240a-44d1-ad8d-1f918e8bd36b.png">
</p>

Code see `Code/testAnticorrelation.m`.
