# Python library for parsing Colorado precinct IDs

Decodes the precinct ID associated with a voter's address, to discover their legislative districts and other data.

```pycon
>>> from colorado_precincts import PrecinctId
>>> my_precinct = PrecinctId(7253364413)
>>> my_precinct.congressional_district
7
>>> my_precinct.state_house_district
33
>>> my_precinct.state_senate_district
25
>>> my_precinct.county
County(id=64, name='Broomfield')
>>> my_precinct.ward
4
>>> 
```