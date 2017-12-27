# import pydoku.solver as slv
import numpy as np


def top95():

    f = open("top95.txt")
    probs = []
    for p in f.readlines():
        probs.append(slv.convex.Convex(9, p.strip()))
    return probs

# import os
# _puzzles = os.listdir('puzzles')
# _puzzles.sort()


def puzzles(i=0):

    f = os.path.join('puzzles', _puzzles[i])
    l = filter(lambda z: not z[0] == '#', open(f).readlines())
               # [z if not z[0]=="#" else '' for z in f.readlines()]

    return matrixize(convert(lambda: "".join(l)))


def matrixize(f):
    s = f()
    a = np.array([int(c) if not c == "." else 0 for c in s])
    n = int(np.sqrt(a.shape[0]))
    a = a.reshape((n, n))

    return lambda: a


def convert(f):

    return lambda: f().replace("\n", "").replace("\t", "").replace(" ", "").replace("0", '.')


@matrixize
@convert
def sample():
    """
    Return a sample Problem instance0
    """
    return """000150070
        106000820
        300860040
        900400567
        004708300
        732006004
        040081009
        017000208
        050037000"""


@matrixize
@convert
def sample_hard():
    """
    Return a sample Problem instance0
    """
    return """400000805
        030000000
        000700000
        020000060
        000080400
        000010000
        000603070
        500200000
        104000000"""


@matrixize
@convert
def sample_tricky():
    """
    Return a "tricky" Problem instance from the paper0
    """
    return """003009081
        000200060
        500010700
        890000000
        005601200
        000000037
        009002008
        070004000
        250800600"""


@matrixize
@convert
def sample_moderate():
    """
    Return a "moderate" Problem instance from the paper0
    """
    return """005000700
        930504000
        840000030
        600020400
        500090008
        009080001
        050000070
        000307086
        001000900"""
