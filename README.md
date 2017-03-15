# Asset Store created using Swagger

## Overview
This server was generated by the [swagger-codegen](https://github.com/swagger-api/swagger-codegen) project.

This example uses the [Connexion](https://github.com/zalando/connexion) library on top of Flask.

The REST API is defined using Swagger and can be viewed at /api/ui endpoint.

Used Cuckoo Filter to check if the name is already present in the system. Cuckoo Filter is a highly space and time efficient probabilistic data structure that is used to check for set membership. It takes about 7 bits per entry with 0% False Negative rate and about 3% False positive rate. It can thought of as an high speed cache and be used to reduce up database reads. [More Info](https://bdupras.github.io/filter-tutorial/).

Did not implement database functionality as data persistence was not a key point.


To run the server, please execute the following from the project root directory:


```
pip3 install -r requirements.txt
python3 -m swagger_server

```

or

```
sudo docker build -t assetStore .
sudo docker run -p 8080:8080 assetStore
```

and open your browser to here:

```
http://localhost:8080/api/ui/
```

Your Swagger definition lives here:

```
http://localhost:8080/api/swagger.json
```

To launch the integration tests, use tox:
```
sudo pip install tox
tox
```