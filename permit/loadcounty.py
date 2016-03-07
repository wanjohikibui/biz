import os
from django.contrib.gis.utils import LayerMapping
from permit.models import County

# Auto-generated `LayerMapping` dictionary for administration model
county_mapping = {
    'name2' : 'NAME2',
    'count' : 'COUNT',
    'geom' : 'MULTIPOLYGON',
}

county_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../permit/data/county.shp'))

def run(verbose=True):
    lm = LayerMapping(County, county_shp, county_mapping,transform=True, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)