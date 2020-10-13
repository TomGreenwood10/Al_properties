# Al_properties
Framework for logging aluminium properties.  Intention is that it becomes a web 
app that can present context data back to user (but one step at at a time...).

## Completed
[x] Database setup
[ ] Object mappers (*in progress*)

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
[docs](https://firebase.google.com/docs/firestore/quickstart) for details).
This should all happen when using requirements.txt for environment setup.

#### Access the database
*Note: this is already in relevant modules*

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
The overall concept of this application resolved around the `Table` object 
class. When importing into the database a `Table` object is created from the 
set of results to import then the write_to_db() method writes all the 
information to google firestore. The `Table` class deals with the formatting of
the data so that it forms the corect document schema.  Therefore the `Table` 
object serves as the middle man between the raw data and the database.

`Table` objects represent a `Table` of results with one or more rows. Contained
are Properties objects that represent single rows and inside them are 
individual measurement objects which represent each individual measurement.
The main reason for using objects rather that direct import from the data is so
that meta data can be held and inserted into database documents which are not
necessarily in every row or the raw data, e.g. units or measurement method.
