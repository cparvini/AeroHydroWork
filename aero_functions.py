# -*- coding: utf-8 -*-
"""
Created on Fri Feb 06 22:27:25 2015

@title: Aero-Hydro Useful Functions
@author: Cameron Parvini
"""
import numpy

class Source:
    """Contains information related to a source (or sink)."""
    def __init__(self, strength, x, y):
        """Initializes the singularity.
        
        Arguments
        ---------
        strength -- strength of the singularity.
        x, y -- coordinates of the singularity.
        """
        self.strength = strength
        self.x, self.y = x, y
    
    def velocity(self, X, Y):
        """Computes the velocity field generated by the singularity.
        
        Arguments
        ---------
        X, Y -- 2D matrix of float; mesh grid.
        """
        self.u = self.strength/(2*numpy.pi)*(X-self.x)/((X-self.x)**2+(Y-self.y)**2)
        self.v = self.strength/(2*numpy.pi)*(Y-self.y)/((X-self.x)**2+(Y-self.y)**2)
    
    def stream_function(self, X, Y):
        """Computes the stream-function generated by the singularity.
        
        Arguments
        ---------
        X, Y -- 2D matrix of float; mesh grid.
        """
        self.psi = self.strength/(2*numpy.pi)*numpy.arctan2((Y-self.y), (X-self.x))

class Vortex:
    """Contains information related to a vortex."""
    def __init__(self, strength, x, y):
        """Initializes the vortex.
        
        Arguments
        ---------
        strength -- float; strength of the vortex.
        x, y -- float; coordinates of the vortex.
        """
        self.strength = strength
        self.x, self.y = x, y
        
    def velocity(self, X, Y):
        """Computes the velocity field generated by a vortex.
        
        Arguments
        ---------
        X, Y -- 2D matrix of float; mesh grid.
        """
        self.u = +self.strength/(2*numpy.pi)*(Y-self.y)/((X-self.x)**2+(Y-self.y)**2)
        self.v = -self.strength/(2*numpy.pi)*(X-self.x)/((X-self.x)**2+(Y-self.y)**2)
        
    def stream_function(self, X, Y):
        """Computes the stream-function generated by a vortex.
        
        Arguments
        ---------
        X, Y -- 2D matrix of float; mesh grid.
        """
        self.psi = -self.strength/(4*numpy.pi)*numpy.log((X-self.x)**2+(Y-self.y)**2)

def create_grid(N,x_start,x_end,y_start,y_end):
    """Creates a 2D meshgrid based on input values.
    
    Arguments
    ---------
    N -- int; number of gridpoints.
    x_start,x_end -- float; x-direction boundaries for the grid.
    y_start,y_end -- float; y-direction boundaries for the grid.
    
    Output
    ---------
    X, Y -- 2D matrix of float; meshgrids of x and y coordinates.
    """
    
    x = numpy.linspace(x_start, x_end, N)
    y = numpy.linspace(y_start, y_end, N)
    X, Y = numpy.meshgrid(x,y)
    
    return X, Y
    
def get_freestream_info(u_inf, alpha, X, Y, N):
    """Returns the cartesian velocities and stream-function
    generated by a freestream.
    
    Arguments
    ---------
    u_inf -- float; freestream velocity.
    alpha -- float; freestream angle of attack.
    Y -- 2D matrix of float; mesh grid of y values.
    N -- int; number of discrete points in each direction on our grid.
    
    Output
    ---------
    u, v -- 2D matrix of float; cartesian velocities of the vortex.
    psi -- 2D matrix of float; stream-function on a grid.
    """
    
    u = u_inf * numpy.cos(alpha) * numpy.ones((N, N), dtype=float)
    v = u_inf * numpy.sin(alpha) * numpy.zeros((N, N), dtype=float)
    psi = u_inf * (Y * numpy.cos(alpha) - X * numpy.sin(alpha))
    
    return u, v, psi
    
def get_vortex_info(strength, xv, yv, X, Y):
    """Returns the cartesian velocities and stream-function
    generated by a vortex.
    
    Arguments
    ---------
    strength -- float; strength of the vortex.
    xv, yv -- float; coordinates of the vortex.
    X, Y -- 2D matrix of float; mesh grid.
    
    Output
    ---------
    u, v -- 2D matrix of float; cartesian velocities of the vortex.
    psi -- 2D matrix of float; potential values on a grid.    
    """
    u = + strength/(2*numpy.pi)*(Y-yv)/((X-xv)**2+(Y-yv)**2)
    v = - strength/(2*numpy.pi)*(X-xv)/((X-xv)**2+(Y-yv)**2)
    psi = strength/(4*numpy.pi)*numpy.log(numpy.sqrt((X-xv)**2+(Y-yv)**2))

    return u, v, psi
    
def get_velocity_infinite_vortices(gamma, X, Y, x_vortices):
    """Returns the cartesian velocities of an infinite row of vortices.
    
    Arguments
    ---------
    gamma -- float; freestream velocity.
    Y -- 2D matrix of float; mesh grid of y values.
    N -- int; number of discrete points in each direction on our grid.
    
    Output
    ---------
    u, v -- 2D matrix of float; cartesian velocities of the vortex.
    """    
    
    a = x_vortices[1]-x_vortices[0]
    c = 2*numpy.pi/a
    
    u = + (gamma/(2*a))*((numpy.sinh(c*Y))/(numpy.cosh(c*Y) - numpy.cos(c*X)))
    v = - (gamma/(2*a))*((numpy.sin(c*X))/(numpy.cosh(c*Y) - numpy.cos(c*X)))
    
    return u, v
    
def get_ss_info(strength, xs, ys, X, Y):
    """Returns the cartesian velocities and stream-function 
    generated by a source/sink.
    
    Arguments
    ---------
    strength -- float; strength of the source/sink.
    xv, yv -- float; coordinates of the source/sink.
    X, Y -- 2D matrix of float; mesh grid.
    
    Output
    ---------
    u, v -- 2D matrix of float; cartesian velocities of the source/sink.
    psi -- 2D matrix of float; potential values on a grid.
    """
    u = strength/(2*numpy.pi)*(X-xs)/((X-xs)**2+(Y-ys)**2)
    v = strength/(2*numpy.pi)*(Y-ys)/((X-xs)**2+(Y-ys)**2)
    psi = strength/(2*numpy.pi)*numpy.arctan2((Y-ys), (X-xs))

    return u, v, psi
    
def get_doublet_info(strength, xd, yd, X, Y):
    """Returns the cartesian velocities and stream-function
    generated by a doublet.
    
    Arguments
    ---------
    strength -- float; strength of the doublet.
    xv, yv -- 1D array of float; coordinates of the doublet.
    X, Y -- 2D matrix of float; mesh grid.

    Output
    ---------
    u, v -- 2D matrix of float; cartesian velocities of the doublet.
    psi -- 2D matrix of float; potential values on a grid.
    """
    u = - strength/(2*numpy.pi)*((X-xd)**2-(Y-yd)**2)/((X-xd)**2+(Y-yd)**2)**2
    v = - strength/(2*numpy.pi)*2*(X-xd)*(Y-yd)/((X-xd)**2+(Y-yd)**2)**2
    psi = - strength/(2*numpy.pi)*(Y-yd)/((X-xd)**2+(Y-yd)**2)
    
    return u, v, psi

def get_freestream_cylindrical_info(u_inf, R, Theta):
    """Returns the stream-function & velocities generated
    by a freestream in cylindrical coordinates.
    
    Arguments
    ---------
    u_inf -- float; freestream velocity.
    R, Theta -- 2D matrix of float; mesh grid of r-theta values.
    
    Output
    ---------
    vr, vtheta -- 2D matrix of float; cylindrival velocities of the freestream.
    psi -- 2D matrix of float; potential values on a grid.    
    """
    
    vr = u_inf*numpy.cos(Theta)
    vtheta = - u_inf*numpy.sin(Theta)
    
    psi = u_inf*R*numpy.sin(Theta)
    
    return vr, vtheta, psi    
    
def get_doublet_cylindrical_info(strength, R, Theta):
    """Returns the stream-function & velocities generated
    by a doublet in cylindrical coordinates.
    
    Arguments
    ---------
    strength -- float; doublet strength.
    R, Theta -- 2D matrix of float; mesh grid of r-theta values.

    Output
    ---------
    vr, vtheta -- 2D matrix of float; cylindrival velocities of the doublet.
    psi -- 2D matrix of float; potential values on a grid.    
    """
    
    vr = - (strength*numpy.cos(Theta)/(2*numpy.pi*(R**2)))
    vtheta = - (strength*numpy.sin(Theta)/(2*numpy.pi*(R**2)))
    
    psi = - strength*numpy.sin(Theta)/(2*numpy.pi*R)
    
    return vr, vtheta, psi