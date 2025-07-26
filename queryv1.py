from xml.etree import ElementTree as ET
import html2text
import requests
import re
__author__ = 'mirvin'

import types
from constants import *


def QueryForTests(instanceEndPoint):
    query ='?sel=Name,Number,Status.Name,Description,ID&where=(Reference="Car";-Status)'
    url = instanceEndPoint + '/' + 'Test' + query
    response = requests.get(url,auth=('admin','admin'))
    tree = ET.ElementTree(ET.fromstring(response.content))
    root = tree.getroot()
	#print "Checking for a test"
    #TODO if I find the pattern total="0", then exit with
    #Currently I am saying if it is probably a response with a test
    if len(response.text) > 150 and response.status_code == 200:
        Name =   root[0][0].text
        Number = root[0][1].text
        Status = root[0][2].text
        Desc =   root[0][3].text
        temp1 = root[0].attrib
        temp2 = temp1['id']
        temp=    re.search(r'Test:([0-9]*)',temp2)
        Oid = temp.group(1)
        print "Name:" + Name + "\nNumber:" + Number  # + "\nID:" 
		#print "Name:",Name,"\nNumber:",Number,"\nStatus:",Status,"\nID:",Oid
        return {'Name': Name,'Number':Number,'Status':Status,'Desc':Desc,'ID': Oid}
    else:
        print "There are no Tests in designated folder"
        return {'Name': 'NOTEST','Number': '-1','Status':'NOTEST','Desc':'NOTEST','ID':'NOTEST'}

# This cleans the html out of the code that will be loaded dynamically
def cleanString(dirtyString):
    clean = html2text.html2text(dirtyString)
    return clean

#This outputs code to the python script to be loaded dynamically
def outputScriptToFile(codeIn):
    oFile = open("script1.py","w")
    oFile.write(codeIn)
    oFile.close()
    print "Saved file to script1.py" 

def updateTest(instanceEndPoint,oid,passFail):
    url = instanceEndPoint + "/Test/" + oid
    payload ='<Asset><Relation name="Status" act="set"><Asset idref=' + "\"" + passFail + "\"" + '/></Relation></Asset>'
    response = requests.post(url,payload,auth=('admin','admin'))
    print "Updated Test"

def execTest(fileName):
	print "In the module NOW"
	with open(fileName) as filePtr:
		source = compile(filePtr.read(),fileName, "exec")
		config_module = types.ModuleType("<config>")
	exec source in config_module.__dict__

def updateConversation(instanceEndPoint,number,passFail):
	message  = "Ran test on " + number + " used Car 101B."
	url = instanceEndPoint + "/Expression"
	payload ='<Asset><Relation name="Author" act="set"><Asset idref="Member:20" /></Relation><Attribute name="AuthoredAt">2016-09-02T01:48:37.940</Attribute>  <Attribute name="Content" act="set">' + message + '</Attribute><Relation name="InReplyTo" act="set"><Asset idref="Expression:27605" /> </Relation></Asset>'
	response = requests.post(url,payload,auth=('admin','admin'))
	print response.text
	print "Updated Conversation"

