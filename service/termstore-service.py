import os

import zeep
from requests import Session
from zeep import Client
from zeep.transports import Transport
from requests_ntlm import HttpNtlmAuth
from lxml import etree

from flask import Flask, request, Response
import json

import logging.config

app = Flask(__name__)

@app.route('/entities')
def get_entities():
    #number of sharedServiceIds must equal number of termsetIds
    #https://msdn.microsoft.com/en-us/library/dd774335%28v=office.12%29.aspx
    if(len(sspIds) != len(tsIds)):
        return Response("The number of sharedServiceIds must equal number of termsetIds", mimetype="text/plain", status=400)

    sharedServiceIds = _build_sspIds(sspIds)
    termSetIds = _build_termSetIds(tsIds)
    clientVersions = _build_clientVersions(len(tsIds))
    clientTimeStamps = _build_clientTimeStamps(len(tsIds))

    session = Session()
    session.auth = HttpNtlmAuth(user, password)
    client = Client(wsdl, transport=Transport(session=session))
    res = client.service.GetTermSets(lcid=lcid, sharedServiceIds=sharedServiceIds, termSetIds=termSetIds, clientVersions=clientVersions, clientTimeStamps=clientTimeStamps)
    root = etree.fromstring(zeep.helpers.serialize_object(res)['GetTermSetsResult'])

    # Description of xml format
    # https://msdn.microsoft.com/en-us/library/dd930727(v=office.12).aspx
    # https://msdn.microsoft.com/en-us/library/dd904799(v=office.12).aspx

    entities = []
    terms = root.xpath('/Container/TermStore/T')
    for term in terms:
        entities.append(
            {"_id": term.get('a9'),
             "default_label": next(iter(term.xpath('LS/TL[@a31 = "true"]/@a32')),None),
             "labels": term.xpath('LS/TL/@a32'),
             "id_path": next(iter(term.xpath('TMS/TM/@a45')), None),
             "label_path": next(iter(term.xpath('TMS/TM/@a40')), None),
             "termset_id": next(iter(term.xpath('TMS/TM/@a24')), None),
             "termset_name": next(iter(term.xpath('TMS/TM/@a12')), None)
             })
    return Response(json.dumps(entities), mimetype='application/json')


def _build_sspIds(sspIds):
    root = etree.Element('sspIds')
    for sspId in sspIds:
        subelement = etree.SubElement(root, 'sspId')
        subelement.text = sspId

    return etree.tostring(root)


def _build_termSetIds(termSetIds):
    root = etree.Element('termSetIds')
    for termSetId in termSetIds:
        subelement = etree.SubElement(root, 'termSetId')
        subelement.text = termSetId

    return etree.tostring(root)


def _build_clientVersions(count):
    root = etree.Element('versions')
    for x in range(0, count):
        subelement = etree.SubElement(root, 'version')
        #Version should alway be 0
        #https://msdn.microsoft.com/en-us/library/dd774335%28v=office.12%29.aspx
        subelement.text = "0"

    return etree.tostring(root)


def _build_clientTimeStamps(count):
    root = etree.Element('dateTimes')
    for x in range(0, count):
        subelement = etree.SubElement(root, 'dateTime')
        #Timestamp should alway be 1900-01-01T00:00:00 to get all
        #https://msdn.microsoft.com/en-us/library/dd774335%28v=office.12%29.aspx
        subelement.text = "1900-01-01T00:00:00"

    return etree.tostring(root)


if __name__ == '__main__':
    user = os.environ.get("USER")
    password = os.environ.get("PASSWORD")
    lcid  = os.environ.get("LCID")
    wsdl = os.environ.get("WSDL")
    sspIds = os.environ.get("SSPIDS").split(";")
    tsIds = os.environ.get("TSIDS").split(";")

    debug = os.environ.get("DEBUG")

    #set up logging for zeep
    if debug == True:
        logging.config.dictConfig({
            'version': 1,
            'formatters': {
                'verbose': {
                    'format': '%(name)s: %(message)s'
                }
            },
            'handlers': {
                'console': {
                    'level': 'DEBUG',
                    'class': 'logging.StreamHandler',
                    'formatter': 'verbose',
                },
            },
            'loggers': {
                'zeep.transports': {
                    'level': 'DEBUG',
                    'propagate': True,
                    'handlers': ['console'],
                },
            }
        })

    app.run(debug=debug, host='0.0.0.0')
