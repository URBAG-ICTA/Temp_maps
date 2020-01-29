# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 12:10:39 2020

@author: 1361078
"""
import math
import numpy as np


def xcomponent(speed,direction):
    direction2 = math.radians(direction)
    return -speed*math.sin(direction2)

def ycomponent(speed,direction):
    direction2 = math.radians(direction)
    return -speed*math.cos(direction2)

def speed(x, y):
    return math.sqrt(x**2+y**2)

def direction(x, y):
    angle = math.atan2(-x, -y)
    if angle < 0:
        angle = angle+2*math.pi
    angle = math.degrees(angle)
    return angle

def u_rotate(u, v, cosa, sina):
    return u*cosa -v*sina

def v_rotate(u, v, cosa, sina):
    return u*sina +v*cosa

def z(ph0, phb0, ph1, phb1):
    z = 0.5*float(ph0+phb0+ph1+phb1)/9.81
    return z

def pressure(p, pb):
    pres = p+pb
    return pres

def temp(theta, p):
    t = theta*pow(p/100000, 2/7)
    return t

def rh(qvapor, pressure, temperature):
    e0 = 6.112
    b = 17.67
    T1 = 273.15
    T2 = 29.65
    eps = 0.622
    es = float(e0*math.exp(b*(temperature-T1)/(temperature-T2)))
    qs = float(eps*es/((pressure/100.) -es))
    rh = 100*qvapor/qs
    if rh > 100:
        rh = 100
    if rh < 0:
        rh = 0
    return rh

def coordinates(wfile):
    LON = np.array(wfile.variables['XLONG'])
    LAT = np.array(wfile.variables['XLAT'])
    LON = LON[0]
    LAT = LAT[0]
    LONU = np.array(wfile.variables['XLONG_U'])
    LATU = np.array(wfile.variables['XLAT_U'])
    LONU = LONU[0]
    LATU = LATU[0]
    LONV = np.array(wfile.variables['XLONG_V'])
    LATV = np.array(wfile.variables['XLAT_V'])
    LONV = LONV[0]
    LATV = LATV[0]
    return LON, LAT, LONU, LATU, LONV, LATV