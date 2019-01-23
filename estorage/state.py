from CoolProp.CoolProp import PropsSI
import pandas as pd


def def_state_tp(fluid, T, p):

    state = pd.Series(index=['fluid','T','p','h','s','D'])

    state.fluid = fluid
    state.T = T
    state.p = p
    state.h = PropsSI('H', 'T', T, 'P', p, fluid)
    state.s = PropsSI('S', 'T', T, 'P', p, fluid)
    state.D = PropsSI('D', 'T', T, 'P', p, fluid)

    return state


def def_state_ph(fluid, p, h):
    state = pd.Series(index=['fluid', 'T', 'p', 'h', 's','D'])

    state.fluid = fluid
    state.T = PropsSI('S', 'P', p, 'H', h, fluid)
    state.p = p
    state.h = h
    state.s = PropsSI('S', 'P', p, 'H', h, fluid)
    state.D = PropsSI('D', 'P', p, 'H', h, fluid)

    return state


def def_state_ps(fluid, p, s):
    state = pd.Series(index=['fluid', 'T', 'p', 'h', 's','D'])

    state.fluid = fluid
    state.T = PropsSI('H', 'P', p, 'S', s, fluid)
    state.p = p
    state.h = PropsSI('H', 'P', p, 'S', s, fluid)
    state.s = s
    state.D = PropsSI('D', 'P', p, 'S', s, fluid)

    return state
