"""
Module containing classes that represent singe results or sets of results that
are obtained at once.  E.g. the several results that come from one test bar

Also classes to represent a result
"""

from typing import List


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


class ProofStress(Measurement):
    """
    Object representing a single Proof stress measurement.
    """
    def __init__(self, value: float = None, percent: float = None, **kwargs):
        self.percent = percent
        super().__init__(value, **kwargs)

    def __repr__(self):
        return f'ProofStress({self.__dict__})'


class Uts(Measurement):
    """
    Object representing a single ultimate tensile strength (UTS) measurement.
    """
    def __init__(self, value: float = None, **kwargs):
        super().__init__(value, **kwargs)

    def __repr__(self):
        return f'Uts({self.__dict__})'


class Elongation(Measurement):
    """
    Object representing a single elongation result.
    """
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

    def to_dict(self):
        rtn_dict = {}
        for attr in self.__dict__:
            if hasattr(getattr(self, attr), 'to_dict'):
                rtn_dict[attr] = getattr(self, attr).to_dict()
            else:
                rtn_dict[attr] = getattr(self, attr)
        return rtn_dict
