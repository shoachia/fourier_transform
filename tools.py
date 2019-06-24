
import numpy as np

def shift(x, k, l, boundary):
    if x.ndim == 2:
        color = 1
    else :
        color = 3
    n1 = np.shape(x)[0]
    n2 = np.shape(x)[1]
    xshifted = np.zeros((n1,n2,color))
    irange = np.mod(np.arange(n1) + k, n1)
    jrange = np.mod(np.arange(n2) + l, n2)
    # firstly move upward then move rightward
    xshifted = x[irange, :][:, jrange]
    if boundary == 'periodical':
        pass
    elif boundary is 'extension':
        m = n1 - k if k > 0 else -k-1
        n = n2 - l if l > 0 else -l-1
        if k != 0:
            xshifted[m::np.sign(k),:,:] = np.tile(xshifted[m-np.sign(k):m-np.sign(k)+1,:,:],(np.sign(k)*k,1,1))
        if l != 0:
            xshifted[:,n::np.sign(l),:] = np.tile(xshifted[:,n-np.sign(l):n-np.sign(l)+1,:],(1,np.sign(l)*l,1))
    elif boundary == 'zero-padding':
        period = xshifted
        xshifted = np.zeros_like(period)
        m = n1 - k if k > 0 else -k-1
        n = n2 - l if l > 0 else -l-1  
        sign_k = np.sign(k) if k != 0 else 1 
        sign_l = np.sign(l) if l != 0 else 1
        if k == 0:
            m = n1
        if l == 0:
            n = n2
        if color == 3:
            xshifted[:m:sign_k,:n:sign_l,:] = period[:m:sign_k,:n:sign_l,:]
        else:
            xshifted[:m:sign_k,:n:sign_l] = period[:m:sign_k,:n:sign_l]
    # mirror
    else:
        m = n1 - k if k > 0 else -k
        n = n2 - l if l > 0 else -l
        add_k = 1 if k < 0 else 0
        add_l = 1 if l < 0 else 0
        if color == 3:
            if k != 0:
                xshifted[m::np.sign(k),:,:] = xshifted[min(m,m-k):max(m,m-k) + add_k,:,:][::-np.sign(k),:,:]
            if l != 0:
                xshifted[:,n::np.sign(l),:] = xshifted[:,min(n,n-l):max(n,n-l) + add_l ,:][:,::-np.sign(l),:]
        else:
            if k != 0:
                xshifted[m::np.sign(k),:] = xshifted[min(m,m-k):max(m,m-k) + add_k,:][::-np.sign(k),:]
            if l != 0:
                xshifted[:,n::np.sign(l)] = xshifted[:,min(n,n-l):max(n,n-l) + add_l][:,::-np.sign(l)]
            
    return xshifted

def convolve(x, nu, boundary= 'periodical'):
    xconv = np.zeros(x.shape)
    s1 = int((nu.shape[0] - 1) / 2)
    s2 = int((nu.shape[1] - 1) / 2)
    for k in range(-s1, s1+1):
        for l in range(-s2, s2+1):
            xconv += nu[k+s1,l+s2]*shift(x,-k,-l,boundary)
    return xconv

def kernel(name, tau=1, eps=1e-3):
    if name == 'gaussian':
        s1 = 0
        while True:
            if np.exp(-(s1**2)/(2*tau)) < eps:
                break
            s1 += 1
        s1 = s1-1
        s2 = s1
        i = np.arange(-s1,s1+1) #-3 ~ 3
        j = np.arange(-s2,s2+1) #-3 ~ 3 
        ii, jj = np.meshgrid(i, j, sparse=True,indexing='ij')
        nu = np.exp(-(ii**2 + jj**2) / (2*tau**2))
        nu[nu < eps] = 0
        nu /= nu.sum()
    elif name == 'exponential':
        if tau == 0:
            s1 = 1
            s2 =1
        else:
            s1 = 0
            while True:
                if np.exp(-(s1)/(tau)) < eps:
                    break
                s1 += 1
            s1 = s1-1
            s2 = s1
            
        i = np.arange(-s1,s1+1) #-20 ~ 20
        j = np.arange(-s2,s2+1) #-20 ~ 20
        ii, jj = np.meshgrid(i, j, sparse=True,indexing='ij')
        if tau == 0: 
            tau = 1e-3
        nu = np.exp(-(np.sqrt(ii**2+jj**2))/tau)
        nu[nu < eps] = 0
        nu /= nu.sum()
    elif name.startswith('box'):
        if name.endswith('1'):
            nu = np.zeros((2*tau+1, 1))
            nu[:,0] = 1/(2*tau+1)
        elif name.endswith('2'):
            nu = np.zeros((1, 2*tau+1))
            nu[0,:] = 1/(2*tau+1)
        else:
            s1 = tau
            s2 = tau
            i = np.arange(-s1,s1+1) #-1 ~ 1
            j = np.arange(-s2,s2+1) #-1 ~ 1
            ii, jj = np.meshgrid(i, j, sparse=True,indexing='ij')
            nu = np.exp(0*(ii+jj))
            nu[nu < eps] = 0
            nu /= nu.sum()
    elif name == 'motion':
        nu = np.load('motionblur.npy')
    elif name.endswith('forward'):
        if name.startswith('1',4,5):
            nu = np.zeros((3, 1))
            nu[1, 0] = 1
            nu[2, 0] = -1
        elif name.startswith('2',4,5):
            nu = np.zeros((1, 3))
            nu[0, 1] = 1
            nu[0, 2] = -1
        else:
            raise ValueError('invalid kernel')
    elif name.endswith('backward'):
        if name.startswith('1',4,5):
            nu = np.zeros((3, 1))
            nu[0, 0] = 1
            nu[1, 0] = -1
        elif name.startswith('2',4,5):
            nu = np.zeros((1, 3))
            nu[0, 0] = 1
            nu[0, 1] = -1
        else: 
            raise ValueError('invalid kernel')
    elif name.startswith('laplacian'):
        if name.endswith('1'):
            nu = np.zeros((3, 1))
            nu[0, 0] = 1
            nu[1, 0] = -2
            nu[2, 0] = 1 
        elif name.endswith('2'):
            nu = np.zeros((1, 3))
            nu[0, 0] = 1
            nu[0, 1] = -2
            nu[0, 2] = 1
        else: 
            raise ValueError('invalid kernel')
    else:
        raise ValueError('invalid kernel')
    return nu
