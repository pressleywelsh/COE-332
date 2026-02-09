from models import MeteoriteLanding, compute_average_mass
import pytest

ml1 = MeteoriteLanding(**{"name": 'Meteor1', "id": 1, "recclass": 'L5', "mass (g)": 3, "reclat": 50.775, "reclong": 6.08333})
ml2 = MeteoriteLanding(**{"name": 'Meteor2', "id": 2, "recclass": 'L5', "mass (g)": 7, "reclat": -50.775, "reclong": 6.08333})
ml3 = MeteoriteLanding(**{"name": 'Meteor3', "id": 3, "recclass": 'L5', "mass (g)": 11, "reclat": -50.775, "reclong": 6.08333})

def test_compute_average_mass():
   assert (compute_average_mass([ml1, ml2]) == 5.0)
   assert (compute_average_mass([ml1, ml3]) == 7.0)
   assert (compute_average_mass([ml1, ml2, ml3]) == 7.0)

def test_compute_average_mass_exceptions():
   assert compute_average_mass([]) == 0.0
   with pytest.raises(AttributeError):
      compute_average_mass(["foo"])

