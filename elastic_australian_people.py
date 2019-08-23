"""A script to generate fake Australian demographic data, and index into Elasticsearch.

Python requirements:
    * elasticsearch
    * faker
Elasticsearch requirements:
    * phonetic plugin
    * name_synonyms.txt in elasticsearch-<version>/config/

Author: Shao Wang
Date: 2019-08-22
"""

from datetime import datetime
from time import sleep

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from faker import Faker
from faker.providers.address.en_AU import Provider as AddressProvider
from faker.providers.person.en import Provider as EnglishPersonProvider


class AddressProviderAU(AddressProvider):
    """Override street_address_formats to get a single line street address
    """
    street_address_formats = (
        '{{building_number}} {{street_name}}',
        '{{secondary_address}} {{building_number}} {{street_name}}',
    )


def people(population, people_generator, index_name):
    for _ in range(population):
        person = {
            'id': people_generator.random_number(digits=10, fix_len=10),
            'first_name': people_generator.first_name(),
            'last_name': people_generator.last_name(),
            'gender': people_generator.random_element(elements=('M', 'F')),
            'dob': people_generator.date_of_birth().isoformat(),
            'address': people_generator.street_address(),
            'suburb': people_generator.city(),
            'state': people_generator.state_abbr(),
            'postcode': people_generator.postcode(),
            '@timestamp': datetime.now()
        }
        yield {
            '_index': index_name,
            '_op_type': 'create',
            '_id': person['id'],
            '_source': person
        }


if __name__ == '__main__':

    POPULATION = 5000000
    ELASTIC_HOST = 'localhost:9200'
    INDEX = 'people-aus'

    # Elasticsearch client
    es = Elasticsearch(hosts=[ELASTIC_HOST])

    # create index
    mappings = {
        "mappings": {
            "properties": {
                "@timestamp": {"type": "date"},
                "address": {"type": "text", "term_vector": "yes", "fields": {"keyword": {"type": "keyword", "ignore_above": 256}}},
                "dob": {"type": "date", "fields": {"keyword": {"type": "keyword"}, "text": {"type": "text", "term_vector": "yes"}}},
                "gender": {"type": "keyword"},
                "id": {"type": "long", "fields": {"keyword": {"type": "keyword"}, "text": {"type": "text", "term_vector": "yes"}}},
                "first_name": {"type": "text", "term_vector": "yes", "fields": {"keyword": {"type": "keyword"}, "phones": {"type": "text", "term_vector": "yes", "analyzer": "phonetic"}, "synonym": {"type": "text", "term_vector": "yes", "analyzer": "name_synonym"}}},
                "last_name": {"type": "text", "term_vector": "yes", "fields": {"keyword": {"type": "keyword"}, "phones": {"type": "text", "term_vector": "yes", "analyzer": "phonetic"}, "synonym": {"type": "text", "term_vector": "yes", "analyzer": "name_synonym"}}},
                "postcode": {"type": "short", "fields": {"keyword": {"type": "keyword"}, "text": {"type": "text", "term_vector": "yes"}}},
                "suburb": {"type": "text", "term_vector": "yes", "fields": {"keyword": {"type": "keyword"}}},
                "state": {"type": "text", "term_vector": "yes", "fields": {"keyword": {"type": "keyword"}}}
            }
        }
    }
    settings = {
        "settings": {
            "index": {
                "number_of_shards": "1",
                "number_of_replicas": "0",
                "analysis": {
                    "filter": {
                        "name_synonym": {"type": "synonym", "synonyms_path": "name_synonyms.txt", "expand": "true"},
                        "phonetic": {"type": "phonetic"}
                    },
                    "analyzer": {
                        "name_synonym": {"filter": ["lowercase", "name_synonym"], "type": "custom",
                                         "tokenizer": "standard"},
                        "phonetic": {"filter": ["lowercase", "phonetic"], "type": "custom", "tokenizer": "standard"}
                    }
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

    # create Australia demographic data generator
    au = Faker('en_AU')
    # use our own derived provider to get street address in a single line
    au.add_provider(AddressProviderAU)
    # use faker.providers.person.en.Provider to get more names
    au.add_provider(EnglishPersonProvider)
    au.seed(12)

    # generate Australian people and bulk index them into Elasticsearch
    res = bulk(es, people(POPULATION, au, INDEX), stats_only=True, raise_on_error=False)
    print(res)
