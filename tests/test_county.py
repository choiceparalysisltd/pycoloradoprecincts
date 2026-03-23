import pytest

from src.colorado_precincts import Counties, PrecinctId


def test_get_county():
    county = Counties.get_by_id(64)
    assert county.id == 64
    assert county.name == "Broomfield"


def test_parse_precinct_fields():
    precinct = PrecinctId(7253364413)
    assert precinct.congressional_district == 7
    assert precinct.state_senate_district == 25
    assert precinct.state_house_district == 33
    assert precinct.county.name == "Broomfield"
    assert precinct.county.id == 64
    assert precinct.precinct == 413
    assert precinct.ward == 4

    with pytest.raises(ValueError):
        _ = precinct.county_commissioner_district