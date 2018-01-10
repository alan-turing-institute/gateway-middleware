"""
Sketch of a data model for Blue.

Should be able to create a "Case" from e.g. a json file, save it, load it etc.

A Case has a "job_spec" (class ParamSpecTree) and should be able to produce "Jobs", which are the actual things that run.

"""

import json
import inspect
import sys
import uuid

class UnitsDontMatchError(Exception):

    def __init__(self,message):
        self.message = message


class ValueOutsideRangeError(Exception):

    def __init__(self,message):
        self.message = message



class Param(object):

    """ 
    A parameter of an actual job, with the value chosen (and fixed).
    """

    def __init__(self,name,description,value,units):
        self.name = name
        self.description = description
        self.value = value
        self.units = units

    def get_val(self):
        """
        return tuple (value, units)
        """
        return (self.value,self.units)
        
class Job(object):

    """
    An actual job that actually runs.
    """

    def __init__(self):
        """
        """
        self.id = uuid.uuid4().hex
        self.params = []
        self.compute_info = None
        self.status = "DRAFT"
        

    def set_status(self,status):
        self.status = status
        
    def add_param(self,param_spec):
        """
        Takes in a ParamSpec object (part of a job spec) which has a range of possible values, and a current_val.
        Use this to create a Param object that has a fixed value, and add it to this job's list.
        """
        new_param = Param(param_spec.name, param_spec.description, param_spec.current_val, param_spec.units)
        self.params.append(new_param)

    def set_compute_info(self, compute_info):
        self.compute_info = compute_info

        

        
class Case(object):

    """
    Experimental setup, defining a 'job specification'.
    """

    def __init__(self,name,description=None):
        self.name = name
        self.description = description
        # job_spec is a root ParamSpecTree
        self.job_spec = None
        self.sim_spec = None

    def set_sim_spec(self,sim_spec):
        """
        What is the actual compute resource that we'll run on? (local cluster, azure, ..., ... )?
        """
        self.sim_spec = sim_spec
        
    def set_job_spec(self,job_spec):
        self.job_spec = job_spec


    def load_from_json(self,filename):
        j = json.load(open(filename))
        self.name = j["name"]
        self.description = j["description"]
        self.set_sim_spec(j["sim_spec"])
        job_spec = ParamSpecTree(self.name, self.description)
        job_spec.recursively_load_from_json(j["job_spec"])
        self.set_job_spec(job_spec)
        

        pass

    def save(self):
        pass

    
    def create_job(self, some_backend_stuff):
        """
        Use the job_spec to create a Job - flattening out the tree of param_spec(_tree) objects in to the job's list of Parameters.
        """
        new_job = Job()
        new_job.set_compute_info(some_backend_stuff)
        param_spec_list = self.job_spec.find_all_child_paramspecs()
        for ps in param_spec_list:
            new_job.add_param(ps)
        return new_job

    
        
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

#    def add_child(self, node_name, node_class):
#
#        self.children[node_name] = node_class(node_name)
#        self.children[node_name].set_parent(self)

    def add_child(self,child):
        child.set_parent(self)
        self.children[child.name] = child
        
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


    def recursively_load_from_json(self, node_list):
        """
        Construct tree from an input dictionary d.
        """
        ### get a list of members of this class
        clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
        for node in node_list:
            for class_name,cls in clsmembers:
                if class_name == node["class_name"]:
                    child = cls(name=node["name"],description=node["description"])
                    if "children" in node.keys() and isinstance(child,ParamSpecTree):
                        child.recursively_load_from_json(node["children"])
                        pass
                    if "values" in node.keys() and isinstance(child,ParamSpec):
                        for k,v in node["values"].items():
                            child.__setattr__(k,v)
                            pass
                        child.reset_to_default()
                        pass
                    self.children[node["name"]] = child
                    self.add_child(child)                                        
                    break
                
    def add_child_from_json(self,input_file_obj):
        """ 
        load something from json and use it to construct bits of the tree
        This works if the child to be added is of a class defined in the current module.
        """

        d=json.load(input_file_obj)
        """  find the class in the current module """
        clsmembers = inspect.getmembers(sys.modules[__name__], inspect.isclass)
        for name,cls in clsmembers:
            if name == d["class_name"]:
                self.add_child(cls(d["name"]))
                break
        
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

    def find_all_child_paramspecs(self):
        """ 
        recursive function to navigate the tree, filling this object's list of ParamSpecs as it goes.
        """
        param_spec_list = []
        for child in self.children.values():
            if isinstance(child,ParamSpec):
                param_spec_list.append(child)
            else:
                param_spec_list += child.find_all_child_paramspecs()
                pass
            pass
        return param_spec_list
            

            
class ParamSpec(object):

    """
    A parameter of the model, with min, max, default values, and units.
    """

    def __init__(self,name,description,default_val=None,min_val=None,max_val=None,units=None):

        self.parent = None
        self.name = name
        self.description = description
        self.default_val = default_val
        self.min_val = min_val
        self.max_val = max_val
        self.units = units
        self.current_val = default_val


    def reset_to_default(self):
        self.current_val = self.default_val
        
    def set_val(self,value, units):
        """
        Set the current value - must give units!
        """
        
        if self.units != units:
            raise UnitsDontMatchError("Trying to set %s, units don't match, %s : %s" % (self.name,self.units,units))
        if value > self.max_val or value < self.min_val:
            raise ValueOutsideRangeError("Value for %s is not in allowed range %s - %s" % (self.name,self.min_val, self.max_val))
        self.current_val = value

    def get_val(self):
        """
        Return the current value, and units
        """
        return (self.current_val, self.units)
        
    def set_parent(self, parent):
        
        self.parent = parent

        
        
    

class Density(ParamSpec):

    """
    Density of a fluid - this is a type of ParamSpec
    """

    def __init__(self,name,description=None):

        default_val = 1000.
        min_val = 0.
        max_val = 3000.
        units = "kg/m^3"
        super().__init__(name,description,default_val,min_val,max_val,units)


class Viscosity(ParamSpec):

    """
    Density of a fluid - this is a type of ParamSpec
    """

    def __init__(self,name,description=None):
        default_val=1e-3
        min_val=1e-4
        max_val=1e-2
        units="Pa.s"
        super().__init__(name,description,default_val,min_val,max_val,units)
        

class Length(ParamSpec):

    """
    Length of something - this is a type of ParamSpec
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
        self.add_child(Density(self.name+":density"))
        self.add_child(Viscosity(self.name+":viscosity"))


class Tank(ParamSpecTree):

    """ 
    Class for tank, subclass of ParamSpecTree.
    """

    def __init__(self,name,description=None):

        super().__init__(name,description)
        self.add_child(Length(self.name+":width"))
        self.add_child(Length(self.name+":height"))        
