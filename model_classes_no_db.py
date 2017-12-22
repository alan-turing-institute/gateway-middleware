"""
Sketch of a data model for Blue.
"""

import json


class UnitsDontMatchError(Exception):

    def __init__(self,message):
        self.message = message


class ValueOutsideRangeError(Exception):

    def __init__(self,message):
        self.message = message


class Case(object):

    """
    Experimental setup, defining a 'job specification'.
    """

    def __init__(self,name,description=None):
        self.name = name
        self.description = description
        # job_spec is a root ParamSpecTree
        self.job_spec = None

    def set_job_spec(self,job_spec):
        self.job_spec = job_spec


    def load(self,name):
        pass

    def save(self):
        pass

        
class ParamSpecTree(object):

    
    """ 
    group of parameters in the form of a tree.  
    Can have children that are other nodes (ParamSpecTrees), or leafs (ParamSpecs)
    """

    def __init__(self,name,description=None):

        self.name = name
        self.description = description
        self.parent = None
        self.children = {}

    def set_parent(self,parent):

        self.parent = parent

    def add_child(self, node_name, node_class):

        self.children[node_name] = node_class(node_name)
        self.children[node_name].set_parent(self)

    def __getitem__(self,key):
        """ 
        Allow dict-like retrieval of children by key.
        """
        return self.children[key]
        
        
    def find_node(self,node_name):
        """ 
        recursive function to find a named node amongst this nodes's children.
        """
        found_node = False

    def load_parameter_tree_from_file(self,input_file,node_name,paramset_name):
        """ 
        find a set of parameters in a list of input dicts, and apply them to a chosen node of the ParamSpecTree
        """
        input_params = json.load(open(input_file))

        params = None
        
        for paramset in input_params:
            print(".... looking at paramset %s " % paramset["name"])
            if paramset["name"] != paramset_name:
                print(" ---nope")
                continue
            params = paramset["parameters"]
            break
        if not params:
            return
        ### now find the node within this parameter tree's children
        node = self.find_child_node(node_name)
        if node:
            print("Found node %s" % node_name)
            node.load_parameters(params)
        
    def find_child_node(self, node_name):
        """ 
        recursive function to navigate the tree, filling the list of sliders as it goes.
        """
        for child in self.children.values():
            print("Child name is %s" % child.name)
            if child.name == node_name:
                return child
            elif isinstance(child,ParamSpecTree):
                found = child.find_child_node(child)
                if found:
                    return found
                pass
            pass
        pass
    
        
    def load_parameters(self,params_list):
        for param in params_list:
            if not param["name"] in self.children.keys():
                print("ParamSpec for %s not in this tree" % param["name"])
                continue
            if not isinstance(self.children[param["name"]],ParamSpec):
                print("%s is not of class ParamSpec" % param["name"])
                continue
            print("Setting %s to %s" % (param["name"],param["value"]))
            self.children[param["name"]].set_val(param["value"],param["units"])


class ParamSpec(object):

    """
    A parameter of the model, with min, max, default values, and units.
    """

    def __init__(self,name,description,default_val,min_val,max_val,units):

        self.parent = None
        self.name = name
        self.description = description
        self.default_val = default_val
        self.min_val = min_val
        self.max_val = max_val
        self.units = units
        self.current_val = default_val

    def set_val(self,value, units):

        if self.units != units:
            raise UnitsDontMatchError("Trying to set %s, units don't match, %s : %s" % (self.name,self.units,units))
        if value > self.max_val or value < self.min_val:
            raise ValueOutsideRangeError("Value for %s is not in allowed range %s - %s" % (self.name,self.min_val, self.max_val))
        self.current_val = value

    def set_parent(self, parent):
        self.parent = parent

    

class Density(ParamSpec):

    """
    Density of a fluid
    """

    def __init__(self,name,description=None):

        default_val = 1000.
        min_val = 0.
        max_val = 3000.
        units = "kg/m^3"
        super().__init__(name,description,default_val,min_val,max_val,units)


class Viscosity(ParamSpec):

    """
    Density of a fluid
    """

    def __init__(self,name,description=None):
        default_val=1e-3
        min_val=1e-4
        max_val=1e-2
        units="Pa.s"
        super().__init__(name,description,default_val,min_val,max_val,units)
        

class Length(ParamSpec):

    """
    Length of something
    """

    def __init__(self,name,description=None):
        default_val=2.
        min_val=0.
        max_val=10.
        units="m"
        super().__init__(name,description,default_val,min_val,max_val,units)
        
        
class Fluid(ParamSpecTree):

    """ 
    Class for fluid, subclass of ParamSpecTree.
    """

    def __init__(self,name,description=None):

        super().__init__(name,description)
        self.add_child("density",Density)
        self.add_child("viscosity",Viscosity)


class Tank(ParamSpecTree):

    """ 
    Class for tank, subclass of ParamSpecTree.
    """

    def __init__(self,name,description=None):

        super().__init__(name,description)
        self.add_child("width",Length)
        self.add_child("depth",Length)        
