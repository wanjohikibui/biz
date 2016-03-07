import os
from django.contrib.gis.utils import LayerMapping
from permit.models import Parcels

# Auto-generated `LayerMapping` dictionary for administration model
parcels_mapping = {
    'id' : 'id',
    'blockid' : 'blockid',
    'sectcode' : 'sectcode',
    'parcel_no' : 'parcel_no',
    'geom' : 'MULTIPOLYGON',
}

parcels_shp = os.path.abspath(os.path.join(os.path.dirname(__file__), '../permit/data/parcels.shp'))

def run(verbose=True):
    lm = LayerMapping(Parcels, parcels_shp,parcels_mapping,transform=True, encoding='iso-8859-1')
    lm.save(strict=True, verbose=verbose)