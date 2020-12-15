# Confidential, Copyright 2020, Sony Corporation of America, All rights reserved.

from dataclasses import dataclass, field
from typing import Set, cast

from .base_business import BusinessBaseLocation
from ..interfaces import PersonID, InfectionSummary, BusinessLocationState, SimTimeTuple

__all__ = ['Hospital', 'HospitalState']


@dataclass
class HospitalState(BusinessLocationState):
    open_time: SimTimeTuple = SimTimeTuple()

    patient_capacity: int = -1
    """Number of patients allowed to be admitted to the Hospital"""

    patients_in_location: Set[PersonID] = field(default_factory=set, init=False)
    """A set of ids of patients who are currently in the location. Default is an empty set."""

    @property
    def persons_in_location(self) -> Set[PersonID]:
        persons = super().persons_in_location
        persons.union(self.patients_in_location)
        return persons


class Hospital(BusinessBaseLocation[HospitalState]):
    """Class that implements a basic hospital location. """

    def create_state(self) -> HospitalState:
        return HospitalState()

    def is_entry_allowed(self, person_id: PersonID) -> bool:
        inf_sum = self._registry.get_person_infection_summary(person_id)
        state = cast(HospitalState, self._state)

        allow_patient = (inf_sum == InfectionSummary.CRITICAL and
                         (state.patient_capacity == -1 or len(state.patients_in_location) < state.patient_capacity))

        return allow_patient or (inf_sum != InfectionSummary.CRITICAL and super().is_entry_allowed(person_id))

    def add_person_to_location(self, person_id: PersonID) -> None:
        inf_sum = self._registry.get_person_infection_summary(person_id)
        state = cast(HospitalState, self._state)
        if inf_sum == InfectionSummary.CRITICAL:
            state.patients_in_location.add(person_id)
        else:
            super().add_person_to_location(person_id)

    def remove_person_from_location(self, person_id: PersonID) -> None:
        state = cast(HospitalState, self._state)
        if person_id in state.patients_in_location:
            state.patients_in_location.remove(person_id)
        else:
            super().remove_person_from_location(person_id)
