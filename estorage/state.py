from CoolProp.CoolProp import PropsSI
import pandas as pd


def def_state_tp(fluid, t, p):

    state = pd.Series(index=['fluid','t','p','h','s'])

    state.fluid = fluid
    state.t = t
    state.p = p
    state.h = PropsSI('H', 'T', t, 'P', p, fluid)
    state.s = PropsSI('S', 'T', t, 'P', p, fluid)

    return state


def def_state_ph(fluid, p, h):
    state = pd.Series(index=['fluid', 't', 'p', 'h', 's'])

    state.fluid = fluid
    state.t = PropsSI('S', 'P', p, 'H', h, fluid)
    state.p = p
    state.h = h
    state.s = PropsSI('S', 'P', p, 'H', h, fluid)

    return state


def def_state_ps(fluid, p, s):
    state = pd.Series(index=['fluid', 't', 'p', 'h', 's'])

    state.fluid = fluid
    state.t = PropsSI('H', 'P', p, 'S', s, fluid)
    state.p = p
    state.h = PropsSI('H', 'P', p, 'S', s, fluid)
    state.s = s

    return state
