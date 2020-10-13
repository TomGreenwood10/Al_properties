"""
Module for writing to database
"""

from google.cloud import firestore


# How too's say to set this environment variable with a terminal but can't get
# this to work plus it would persist across sessions so doing it at the top of
# this file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'keyfile.json'

db = firestore.Client()


class Delete:
    @classmethod
    def collection(cls, name: str):
        col_ref = db.collection(name)
        docs = col_ref.limit(500).stream()
        for doc in docs:
            doc.reference.delete()
    # todo: make the above delete more the 500 (the whole lot!)
