
### Current status (18th Jan 3pm)

* renamed app.py to sqlalchemy_classes.py and removed everything that wasn't related to defining the classes
* separated out lengthy code to create tank, fluid cases, and milk,water,tankX mintstore into separate modules.
* "main" script is now create_and_mint_case_using_stores.py
 - currently implementing functions to create a MintedCase given a Case and some MintStore objects.
* added marshmallow_schema_classes.py - can currently serialize/deserialize cases and their children.  Will add example
and extend to Minted stuff.
