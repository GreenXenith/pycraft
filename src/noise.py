# Source: https://pvigier.github.io/2018/06/13/perlin-noise-numpy.html
# I don't know how much of this works. Numpy vectorization is black magic to me.
import numpy

def perlin(shape, res):
    def f(t):
        return 6*t**5 - 15*t**4 + 10*t**3

    delta = (res[0] / shape[0], res[1] / shape[1])
    d = (shape[0] // res[0], shape[1] // res[1])
    grid = numpy.mgrid[0:res[0]:delta[0],0:res[1]:delta[1]].transpose(1, 2, 0) % 1
    # Gradients
    angles = 2*numpy.pi*numpy.random.rand(res[0]+1, res[1]+1)
    gradients = numpy.dstack((numpy.cos(angles), numpy.sin(angles)))
    g00 = gradients[0:-1,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g10 = gradients[1:,0:-1].repeat(d[0], 0).repeat(d[1], 1)
    g01 = gradients[0:-1,1:].repeat(d[0], 0).repeat(d[1], 1)
    g11 = gradients[1:,1:].repeat(d[0], 0).repeat(d[1], 1)
    # Ramps
    n00 = numpy.sum(grid * g00, 2)
    n10 = numpy.sum(numpy.dstack((grid[:,:,0]-1, grid[:,:,1])) * g10, 2)
    n01 = numpy.sum(numpy.dstack((grid[:,:,0], grid[:,:,1]-1)) * g01, 2)
    n11 = numpy.sum(numpy.dstack((grid[:,:,0]-1, grid[:,:,1]-1)) * g11, 2)
    # Interpolation
    t = f(grid)
    n0 = n00*(1-t[:,:,0]) + t[:,:,0]*n10
    n1 = n01*(1-t[:,:,0]) + t[:,:,0]*n11
    return numpy.sqrt(2)*((1-t[:,:,1])*n0 + t[:,:,1]*n1)
