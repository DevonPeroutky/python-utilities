#!/ujr/bin/env python
# -*- coding: utf-8 -*-
from math import sqrt

def calc_pixel_color_distance(pixelA, pixelB):
    """
    Calculate the CIE94 distance between two RGB pixels.
    """
    labcolorA = rgb2lab((red(pixelA), green(pixelA), blue(pixelA)))
    labcolorB = rgb2lab((red(pixelB), green(pixelB), blue(pixelB)))
    return cie94(labcolorA, labcolorB)


def cie94(L1_a1_b1, L2_a2_b2):
    """
    Calculate color difference by using CIE94 formulae
    
    See http://en.wikipedia.org/wiki/Color_difference or
    http://www.brucelindbloom.com/index.html?Eqn_DeltaE_CIE94.html.
    
    cie94(rgb2lab((255, 255, 255)), rgb2lab((0, 0, 0)))
    >>> 58.0
    cie94(rgb2lab(rgb(0xff0000)), rgb2lab(rgb('#ff0000')))
    >>> 0.0
    """
    
    L1, a1, b1 = L1_a1_b1
    L2, a2, b2 = L2_a2_b2

    C1 = sqrt(_square(a1) + _square(b1))
    C2 = sqrt(_square(a2) + _square(b2))
    delta_L = L1 - L2
    delta_C = C1 - C2
    delta_a = a1 - a2
    delta_b = b1 - b2
    delta_H_square = _square(delta_a) + _square(delta_b) - _square(delta_C)
    return (sqrt(_square(delta_L)
            + _square(delta_C) / _square(1.0 + 0.045 * C1)
            + delta_H_square / _square(1.0 + 0.015 * C1)))


def rgb2lab(R_G_B):
    """
    Convert RGB colorspace to Lab
    
    Adapted from http://www.easyrgb.com/index.php?X=MATH.
    """
    
    R, G, B = R_G_B
    
    # Convert RGB to XYZ
    
    var_R = ( R / 255.0 )        # R from 0 to 255
    var_G = ( G / 255.0 )        # G from 0 to 255
    var_B = ( B / 255.0 )        # B from 0 to 255

    if ( var_R > 0.04045 ): var_R = ( ( var_R + 0.055 ) / 1.055 ) ** 2.4
    else:                   var_R = var_R / 12.92
    if ( var_G > 0.04045 ): var_G = ( ( var_G + 0.055 ) / 1.055 ) ** 2.4
    else:                   var_G = var_G / 12.92
    if ( var_B > 0.04045 ): var_B = ( ( var_B + 0.055 ) / 1.055 ) ** 2.4
    else:                   var_B = var_B / 12.92

    var_R = var_R * 100.0
    var_G = var_G * 100.0
    var_B = var_B * 100.0

    # Observer. = 2°, Illuminant = D65
    X = var_R * 0.4124 + var_G * 0.3576 + var_B * 0.1805
    Y = var_R * 0.2126 + var_G * 0.7152 + var_B * 0.0722
    Z = var_R * 0.0193 + var_G * 0.1192 + var_B * 0.9505
    
    # Convert XYZ to L*a*b*
    
    var_X = X / 95.047         # ref_X =  95.047   Observer= 2°, Illuminant= D65
    var_Y = Y / 100.000        # ref_Y = 100.000
    var_Z = Z / 108.883        # ref_Z = 108.883

    if ( var_X > 0.008856 ): var_X = var_X ** ( 1.0/3.0 )
    else:                    var_X = ( 7.787 * var_X ) + ( 16.0 / 116.0 )
    if ( var_Y > 0.008856 ): var_Y = var_Y ** ( 1.0/3.0 )
    else:                    var_Y = ( 7.787 * var_Y ) + ( 16.0 / 116.0 )
    if ( var_Z > 0.008856 ): var_Z = var_Z ** ( 1.0/3.0 )
    else:                    var_Z = ( 7.787 * var_Z ) + ( 16.0 / 116.0 )

    CIE_L = ( 116.0 * var_Y ) - 16.0
    CIE_a = 500.0 * ( var_X - var_Y )
    CIE_b = 200.0 * ( var_Y - var_Z )
    return (CIE_L, CIE_a, CIE_b)

def _square(x):
    return x * x
