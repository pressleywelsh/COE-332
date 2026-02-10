from ml_data_analysis import GeoLocation, MeteoriteLanding, compute_average_mass, check_hemisphere, count_classes
import pytest

ml1 = MeteoriteLanding(**{"name": "Ruiz",
      "id": "10001",
      "recclass": "L5",
      "mass (g)": "21",
      "reclat": "50.775",
      "reclong": "6.08333",
      "GeoLocation": "(50.775, 6.08333)"})
ml2 = MeteoriteLanding(**{"name": "Beeler",
      "id": "10002",
      "recclass": "H6",
      "mass (g)": "720",
      "reclat": "56.18333",
      "reclong": "10.23333",
      "GeoLocation": "(56.18333, 10.23333)"})
ml3 = MeteoriteLanding(**{"name": "Brock",
      "id": "10003",
      "recclass": "EH4",
      "mass (g)": "107000",
      "reclat": "54.21667",
      "reclong": "-113",
      "GeoLocation": "(54.21667, -113.0)"})
ml4 = MeteoriteLanding(**{"name": "Hillebrand",
      "id": "10004",
      "recclass": "Acapulcoite",
      "mass (g)": "1914",
      "reclat": "16.88333",
      "reclong": "-99.9",
      "GeoLocation": "(16.88333, -99.9)"})
ml5 = MeteoriteLanding(**{"name": "Mitchell",
      "id": "10005",
      "recclass": "L6",
      "mass (g)": "780",
      "reclat": "-33.16667",
      "reclong": "-64.95",
      "GeoLocation": "(-33.16667, -64.95)"})
ml6 = MeteoriteLanding(**{"name": "Ortiz",
      "id": "10006",
      "recclass": "EH4",
      "mass (g)": "4239",
      "reclat": "32.1",
      "reclong": "71.8",
      "GeoLocation": "(32.1, 71.8)"})

def test_compute_average_mass():
   assert (compute_average_mass([ml1, ml2]) == 370.5)
   assert (compute_average_mass([ml1, ml3]) == 53510.5)
   assert (compute_average_mass([ml1, ml2, ml3]) == 27413.75)

def test_compute_average_mass_exceptions():
   assert compute_average_mass([]) == 0.0
   with pytest.raises(AttributeError):
      compute_average_mass(["foo"])

def test_check_hemisphere():
    assert(check_hemisphere(ml1) == 'Northern & Eastern')
    assert(check_hemisphere(ml5) == 'Southern & Western')
    assert(check_hemisphere(ml2) != 'Southern & Eastern')

def test_check_hemisphere_exceptions():
    with pytest.raises(AttributeError):
        check_hemisphere("foo")

def test_count_classes():
    result = count_classes(landings)
    assert (result['EH4'] == 2)
    assert (result['L6'] == 1)
    assert (result['Acapulcoite'] != 2)

def test_count_classes_exceptions():
    with pytest.raises(AttributeError):
        count_classes(["foo"])
