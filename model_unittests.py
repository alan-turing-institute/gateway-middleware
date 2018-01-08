#!/usr/bin/env python

""" 
Unit tests for model_no_db
"""

import unittest

from  model_python_classes import *

import redis
import pickle


class TestParamSpecs(unittest.TestCase):
    """
    Test assigning values to ParamSpecs.
    """

    
    def test_wrong_units(self):
        density = ParamSpec(name="density",description="density",min_val=0.,max_val=10.,default_val=5.,units="kg/m^3")
        with self.assertRaises(UnitsDontMatchError):
            density.set_val(5.0,None)

    def test_value_outside_range(self):
        density = ParamSpec(name="density",description="density",min_val=0.,max_val=10.,default_val=5.,units="kg/m^3")
        with self.assertRaises(ValueOutsideRangeError):
            density.set_val(55.0,"kg/m^3")

    def test_set_and_retrieve(self):
        density = ParamSpec(name="density",description="density",min_val=0.,max_val=10.,default_val=5.,units="kg/m^3")
        test_val = 3.2
        test_units = "kg/m^3"
        density.set_val(test_val,test_units)
        val,units = density.get_val()
        self.assertTrue(test_val == val and test_units == units)
        
            

class TestParamSpecTree(unittest.TestCase):
    """
    Test constructing a tree and accessing leaf node values.
    """

    def setUp(self):
        self.root_node = ParamSpecTree(name="myJobSpec",description="2 fluids+ tank")

    def test_add_child(self):
        self.root_node.add_child("Fluid_1",Fluid)
        self.assertTrue(self.root_node["Fluid_1"].__class__ == Fluid)

    def test_child_parentage(self):
        self.root_node.add_child("Fluid_1",Fluid)
        self.assertTrue(self.root_node["Fluid_1"].parent.name == self.root_node.name)
        

class TestRedis(unittest.TestCase):
    """
    Test saving stuff to a redis db, reading it back, changing something, saving it again, and reading it back again. 
    """

    def setUp(self):
        self.rs = redis.Redis(host="localhost", port=6379)
        self.case = Case("TestCase")
        job_spec = ParamSpecTree(name="JobSpecA",description="tank+2 fluids")
        job_spec.add_child("Tank",Tank)
        job_spec.add_child("Fluid_1",Fluid)
        job_spec.add_child("Fluid_2",Fluid)
        self.case.set_job_spec(job_spec)

    def test_save_to_redis(self):
        self.assertTrue(self.rs.set("MyCase",pickle.dumps(self.case)))

    def test_save_load_change_save_load(self):
        """
        save self.case, then load it back, change a value and save it again.
        Then load it again, and check we have the changed value.
        """
        ### save with key MyCase
        self.rs.set("MyCase",pickle.dumps(self.case))
        ### load it back
        loaded_case = pickle.loads(self.rs.get("MyCase"))
        ### we will set the density to this value
        test_val = 1321.5
        loaded_case.job_spec["Fluid_1"]["density"].set_val(test_val,"kg/m^3")
        ### save it again
        self.rs.set("MyCase",pickle.dumps(loaded_case))
        ### load it again
        test_case = pickle.loads(self.rs.get("MyCase"))
        self.assertEqual(test_val, test_case.job_spec["Fluid_1"]["density"].get_val()[0])

        
if __name__ == "__main__":
    unittest.main()
