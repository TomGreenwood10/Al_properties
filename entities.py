"""
Module containing classes that represent single results or sets of results that
are obtained at once.  E.g. the several results that come from one test bar

Also classes to represent a result
"""

import os
from typing import List, Tuple
import pandas as pd
from google.cloud import firestore


# How too's say to set this environment variable with a terminal but can't get
# this to work plus it would persist across sessions so doing it at the top of
# this file
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'keyfile.json'

db = firestore.Client()


class Measurement:
    """
    Class for measurements with standards attributes (e.g. a mechanical
    strength result)
    """
    def __init__(self,
                 value: float = None,
                 standards: List[str] = None,
                 notes: List[str] = None,
                 units: str = None):
        self.value = value
        self.standards = standards
        self.notes = notes
        self.units = units

    def to_dict(self):
        return {
            key: val for key, val in self.__dict__.items() if val is not None
        }

    def __add__(self, other):
        if isinstance(other, Measurement):
            return Properties.from_measurements(self, other)
        else:
            raise TypeError("'+' operator not supported between instances of "
                            f"Measurement and {type(other)}")


class ProofStress(Measurement):
    """
    Object representing a single Proof stress measurement.
    """
    name = 'proof_stress'

    def __init__(self, value: float = None, percent: float = None, **kwargs):
        self.percent = percent
        super().__init__(value, **kwargs)

    def __repr__(self):
        return f'ProofStress({self.__dict__})'


class Uts(Measurement):
    """
    Object representing a single ultimate tensile strength (UTS) measurement.
    """
    name = 'uts'

    def __init__(self, value: float = None, **kwargs):
        super().__init__(value, **kwargs)

    def __repr__(self):
        return f'Uts({self.__dict__})'


class Elongation(Measurement):
    """
    Object representing a single elongation result.
    """
    name = 'elongation'

    def __init__(self, value: float = None, **kwargs):
        super().__init__(value, **kwargs)

    def __repr__(self):
        return f'Elongation({self.__dict__})'


class Properties:
    """
    Object representing a set of results for a single item / coupon / bar
    tested.
    """
    def __init__(self,
                 proof_stress: ProofStress = None,
                 uts: Uts = None,
                 elongation: Elongation = None,
                 grade: str = None,
                 temper: str = None,
                 alloy: str = None):
        self.proof_stress = proof_stress
        self.uts = uts
        self.elongation = elongation
        self.grade = grade
        self.temper = temper
        self.alloy = alloy

    def __repr__(self):
        return f'Properties({self.__dict__})'

    def __add__(self, other):
        if isinstance(other, Measurement):

            # Seems safest to error if the meaurement is already an attribute  
            if getattr(self, other.name):
                raise AttributeError("Properties object already has "
                                     f"{other.name} attribute")
            
            # Method - create a new Properties object, transfer attributes then
            #   add new measurement
            new_obj = self._copy()
            setattr(new_obj, other.name, other)
            return new_obj

        elif isinstance(other, Properties):
            # Method - create a copy then if the other Properties has an
            #   attribute then transfer it. Error if it's already there. Then
            #   return the new object, originals preserved.
            new_obj = self.copy()
            for attr_name, attr in other.__dict__.items():
                if getattr(other, attr_name):
                    if getattr(new_obj, attr_name):
                        raise AttributeError(
                            "instance allredy has {attr_name} attribute - "
                            "cannot be overwritten"
                        )
                    setattr(new_obj, attr_name, attr)
            return new_obj

    @classmethod
    def _transfer_attrs_to_new(cls, obj):
        new_obj = cls()
        for attr_name, attr in obj.__dict__.items():
            setattr(new_obj, attr_name, attr)
        return new_obj

    def copy(self):
        return Properties()._transfer_attrs_to_new(self)

    def to_dict(self):
        rtn_dict = {}
        for attr in self.__dict__:
            if hasattr(getattr(self, attr), 'to_dict'):
                rtn_dict[attr] = getattr(self, attr).to_dict()
            else:
                rtn_dict[attr] = getattr(self, attr)
        return rtn_dict
    
    @staticmethod
    def from_measurements(*measurements):
        new_obj = Properties()
        for measurement in measurements:
            setattr(new_obj, measurement.name, measurement)
        return new_obj

    @classmethod
    def from_row(cls, row: Tuple):
        props = cls()

        if 'PS' in row.index:
            props.proof_stress = ProofStress(value=row['PS'])
        if 'UTS' in row.index:
            props.uts = Uts(value=row['UTS'])
        if 'Elongation' in row.index:
            props.elongation = Elongation(value=row['Elongation'])
        if 'temper' in row.index:
            props.temper = row['temper']
        if 'grade' in row.index:
            props.grade = row['grade']
        if 'alloy' in row.index:
            props.alloy = row['alloy']
        # todo: refactor above - must be a tidier, expandable way

        return props

    def write_to_db(self):
        doc_ref = db.collection('properties').document()
        doc_ref.set(self.to_dict())


class Table:
    """
    To contain sets of Properties
    """
    def __init__(self):
        self.properties = []
        self.property_names = []

    def __repr__(self):
        return (f"Table(columns={self.property_names}, "
                f"rows={len(self.properties)})")

    @classmethod
    def from_csv(cls, path: str):
        df = pd.read_csv(path)
        return cls.from_dataframe(df)

    @classmethod
    def from_dataframe(cls, df: pd.DataFrame):
        table = cls()
        table.property_names = df.columns
        for _, row in df.iterrows():
            table.properties.append(Properties.from_row(row))
        return table
    
    def to_dataframe(self):
        pass

    def to_csv(self):
        pass

    def write_to_db(self):
        batch = db.batch()
        for item in self.properties:
            doc_ref = db.collection('properties').document()
            batch.set(doc_ref, item.to_dict())
        batch.commit()
