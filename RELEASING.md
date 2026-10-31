# Releasing the GeLaTo clld app

Clone and install the app:
```shell
git clone --branch v1.0.1 --depth 1 https://github.com/gelato-org/gelato-data
git clone https://github.com/clld/gelato
cd gelato
pip install -e .[test]
```

Recreate the database and run the test suite:
```shell
clld initdb development.ini --cldf ../gelato-data/cldf/StructureDataset-metadata.json
pytest
```

Store the tested requirements:
```shell
pip freeze > requirements.txt
```

Store a db dump:
```shell
pg_dump -xO --compress gzip:9 gelato > gelato.sql.gz
```

