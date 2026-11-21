"""Finite ellipse focal-area qualification and coordinate angle checks."""
import sympy as sp
from .transition_primitives import TransitionError

def focal_area(aa,bb,cc,theta):
    if any(v.free_symbols or v.is_real is not True or v.is_finite is not True for v in (aa,bb,cc,theta)):
        raise TransitionError('undetermined','Finite numeric inputs required')
    if theta.is_positive is not True or (sp.pi-theta).is_positive is not True:
        raise TransitionError('conflict','Nondegenerate angle in (0, pi) required')
    margin=sp.simplify(cc-aa*sp.sin(theta/2)**2)
    if margin.is_nonnegative is not True:
        raise TransitionError('conflict' if margin.is_negative else 'undetermined','Angle not attainable on ellipse')
    return sp.simplify(bb*sp.tan(theta/2)),margin

def verify_point_angle(xy,axis,cc,theta):
    u,v=xy if axis=='x' else tuple(reversed(xy))
    c=sp.sqrt(cc)
    product=sp.sqrt(((u-c)**2+v*v)*((u+c)**2+v*v))
    if product.is_positive is not True:raise TransitionError('conflict','Angle has zero direction')
    if sp.simplify((u*u+v*v-cc)/product-sp.cos(theta))!=0:
        raise TransitionError('conflict','Coordinates contradict given focal angle')
