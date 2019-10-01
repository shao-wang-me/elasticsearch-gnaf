# Import-G-NAF-dataset-into-Elasticsearch
Python scripts and Jupyter notebooks to import G-NAF dataset into Elasticsearch using MongoDB along with a script to generate dummy Australian demographic data and import it into Elasticsearch.

The [Geocoded National Address File](https://data.gov.au/dataset/ds-dga-19432f89-dc3a-4ef3-b943-5326ef1dbecc/) (referred to as G-NAF) is Australia’s authoritative, geocoded address file. It is produced by PSMA Australia and on [their page for GNAF](https://psma.com.au/product/gnaf/), there is a [Getting Started Guide](https://psma.com.au/wp-content/uploads/2019/06/G-NAF-Getting-Started-Guide-New.pdf). You can follow the steps in the guide to import G-NAF into a relational database.

`copy_gnaf_to_postgres.ipynb` generates PostgreSQL's COPY command to import the files into Postgres. Just copy the generated command and use in PostgreSQL.

`elastic_gnaf.py` imports G-NAF from postgres to Elasticsearch.

`elastic_australian_people.py` is not related to G-NAF, but generates dummy Australian demographic data and imports it into Elasticsearch, if you need. :blush:

## See also
1. [data61/gnaf](https://github.com/data61/gnaf): A set of utilities developed by CSIRO's Data61 to import G-NAF into a relational database, establish a Apache Lucence (which Elasticsearch uses under the hood) index and many other things.
1. [Building real-time address search with the Australian G-NAF dataset](https://www.elastic.co/blog/realtime-address-search-with-australian-gnaf): A blog from Elastic with a similar goal as this repository but uses Microsoft F#.
1. [aus-search](https://github.com/matthaywardwebdesign/aus-search): Uses Node.js and MongoDB to import G-NAF into Elasticsearch.