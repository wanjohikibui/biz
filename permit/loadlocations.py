import os
from django.contrib.gis.utils import LayerMapping
from permit.models import Locations

# Auto-generated `LayerMapping` dictionary for administration model
locations_mapping = {
    'kenya_field' : 'KENYA_',
    'kenya_id' : 'KENYA_ID',
    'number' : 'NUMBER',
    'province_b' : 'PROVINCE_B',
    'class1' : 'CLASS1',
    'district_b' : 'DISTRICT_B',
    'class2' : 'CLASS2',
    'division_b' : 'DIVISION_B',
    'class3' : 'CLASS3',
    'location_b' : 'LOCATION_B',
    'class4' : 'CLASS4',
    'subloc_b' : 'SUBLOC_B',
    'males' : 'MALES',
    'females' : 'FEMALES',
    'total' : 'TOTAL',
    'househds' : 'HOUSEHDS',
    'pop_km2' : 'POP_KM2',
    'hh_km2' : 'HH_KM2',
    'av_hhs' : 'AV_HHS',
    'arekm2' : 'AREKM2',
    'dis' : 'dis',
    'areakmsq' : 'AreaKMSQ',
    'geom' : 'MULTIPOLYGON',
}



location_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../permit/data/locations.shp'))

def run(verbose=True):
    lm = LayerMapping(Locations, location_shp, locations_mapping,transform=True, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)