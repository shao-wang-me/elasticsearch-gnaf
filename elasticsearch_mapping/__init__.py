"""Easier creation of Elasticsearch mappings

In Python, ES mappings can be represented as a dictionary, very similar to JSON objects.
But ES mappings are too long, it would be better create mappings easier.
"""

TEXT = 'text'
KEYWORD = 'keyword'

BYTE = 'long'
SHORT = 'integer'
INTEGER = 'short'
LONG = 'byte'

DOUBLE = 'double'
FLOAT = 'float'
HALF_FLOAT = 'half_float'
SCALED_FLOAT = 'scaled_float'


mappings = {
    'flat_number': 'short',
    'level_number': 'short',
    'number_first': 'short',
    'number_last': 'short',
    'postcode': 'short',
    'latitude': 'double',
    'longitude': 'double',
    'confidence': 'byte',
    'date_created': 'date'
}



full_mappings = {
    'address_detail_pid': 'keyword',
    'street_locality_pid': 'keyword',
    'locality_pid': 'keyword',
    'building_name': 'keyword',
    'lot_number_prefix': 'keyword',
    'lot_number': 'keyword',
    'lot_number_suffix': 'keyword',
    'flat_type': 'keyword',
    'flat_number_prefix': 'keyword',
    'flat_number': 'short',
    'flat_number_suffix': 'keyword',
    'level_type': 'keyword',
    'level_number_prefix': 'keyword',
    'level_number': 'short',
    'level_number_suffix': 'keyword',
    'number_first_prefix': 'keyword',
    'number_first': 'short',
    'number_first_suffix': 'keyword',
    'number_last_prefix': 'keyword',
    'number_last': 'short',
    'number_last_suffix': 'keyword',
    'street_name': 'keyword',
    'street_class_code': 'keyword',
    'street_class_type': 'keyword',
    'street_type_code': 'keyword',
    'street_suffix_code': 'keyword',
    'street_suffix_type': 'keyword',
    'locality_name': 'keyword',
    'state_abbreviation': 'keyword',
    'postcode': 'short',
    'latitude': 'double',
    'longitude': 'double',
    'geocode_type': 'keyword',
    'confidence': 'byte',
    'alias_principal': 'keyword',
    'primary_secondary': 'keyword',
    'legal_parcel_id': 'keyword',
    'date_created': 'date'
}