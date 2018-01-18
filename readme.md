
### Current status (18th Jan 5:30pm)

* renamed app.py to sqlalchemy_classes.py and removed everything that wasn't related to defining the classes
* separated out lengthy code to create tank, fluid cases, and milk,water,tankX mintstore into separate modules.
* "main" script is now create_and_mint_case_using_stores.py
 - implemented functions to create a MintedCase given a Case and a mapping (dict) between case_fields and mintstore objects.
* added marshmallow_schema_classes.py - can currently serialize/deserialize cases and their children.  Will add example
and extend to Minted stuff.

To run:
```
python -i create_and_mint_case_using_stores.py
```

* Not yet implemented:
   * having the minted case know what mintstore names and versions its
values came from.
   * marshmallow serialization/deserialization of the "Minted" half of the data model.
