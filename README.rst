==========================
termstore-service
==========================

A Python micro service for getting terms from a SharePoint 2010/2013 termstore.

The service listens on port 5000. JSON entities can be retrieved from 'http://localhost:5000/entities'.

Example system configuration:
::

  {
    "_id": "termstore-service-example",
    "type": "system:microservice",
    "docker": {
      "environment": {
        "DEBUG": "True",
        "LCID": "1033",
        "PASS": "$SECRET(password)",
        "SSPIDS": "793bb2cf-49e4-4786-a8fa-390226915d1",
        "TSIDS": "eb7880be-f44e-45bf-9442-aeec70fa312d",
        "USER": "domain\\user",
        "WSDL": "http://sharepoint/_vti_bin/TaxonomyClientService.asmx?wsdl"
      },
      "image": "sesam-io/termstore-service",
      "port": 5000
    }
  }

::

The following output is from a simple termset called countries with the following structure:

Countries
  Asia
    China
  Europe
    Norway

::

  curl -s 'http://localhost:5000/entities' | python3 -m json.tool
  [
      {
          "label_path": "",
          "default_label": "Europe",
          "labels": [
              "Europe"
          ],
          "termset_name": "Countries",
          "termset_id": "becaf3fc-2f98-40e1-a161-663789913dd3",
          "id_path": "93c9c293-e9f1-4b32-8aa1-743cde0c8c3a",
          "_id": "93c9c293-e9f1-4b32-8aa1-743cde0c8c3a"
      },
      {
          "label_path": "",
          "default_label": "Asia",
          "labels": [
              "Asia"
          ],
          "termset_name": "Countries",
          "termset_id": "becaf3fc-2f98-40e1-a161-663789913dd3",
          "id_path": "776db12b-af73-469f-bb74-328d501bfacc",
          "_id": "776db12b-af73-469f-bb74-328d501bfacc"
      },
      {
          "label_path": "Europe",
          "default_label": "Norway",
          "labels": [
              "Norway"
          ],
          "termset_name": "Countries",
          "termset_id": "becaf3fc-2f98-40e1-a161-663789913dd3",
          "id_path": "93c9c293-e9f1-4b32-8aa1-743cde0c8c3a;628aa0d6-8b86-4844-9864-dbcc06ac4dce",
          "_id": "628aa0d6-8b86-4844-9864-dbcc06ac4dce"
      },
      {
          "label_path": "Asia",
          "default_label": "China",
          "labels": [
              "China"
          ],
          "termset_name": "Countries",
          "termset_id": "becaf3fc-2f98-40e1-a161-663789913dd3",
          "id_path": "776db12b-af73-469f-bb74-328d501bfacc;3d3520ca-2d88-4d6c-988d-783c41bc3e6a",
          "_id": "3d3520ca-2d88-4d6c-988d-783c41bc3e6a"
      }
  ]

::

The following properties are returned:

_id
  Identifier of term.
default_label
  The default term label.
labels
  This is the collection of term labels that this term contains.
label_path
  Term label path of term with term labels. This path starts from the root term and goes until the parent of the term.
id_path
  Term label path of term with identifiers. This path starts from the root term and goes until the term itself.
termset_id
  Identifier of term set.
termset_name
  Term set name in the language requested by the client. If the term set does not have a name in the client’s language, the name in the term store default language is returned.
