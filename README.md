# Spectral Convolution
### Spectral Analysis
1. Horizontal sinsoidal : 
![test image size](https://i.imgur.com/ymlgpKf.png){:height="400px" width="400px"}
We can see there is only two points in the frequency domain, which means that there are only one frequency in the horizontal direction and DC in vetical direction.
2. Vertical sinsoidal:
![test image size](https://i.imgur.com/diQ7hlZ.png){:height="400px" width="400px"}
Vice versa.
3. What will changed in the frequency domain when we down-sampling the image?
![test image size](https://i.imgur.com/tEc95nv.png){:height="300px" width="300px"}
![test image size](https://i.imgur.com/OZYJluX.png){:height="300px" width="300px"}
![test image size](https://i.imgur.com/s6lTMHR.png){:height="300px" width="300px"}


The adjacent frequency signals have been merge into same frequency as the sub-sampling by larger factor

### 2. Spectral Convolution
According to the convolution theorm 
![](https://i.imgur.com/nqnXUUZ.png)

we can perform the convolution in frequnecy domain.

* The time complexity of convolution in spatial domain is **O(NNKK)** where N is side length of the image. K is side length of kernel.
* Since the complexity of DFT is **O(NlogN)**, so the complexity of the convolution in frequency domain is
**O(NlogN) + O(NlogN) + O(N^2) + O(NlogN) = O(N^2 + 3NlogN)**
As N --> infinity, the complexity becomes **O(N^2)** which is much faster than convolution in spatial domain
![test image size](https://i.imgur.com/V80x24W.png){:height="300px" width="300px"}![test image size](https://i.imgur.com/ZuFkjnN.png){:height="300px" width="300px"}
### 3. Adjoint
Deriving the adjoint kernel of convolution operator.
![](https://i.imgur.com/3jOHOIZ.png)



