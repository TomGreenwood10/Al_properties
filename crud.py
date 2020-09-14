"""
Module for writing to database
"""

import os
import asyncio
import pandas as pd
from google.cloud import firestore
from entities import ProofStress, Uts, Elongation, Properties


# How too's say to set this environment variable with a terminal but can't get
# this to work plus it would persist across sessions so doing it at the top of
# this file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'keyfile.json'

db = firestore.Client()


class Write:
    """
    Standard writing class.
    """
    # todo: include meta info e.g. grade etc which may not be provided for evey
    #  row in user supplied data

    def __init__(self, user=None):
        self.user = user

    @staticmethod
    def _row_to_obj(row):
        props = Properties()

        # The if statements below are very inflexible to column names - I
        #  intend to replace this to a column recogniser before production
        #  release.
        if 'PS' in row.index:
            props.proof_stress = ProofStress(
                value=row['PS'], percent=0.2, units='MPa')
        if 'UTS' in row.index:
            props.uts = Uts(value=row['UTS'], units='MPa')
        if 'Elongation' in row.index:
            props.elongation = Elongation(
                value=row['Elongation'], units='%')
        if 'temper' in row.index:
            props.temper = row['temper']
        if 'grade' in row.index:
            props.grade = row['grade']
        if 'alloy' in row.index:
            props.alloy = row['alloy']
        # todo: refactor above - must be a tidier, expandable way

        return props

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame):
        batch = db.batch()

        # Gather document object with entities module classes
        for _, row in df.iterrows():
            props = cls._row_to_obj(row)
            doc_ref = db.collection(u'properties').document()
            batch.set(doc_ref, props.to_dict())
        batch.commit()

    @classmethod
    async def from_dataframe_async(cls, df: pd.DataFrame):
        for _, results in df.iterrows():
            doc_ref = db.collection(u'properties').document()
            await doc_ref.set(results.to_dict())

    @classmethod
    def from_csv(cls, csv_path):
        """
        Imports all data in csv into database.

        :param csv_path: string or file object -- path to csv of open file
            object representing a csv in read mode
        """
        df = pd.read_csv(csv_path)
        cls.from_dataframe(df)


class Read:
    """
    Class for reading from database
    """


class Delete:
    @classmethod
    def collection(cls, name: str):
        col_ref = db.collection(name)
        docs = col_ref.limit(500).stream()
        for doc in docs:
            doc.reference.delete()
