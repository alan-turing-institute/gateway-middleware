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



- [ ] represent a parameter as a `ParameterSpec`
- [ ] associate the parameter with a case
- [ ] generate a job from the case



- [ ] clone a job