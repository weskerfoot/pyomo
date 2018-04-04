#!/usr/bin/env python

import pyutilib.th as unittest

from pyomo.core.base.expr import identify_variables
from pyomo.environ import *
from pyomo.contrib.trustregion.PyomoInterface import *

class TestPyomoInterfaceInitialization(unittest.TestCase):
    def setUp(self):
        m = ConcreteModel()
        m.z = Var(range(3),domain=Reals)
        for i in range(3):
            m.z[i] = 2.0
        m.x = Var(range(2))
        for i in range(2):
            m.x[i] = 2.0
        m.obj = Objective(expr= (m.z[0]-1.0)**2 + (m.z[0]-m.z[1])**2 + (m.z[2]-1.0)**2 + (m.x[0]-1.0)**4 + (m.x[1]-1.0)**6)
        m.c2 = Constraint(expr=m.z[2]**4 * m.z[1]**2 + m.z[1] == 8+sqrt(2.0))
        self.m = m

    def test_1(self):
        '''
        The simplest case that the black box has only two inputs and there is only one black block involved
        '''
        def blackbox(a,b):
            return sin(a-b)

        m = self.m
        bb = ExternalFunction(blackbox)
        m.eflist = [bb]
        m.c1 = Constraint(expr=m.x[0] * m.z[0]**2 + bb(m.x[0],m.x[1]) == 2*sqrt(2.0))
        pI = PyomoInterface(m, [bb])
        self.assertEqual(pI.lx,2)
        self.assertEqual(pI.ly,1)
        self.assertEqual(pI.lz,3)
        self.assertEqual(len(list(identify_variables(m.c1.body))),3)
        self.assertEqual(len(list(identify_variables(m.c2.body))),2)

    def test_2(self):
        '''
        The simplest case that the black box has only one inputs and there is only a formula
        '''
        def blackbox(a):
            return sin(a)

        m = self.m
        bb = ExternalFunction(blackbox)
        m.eflist = [bb]
        m.c1 = Constraint(expr=m.x[0] * m.z[0]**2 + bb(m.x[0]-m.x[1]) == 2*sqrt(2.0))
        pI = PyomoInterface(m, [bb])
        self.assertEqual(pI.lx,1)
        self.assertEqual(pI.ly,1)
        self.assertEqual(pI.lz,5)
        self.assertEqual(len(list(identify_variables(m.c1.body))),3)
        self.assertEqual(len(list(identify_variables(m.c2.body))),2)
        self.assertEqual(len(m.tR.conset),1)
        self.assertEqual(len(list(identify_variables(m.tR.conset[1].body))),3)

    def test_3(self):
        '''
        The simplest case that the black box has only two inputs and there is only one black block involved
        '''
        def blackbox(a,b):
            return sin(a-b)

        m = self.m
        bb = ExternalFunction(blackbox)
        m.eflist = [bb]
        m.c1 = Constraint(expr=m.x[0] * m.z[0]**2 + bb(m.x[0], m.x[1]) == 2*sqrt(2.0))
        m.c3 = Constraint(expr=m.x[0] * m.z[0]**2 + bb(m.x[0], m.z[1]) == 2*sqrt(2.0))
        pI = PyomoInterface(m, [bb])
        self.assertEqual(pI.lx,3)
        self.assertEqual(pI.ly,2)
        self.assertEqual(pI.lz,2)
        self.assertEqual(len(list(identify_variables(m.c1.body))),3)
        self.assertEqual(len(list(identify_variables(m.c2.body))),2)
        self.assertEqual(len(list(identify_variables(m.c3.body))),3)


    def test_4(self):
        '''
        The simplest case that the black box has only two inputs and there is only one black block involved
        '''
        def blackbox(a,b):
            return sin(a-b)

        m = self.m
        bb = ExternalFunction(blackbox)
        m.eflist = [bb]
        m.c1 = Constraint(expr=m.x[0] * m.z[0]**2 + bb(m.x[0], m.x[1]) == 2*sqrt(2.0))
        m.c3 = Constraint(expr=m.x[0] * m.z[0]**2 + bb(m.x[0], m.z[1]) == 2*sqrt(2.0))
        pI = PyomoInterface(m, [bb])
        self.assertEqual(pI.lx,3)
        self.assertEqual(pI.ly,2)
        self.assertEqual(pI.lz,2)
        self.assertEqual(len(list(identify_variables(m.c1.body))),3)
        self.assertEqual(len(list(identify_variables(m.c2.body))),2)
        self.assertEqual(len(list(identify_variables(m.c3.body))),3)





if __name__ == '__main__':
    unittest.main()
