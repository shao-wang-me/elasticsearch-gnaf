from time import sleep

import psycopg2
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk


class Address:
    _fields = [
        'address_detail_pid',
        'street_locality_pid',
        'locality_pid',
        'building_name',
        'lot_number_prefix',
        'lot_number',
        'lot_number_suffix',
        'flat_type',
        'flat_number_prefix',
        'flat_number',
        'flat_number_suffix',
        'level_type',
        'level_number_prefix',
        'level_number',
        'level_number_suffix',
        'number_first_prefix',
        'number_first',
        'number_first_suffix',
        'number_last_prefix',
        'number_last',
        'number_last_suffix',
        'street_name',
        'street_class_code',
        'street_class_type',
        'street_type_code',
        'street_suffix_code',
        'street_suffix_type',
        'locality_name',
        'state_abbreviation',
        'postcode',
        'latitude',
        'longitude',
        'geocode_type',
        'confidence',
        'alias_principal',
        'primary_secondary',
        'legal_parcel_id',
        'date_created'
    ]

    def __init__(self, address_tuple):
        self._dict = dict(zip(self._fields, address_tuple))

        if self._dict['flat_number']: self._dict['flat_number'] = int(self._dict['flat_number'])
        if self._dict['level_number']: self._dict['level_number'] = int(self._dict['level_number'])
        if self._dict['number_first']: self._dict['number_first'] = int(self._dict['number_first'])
        if self._dict['number_last']: self._dict['number_last'] = int(self._dict['number_last'])
        if self._dict['postcode']: self._dict['postcode'] = int(self._dict['postcode'])
        if self._dict['confidence']: self._dict['confidence'] = int(self._dict['confidence'])

        self._convert_geo_coordinates()

    def _convert_geo_coordinates(self):
        self._dict['geo_coordinates'] = [self._dict['longitude'], self._dict['latitude']]
        del self._dict['latitude'],
        del self._dict['longitude']

    def as_dict(self):
        return self._dict


def addresses(dbname, user, password, index_name):
    conn = psycopg2.connect(dbname=dbname, user=user, password=password)
    cur = conn.cursor(name='nice_view')

    cur.execute('SELECT * FROM address_view LIMIT 5000')

    for address_tuple in cur:
        address = Address(address_tuple).as_dict()
        yield {
            '_index': index_name,
            '_op_type': 'create',
            '_id': address['address_detail_pid'],
            '_source': address
        }

    cur.close()
    conn.close()


if __name__ == '__main__':
    ELASTIC_HOST = 'localhost:9200'
    INDEX = 'address'

    DB_NAME = 'postgres'
    USER = 'postgres'
    PASSWORD = '5454'

    es = Elasticsearch(hosts=[ELASTIC_HOST])

    mappings = {
        'mappings': {
            'properties': {
                'geo_coordinates': {
                    'type': 'geo_point'
                }
            }
        }
    }
    settings = {
        'settings': {
            'index': {
                'number_of_shards': '1',
                'number_of_replicas': '0',
                'blocks': {
                    'read_only_allow_delete': 'true'
                }
            }
        }
    }
    index = {**mappings, **settings}

    if es.indices.exists(INDEX):
        res = es.indices.delete(INDEX)
        print(res)
        sleep(5)
    res = es.indices.create(index=INDEX, body=index)
    print(res)

    res = bulk(
        client=es,
        actions=addresses(dbname=DB_NAME, user=USER, password=PASSWORD, index_name=INDEX),
        stats_only=False,
        raise_on_error=False
    )
    print(res)
