# Al_properties
Framework for logging aluminium properties.  Intention is that it becomes a web 
app tht can present context data back to user (but one step at at a time...).

## Completed
### Database setup

Using Google Firestore (part of the Firebase app platform), which is document 
noSQL.  Seems to have good 
[documentation](https://firebase.google.com/docs/firestore) and why not - I'll 
give it a go.

I have set up an instance which gives you a keyfile.json .  This is saved in 
the local development repo (ignored in git deliberately for security purposes).
This is an important file which contains connection info.

The google cloud python client library is required and has been installed into 
the local virtual environment with `pip install --upgrade firebase-admin` (see 
[docs](https://firebase.google.com/docs/firestore/quickstart) for details)

#### Access the database
*Note: this is already in crud.py*

```
# Import the firestore module
from google.cloud import firestore

# set the environment variable to the local keyfile
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'keyfile.json'

# Then you can initialise the database object
db = firestore.Client()
```

### Document schema
Each row of data from a table will be a document. Properties are nested to 
allow for meta data e.g. units or method.  To facilitate this there are classes
in the entities module which represent each individual property and then also
the `Properties` class to collect all data from the row (the measured 
properties) and other metadata e.g. temper.

#### Object mappers
**Individual properties:**
* `ProofStress`
* `Uts`
* `Elongation`

*Note: These all inherit from the `Measurement` base class.

All have `to_dict()` which will give a dictionary format ready to be nested in
the document.  *Note: use `to_dict()` instead of `__dict__` as it will exclude
keys with None values.

These should all be collected in a `Properties` object where the `to_dict()` 
method will give the full dictionary ready to be imported directly as a 
document.


### Write function
In the crud module. The `Write` class is used to import csv tables or pandas 
dataframes directly with the `from_dataframe()` or `from_csv()` static methods
respectively. It performs batch import and will currently fail if rows exceed 
500 (firestore document limit for batch import).
