# Science-gateway data model



```
parameter_spec = ParameterSpec(name='foo', value=20)

family = ParameterFamily()
family.append(parameter_spec)

case = Case(family_list=family)

job = case.to_job()

job_cloned = job.clone()
job_shareable = job.share()
```



- [x] Do we use python classes or sqlalchemy classes

      > Use sqlalchemy classes as these will be used in the production version. We are passing around sqlalchemy objects (i.e. treating them as raw python objects that happen to have serialisation/de-serialisation methods)



- [ ] represent a parameter as a `ParamSpec`
- [ ] associate the parameter with a case
- [ ] generate a job from the case



- [ ] clone a job


- [x] Things to investigate - Ontology (OWL, RDF), Object Store (key:value pairs storing object (pickle?) in DB).


- Playing around in pure python classes - model_classes_no_db.py and test_ui_no_db.py (and test_param_sets.json)

```
python -i test_ui.py
>>> my_ui.display()
```

This constructs a ParamSpecTree, and then loads values from a json file to apply to the leaf nodes.


## Trying a key/object store:  Redis
Redis is open source, BSD licensed.
Download tar.gz from https://redis.io/
then unpack, cd to directory, and
`make`
then
```
cd src
./redis-server
```
server will be running on localhost port 6379.
There is a Python wrapper, that can be installed with
`pip install redis`.
Seems to be trivial to store/retrieve pickled items:
```
import redis
import pickle
rs = redis.Redis(host="localhost", port=6379)
save_result = rs.set(mykey,pickle.dumps(myobj))
retrieved_obj = pickle.loads(rs.get(mykey))
```
(see redis_test.py)

