# Spectral Convolution
### Spectral Analysis
1. Horizontal sinsoidal : 

<img src="https://i.imgur.com/ymlgpKf.png" width="400">
We can see there is only two points in the frequency domain, which means that there are only one frequency in the horizontal direction and DC in vetical direction.
2. Vertical sinsoidal:

<img src="https://i.imgur.com/diQ7hlZ.png" width="400">
Vice versa.
3. What will changed in the frequency domain when we down-sampling the image?
<img src="https://i.imgur.com/tEc95nv.png" width="300">
<img src="https://i.imgur.com/OZYJluX.png" width="300">
<img src="https://i.imgur.com/s6lTMHR.png" width="300">


The adjacent frequency signals have been merge into same frequency as the sub-sampling by larger factor

### 2. Spectral Convolution
According to the convolution theorm 
![](https://i.imgur.com/nqnXUUZ.png)

we can perform the convolution in frequnecy domain.

* The time complexity of convolution in spatial domain is **O(NNKK)** where N is side length of the image. K is side length of kernel.
* Since the complexity of DFT is **O(NlogN)**, so the complexity of the convolution in frequency domain is
**O(NlogN) + O(NlogN) + O(N^2) + O(NlogN) = O(N^2 + 3NlogN)**
As N --> infinity, the complexity becomes **O(N^2)** which is much faster than convolution in spatial domain

<img src="https://i.imgur.com/V80x24W.png" width="300"><img src="https://i.imgur.com/ZuFkjnN.png" width="300">

### 3. Adjoint
Deriving the adjoint kernel of convolution operator.

<div align=left><img src="https://i.imgur.com/3jOHOIZ.png"> 



