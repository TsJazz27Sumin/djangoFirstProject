from django.shortcuts import render
from lxml import etree
from bs4 import BeautifulSoup
from edinet.models import CorporateOfficer

import requests
import json
import zipfile
import io
import os
import re

list_api = "https://disclosure.edinet-fsa.go.jp/api/v1/documents.json?date={target}&type=2"
file_api = "https://disclosure.edinet-fsa.go.jp/api/v1/documents/{document_id}?type=1"
number_translate_dictionary = {"０":"0","１":"1","２":"2","３":"3","４":"4","５":"5","６":"6","７":"7","８":"8","９":"9"}
trans_table = str.maketrans(number_translate_dictionary)

def corporate_officer_list(request):
    context = {'corporate_officer_list': list(), 'corporate_officer_list_count': 0}
    return render(request, 'edinet/corporate_officer_list.html', context)

def call_edinet_api(request):

    for result in get_results("2018-06-19"):
        if result["edinetCode"] == "E01777" and "有価証券" in result["docDescription"]:
            document_id = result["docID"]
            url = file_api.format(document_id=document_id)
            r = requests.get(url)

            zip = zipfile.ZipFile(io.BytesIO(r.content))
            zip.extractall()

            file = os.getcwd() + r"\XBRL\PublicDoc\jpcrp030000-asr-001_E01777-000_2018-03-31_01_2018-06-19.xbrl"
            data = get_information_about_officers_text(file)
            soup = BeautifulSoup(data.text)

            corporate_officer_list = get_corporate_officer_list(soup)          

    context = {'corporate_officer_list': corporate_officer_list, 'corporate_officer_list_count': len(corporate_officer_list)}
                               
    return render(request, 'edinet/corporate_officer_list.html', context)

def reload(request):

    file = os.getcwd() + r"\XBRL\PublicDoc\jpcrp030000-asr-001_E01777-000_2018-03-31_01_2018-06-19.xbrl"
    data = get_information_about_officers_text(file)
    soup = BeautifulSoup(data.text)
    corporate_officer_list = get_corporate_officer_list(soup)  
    
    context = {'corporate_officer_list': corporate_officer_list, 'corporate_officer_list_count': len(corporate_officer_list)}
                               
    return render(request, 'edinet/corporate_officer_list.html', context)

def get_corporate_officer_list(soup):

    corporate_officer_list = list()

    for table in soup.find_all("table"):
        for tableChild in table.children:

            if tableChild.name == "tbody":
                for tr in tableChild.children:

                    if tr.name == "tr":
                        column_value_list = list()

                        if len(tr.find_all("td")) > 7:
                            for trChild in tr.children:
                                if trChild.name == "td":
                                    column_value_list.append(trChild.get_text().replace('\n', '/'))

                        if len(column_value_list) > 0:
                            corporate_officer = create_corporate_officer(column_value_list)
                            corporate_officer_list.append(corporate_officer)
    
    return corporate_officer_list

def create_corporate_officer(column_value_list):
    corporate_officer = CorporateOfficer()

    if len(column_value_list) > 0:
        corporate_officer.position = process_item(column_value_list[0]).replace("/","")
    
    if len(column_value_list) > 1:
        corporate_officer.job = process_item(column_value_list[1]).replace("/","")
    
    if len(column_value_list) > 2:
        corporate_officer.name = process_item(column_value_list[2]).replace("/","")
    
    if len(column_value_list) > 3:
        corporate_officer.birthday = process_item(column_value_list[3])
    
    if len(column_value_list) > 4:
        corporate_officer.biography = get_biography_value(column_value_list)
    
    if len(column_value_list) > 5:
        corporate_officer.term = process_item(column_value_list[5])
    
    if len(column_value_list) > 6:
        corporate_officer.stock = process_item(column_value_list[6])
    
    return corporate_officer

def get_biography_value(column_value_list):
    biography = process_item(column_value_list[4])
    biography_list = biography.split("/")

    number = 1
    value = ""
    for target in biography_list:
        if target.strip() != "":
            if re.search("[0-9]",target):
                number = 1

                if value.strip() != "":
                    value += "\n"

            if number == 1:
                value += target + " "
                number += 1
                continue

            if number == 2:
                value += target
                continue
    return value

def process_item(item):
    return item.translate(trans_table).strip("/")

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
