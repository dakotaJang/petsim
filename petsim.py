import pylab as pl
import numpy as np
from skimage.transform import iradon

# sample simulation setup
def sample():
    # sample set up
    xLength = 2.85
    yLength = 6.6
    xOffSet = 5.2 / 2.0
    xdensity = 100
    ydensity = 100
    x0,y0 = initPointCloud(xLength,yLength,xOffSet,xdensity, ydensity)

    # device setup
    slitWidth = 5 # width of slit that controlls the gamma rays that can go through to the detector
    d = 138 # distance between sample and the face of detector (mm)

    # experiment parameters
    dx_steps = 100   # number of steps to complete going across the detector
    dphi_steps = 100 # number of steps to complete the half rotation
    dx = 15.0 / dx_steps # increment of x for each scan
    dphi = np.pi / dphi_steps # increment of rotation after each scan through x
    emissions = 5 # number of emissions per point

    sinogram = PETscan(x0,y0,slitWidth,d,dx,dphi,emissions)
    return sinogram

# rotate point cloud by dphi
def rotatePointCloud(x0, y0, dphi):
    r = ((x0**2.0) + (y0**2.0))**0.5
    phi = np.arctan2(y0, x0)
    x = r * np.cos(phi + dphi)
    y = r * np.sin(phi + dphi)
    return x, y

# initialize mesh of two rectangular blocks of dimension of xLength and yLength separated by xOffset
def initPointCloud(xLength, yLength, xOffSet, xdensity, ydensity):
    x0 = np.zeros(xdensity * ydensity)
    y0 = np.zeros(xdensity * ydensity)
    for ii in range(xdensity):
        for jj in range(ydensity):
            x0[ii * ydensity + jj] = xOffSet + (ii * (xLength / (xdensity - 1)))
            y0[ii * ydensity + jj] = - \
                (yLength * jj / (ydensity - 1)) + (yLength / 2.0)
    x0 = np.append(-x0[::-1], x0)
    y0 = np.append(y0, y0)
    return x0, y0

# run simulation
def PETscan(x0,y0,slitWidth,d,dx,dphi,emissions):
    xRange = 15 # scan from -xRange to +xRange (mm)
    phirange = np.pi # scan the sample from front to back
    x,y = x0,y0
    sinogram = np.zeros([int(2.0 * xRange / dx) + 1, int(phirange / dphi) + 1])
    for hh in range(sinogram.shape[1]):
        # scan from -xRange and increment by dx
        x = x - xRange
        for ii in range(sinogram.shape[0]):
            count = 0
            thetaUL = np.arctan(((slitWidth / 2.0) + x) / (d - y)) + (np.pi / 2.0)
            thetaUR = np.arctan((d - y) / ((slitWidth / 2.0) - x))
            thetaDL = np.arctan((d + y) / ((slitWidth / 2.0) + x)) + np.pi
            thetaDR = np.arctan(((slitWidth / 2.0) - x) / (d + y)) + (3 * np.pi / 2)
            if ~(x.min() > slitWidth / 2.0 or x.max() < -slitWidth / 2.0):
                for jj in range(emissions):
                    theta = np.random.random(len(x)) * np.pi
                    count = count + sum((theta < thetaUL).astype(int) * (theta > thetaUR).astype(int) * (x < slitWidth / 2.0).astype(int) * (
                        x > -slitWidth / 2.0).astype(int) * (theta + np.pi > thetaDL).astype(int) * (theta + np.pi < thetaDR).astype(int))
            sinogram[ii, hh] = count
            x = x + dx
            print("phi_progress = %f,x_progress = %f" % (100.0 * hh / sinogram.shape[1], 100.0 * ii / sinogram.shape[0]))
        x, y = rotatePointCloud(x0, y0, dphi * (hh + 1))
    print("phi_progress = 100,x_progress = 100")
    showResult(sinogram)
    return sinogram

# show plots
def showResult(sinogram):
    recon=iradon(sinogram,theta=np.linspace(0,180,sinogram.shape[1]))
    pl.figure()
    pl.imshow(sinogram, aspect='auto')
    pl.figure()
    pl.imshow(recon, aspect='auto')
    pl.show()