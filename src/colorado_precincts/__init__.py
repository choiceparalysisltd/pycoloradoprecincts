from dataclasses import dataclass
from enum import Enum
from functools import cache, cached_property


@dataclass
class County:
    """A dataclass representing a county's name and ID number"""

    id: int
    name: str


class Counties(Enum):
    """A mapping of all the counties in Colorado"""

    @classmethod
    @cache
    def get_by_id(cls, county_id: int) -> County:
        """Retrieve a county by its ID number"""
        for county in cls:
            if county_id == county.value.id:
                return county.value
        raise KeyError(f"No county exists with id={county_id}")

    ADAMS = County(id=1, name="Adams")
    ALAMOSA = County(id=2, name="Alamosa")
    ARAPAHOE = County(id=3, name="Arapahoe")
    ARCHULETA = County(id=4, name="Archuleta")
    BACA = County(id=5, name="Baca")
    BENT = County(id=6, name="Bent")
    BOULDER = County(id=7, name="Boulder")
    CHAFFEE = County(id=8, name="Chaffee")
    CHEYENNE = County(id=9, name="Cheyenne")
    CLEAR_CREEK = County(id=10, name="Clear Creek")
    CONEJOS = County(id=11, name="Conejos")
    COSTILLA = County(id=12, name="Costilla")
    CROWLEY = County(id=13, name="Crowley")
    CUSTER = County(id=14, name="Custer")
    DELTA = County(id=15, name="Delta")
    DENVER = County(id=16, name="Denver")
    DOLORES = County(id=17, name="Dolores")
    DOUGLAS = County(id=18, name="Douglas")
    EAGLE = County(id=19, name="Eagle")
    ELBERT = County(id=20, name="Elbert")
    EL_PASO = County(id=21, name="El Paso")
    FREMONT = County(id=22, name="Fremont")
    GARFIELD = County(id=23, name="Garfield")
    GILPIN = County(id=24, name="Gilpin")
    GRAND = County(id=25, name="Grand")
    GUNNISON = County(id=26, name="Gunnison")
    HINSDALE = County(id=27, name="Hinsdale")
    HUERFANO = County(id=28, name="Huerfano")
    JACKSON = County(id=29, name="Jackson")
    JEFFERSON = County(id=30, name="Jefferson")
    KIOWA = County(id=31, name="Kiowa")
    KIT_CARSON = County(id=32, name="Kit Carson")
    LA_PLATA = County(id=33, name="La Plata")
    LAKE = County(id=34, name="Lake")
    LARIMER = County(id=35, name="Larimer")
    LAS_ANIMAS = County(id=36, name="Las Animas")
    LINCOLN = County(id=37, name="Lincoln")
    LOGAN = County(id=38, name="Logan")
    MESA = County(id=39, name="Mesa")
    MINERAL = County(id=40, name="Mineral")
    MOFFAT = County(id=41, name="Moffat")
    MONTEZUMA = County(id=42, name="Montezuma")
    MONTROSE = County(id=43, name="Montrose")
    MORGAN = County(id=44, name="Morgan")
    OTERO = County(id=45, name="Otero")
    OURAY = County(id=46, name="Ouray")
    PARK = County(id=47, name="Park")
    PHILLIPS = County(id=48, name="Phillips")
    PITKIN = County(id=49, name="Pitkin")
    PROWERS = County(id=50, name="Prowers")
    PUEBLO = County(id=51, name="Pueblo")
    RIO_BLANCO = County(id=52, name="Rio Blanco")
    RIO_GRANDE = County(id=53, name="Rio Grande")
    ROUTT = County(id=54, name="Routt")
    SAGUACHE = County(id=55, name="Saguache")
    SAN_JUAN = County(id=56, name="San Juan")
    SAN_MIGUEL = County(id=57, name="San Miguel")
    SEDGWICK = County(id=58, name="Sedgwick")
    SUMMIT = County(id=59, name="Summit")
    TELLER = County(id=60, name="Teller")
    WASHINGTON = County(id=61, name="Washington")
    WELD = County(id=62, name="Weld")
    YUMA = County(id=63, name="Yuma")
    BROOMFIELD = County(id=64, name="Broomfield")


@dataclass
class PrecinctId:
    """A dataclass which "explodes" a 10-digit precinct number into its component fields"""

    raw_id: int

    @cached_property
    def precinct(self) -> int:
        """The short precinct number"""
        return self.raw_id % 1000

    @cached_property
    def county(self) -> County:
        """The county containing this precinct"""
        county_id = (self.raw_id // 1_000) % 100
        return Counties.get_by_id(county_id)

    @cached_property
    def congressional_district(self) -> int:
        """The district number for the federal House of Representatives"""
        return self.raw_id // 1_000_000_000

    @cached_property
    def state_senate_district(self) -> int:
        """The district number for the state Senate"""
        return (self.raw_id // 10_000_000) % 100

    @cached_property
    def state_house_district(self) -> int:
        """The district number for the state House of Representatives"""
        return (self.raw_id // 100_000) % 100

    @cached_property
    def ward(self) -> int:
        """The ward number, if applicable.

        Only Broomfield county has wards. For all other counties, this will raise a `ValueError`."""
        if self.county is not Counties.BROOMFIELD.value:
            raise ValueError("Only Broomfield County has wards")
        return self.precinct // 100

    @cached_property
    def county_commissioner_district(self) -> int:
        """The county commissioner district, if applicable and supported.

        Most counties do not have commissioner districts, and this will raise a `ValueError` if not applicable.

        El Paso County does have commissioner districts, but the logic for them is complex and not yet supported by this package.
        This function will raise a `NotImplementedError` for precincts in El Paso County."""
        if self.precinct < 100 or self.county in [
            Counties.BROOMFIELD.value,
            Counties.DENVER.value,
        ]:
            raise ValueError(
                "This precinct is not associated with a county commissioner district"
            )
        if self.county is Counties.EL_PASO.value:
            raise NotImplementedError(
                "County commissioner districts are not yet supported for El Paso County"
            )
        return self.precinct % 100
