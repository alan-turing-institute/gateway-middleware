#!/usr/bin/env python
""" 
Test out various aspects of the data model, using pure python classes.
Use matplotlib sliders as a quick'n'dirty way of illustrating the sliders.
"""

import sqlalchemy
from sqlalchemy import create_engine, ForeignKey 
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker,relationship
from sqlalchemy import Column, Integer, String, Float

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button

from model_classes_no_db import *



class FakeSlider(object):
    """
    Represents a variable, has a name, a range of allowed values, and a current value.
    """
    def __init__(self, name, allowed_range, current_value):
        self.name = name
        self.allowed_range = allowed_range
        self.current_value = current_value
        pass

    def set_value(self,value):
        self.current_value = value

    def get_value(self):
        return self.current_value

    def get_range_min(self):
        return self.allowed_range[0]

    def get_range_max(self):
        return self.allowed_range[1]
    

class FakeUserInterface(object):
    """ 
    Something that represents a UI, contains sliders, each of which has a range and a current value.
    """
    
    def __init__(self):
        self.families = []
        self.sliders = []
        pass

    def load_job_spec(self,job_spec):
        """ 
        will get a root-level ParamSpecTree - need to navigate along to the params, and create a slider for each param.
        """
        if not isinstance(job_spec,ParamSpecTree):
            raise TypeError("JobSpec must be a ParamSpecTree")
        self.navigate_param_spec_tree(job_spec)
        
    def navigate_param_spec_tree(self,param_spec_tree):
        """ 
        recursive function to navigate the tree, filling the list of sliders as it goes.
        """
        for child in param_spec_tree.children.values():
            if isinstance(child,ParamSpec):
                slider = FakeSlider(child.parent.name+"::"+child.name,(child.min_val,child.max_val),child.current_val)
                self.sliders.append(slider)                
            else:
                self.navigate_param_spec_tree(child)
                pass
            pass
        pass

    def display(self):
        fig, axes = plt.subplots(len(self.sliders),1)
        display_sliders = []
        for i in range(len(self.sliders)):
            print("Configuring slider %i" % (i))
            display_sliders.append(Slider(axes[i],self.sliders[i].name,
                                          self.sliders[i].allowed_range[0],
                                          self.sliders[i].allowed_range[1],
                                          self.sliders[i].get_value()))
        plt.show()

        

if __name__ == "__main__":

    ### build a simple example job_spec:
    
    job_spec = ParamSpecTree(name="tank_two_fluids",description="tank+2 fluids")
    job_spec.add_child("Tank",Tank)
    job_spec.add_child("Fluid_1",Fluid)
    job_spec.add_child("Fluid_2",Fluid)
    
    ## construct a UI view
    my_ui = FakeUserInterface()

    job_spec.load_parameter_tree_from_file("test_param_sets.json","Fluid_1","water")
    job_spec.load_parameter_tree_from_file("test_param_sets.json","Fluid_2","oil")    
    job_spec.load_parameter_tree_from_file("test_param_sets.json","Tank","tankA")

    case = Case(name="water+oil in tankA")
    case.set_job_spec(job_spec)
    
    my_ui.load_job_spec(job_spec)
