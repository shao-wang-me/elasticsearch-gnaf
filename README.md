# Import-G-NAF-dataset-into-Elasticsearch
Python scripts and Jupyter notebooks to import G-NAF dataset into Elasticsearch.

The [Geocoded National Address File](https://data.gov.au/dataset/ds-dga-19432f89-dc3a-4ef3-b943-5326ef1dbecc/) (referred to as G-NAF) is Australia’s authoritative, geocoded address file. It is produced by PSMA Australia and on [their page for GNAF](https://psma.com.au/product/gnaf/), there is a [Getting Started Guide](https://psma.com.au/wp-content/uploads/2019/06/G-NAF-Getting-Started-Guide-New.pdf). You can follow the steps in the guide to import G-NAF into a relational database.

`copy_gnaf_to_postgres.ipynb` generates PostgreSQL's COPY command to import the files into Postgres.

`elastic_gnaf.py` imports G-NAF from postgres to Elasticsearch.

`elastic_australian_people.py` is not related to G-NAF, but generates some dummy Australian demographic data and imports them into Elasticsearch, if you need. :blush:
