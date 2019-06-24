from django.shortcuts import render
from lxml import etree

import requests
import json
import zipfile
import io
import os

list_api = "https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date={target}&type=2"
file_api = "https://disclosure.edinet-fsa.go.jp/api/v1/documents/{document_id}?type=1"

def corporate_officer_list(request):
    return render(request, 'edinet/corporate_officer_list.html', {})

def call_edinet_api(request):

    print(os.getcwd())

    for result in get_results("2018-06-19"):
        if result["edinetCode"] == "E01777" and "有価証券" in result["docDescription"]:
            document_id = result["docID"]
            url = file_api.format(document_id=document_id)
            r = requests.get(url)

            zip = zipfile.ZipFile(io.BytesIO(r.content))
            zip.extractall()

            file = os.getcwd() + "\XBRL\PublicDoc\jpcrp030000-asr-001_E01777-000_2018-03-31_01_2018-06-19.xbrl"
            data = get_information_about_officers_text(file)
            print(data.text)
            
    return render(request, 'edinet/corporate_officer_list.html', {})

def get_information_about_officers_text(file):
    root = read_xml_lxml_etree(file)
    namespace = root.nsmap['jpcrp_cor']
    tag = 'InformationAboutOfficersTextBlock'
    attr = 'contextRef'
    value = 'FilingDateInstant'

    xpath = './/{%s}%s[@%s="%s"]' % (namespace, tag, attr, value)
    data = root.find(xpath)

    return data

def read_xml_lxml_etree(file):
    with open(file, 'rb') as f:
        return etree.fromstring(f.read())

def get_results(target):

    url = list_api.format(target=target)
    r = requests.get(url)
    data = json.loads(r.text)
    results = data["results"]

    return results
