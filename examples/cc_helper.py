"""
3 entries for FSM

input, states, outputs

 table for forward states - for CC just shift
(s >> 1) | in

table for outputs - for CC output of concatenated outputs of polys
"""

def popcount(val):
    accum = 0
    while val > 0:
        accum += (val & 1)
        val = val >> 1
    return accum

def parity(val):
    return popcount(val) & 1

def cc_fsm_gen(k, polys):
    st = []
    outs = []
    for i in range(1 << (k-1)):
        for j in [0,1]:
            nst = i | (j << (k-1))
            st.append(nst >> 1)

            accum = 0
            for pi, p in enumerate(polys):
                accum |= parity(p & nst) << pi
            outs.append(accum)
    return st, outs

if __name__ == '__main__':
    s,o = cc_fsm_gen(3, [7, 5])
    #print("states", s)
    #print("outs  ", o)

    s,o = cc_fsm_gen(7, [0o133, 0o171])
    print("states", len(s), s)
    print("outs  ", len(o), o)

    s2 = [int(x) for x in """
0 32
0 32
1 33
1 33
2 34
2 34
3 35
3 35
4 36
4 36
5 37
5 37
6 38
6 38
7 39
7 39
8 40
8 40
9 41
9 41
10 42
10 42
11 43
11 43
12 44
12 44
13 45
13 45
14 46
14 46
15 47
15 47
16 48
16 48
17 49
17 49
18 50
18 50
19 51
19 51
20 52
20 52
21 53
21 53
22 54
22 54
23 55
23 55
24 56
24 56
25 57
25 57
26 58
26 58
27 59
27 59
28 60
28 60
29 61
29 61
30 62
30 62
31 63
31 63
""".split()]
    o2 = [int(x) for x in """
0 3
3 0
1 2
2 1
0 3
3 0
1 2
2 1
3 0
0 3
2 1
1 2
3 0
0 3
2 1
1 2
3 0
0 3
2 1
1 2
3 0
0 3
2 1
1 2
0 3
3 0
1 2
2 1
0 3
3 0
1 2
2 1
2 1
1 2
3 0
0 3
2 1
1 2
3 0
0 3
1 2
2 1
0 3
3 0
1 2
2 1
0 3
3 0
1 2
2 1
0 3
3 0
1 2
2 1
0 3
3 0
2 1
1 2
3 0
0 3
2 1
1 2
3 0
0 3
""".split()]
    assert(o2 == o)
    assert(s2 == s)

    s,o = cc_fsm_gen(5, [0o35, 0o23])
    print("states", len(s), s)
    print("outs  ", len(o), o)
