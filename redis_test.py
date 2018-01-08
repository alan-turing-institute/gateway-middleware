"""
Try using Redis (an open source key/value NoSQL DB) to store pickled "case" objects.
"""

import redis
import pickle
from model_python_classes import *




def load_from_redis(key):
    """
    retrieve an object from Redis and unpickle it.
    """
    rs = redis.Redis(host="localhost", port=6379)
    return pickle.loads(rs.get(key))

def create_test_case():
    """
    create a case called TestCase, with a full jobSpec.
    """

    case = Case("TestCase")
    job_spec = ParamSpecTree(name="JobSpecA",description="tank+2 fluids")
    job_spec.add_child("Tank",Tank)
    job_spec.add_child("Fluid_1",Fluid)
    job_spec.add_child("Fluid_2",Fluid)
    case.set_job_spec(job_spec)
    return case


    
def save_to_redis(keyname, obj):
    """
    Save pickle(obj) to Redis with key keyname.
    """
    rs = redis.Redis(host="localhost", port=6379)
    result = rs.set(keyname, pickle.dumps(obj))
    return result

    

if __name__ == "__main__":
    c = create_test_case()

    save_result = save_to_redis("TestCase1",c)
    if save_result:
        print("Saved %s OK!" % c.name)
        ### now load it back
        c2 = load_from_redis("TestCase1")
        print("Loaded %s OK!" % c2.name)
        
