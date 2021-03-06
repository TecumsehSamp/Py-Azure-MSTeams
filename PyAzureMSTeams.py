import ConnectionHandler
import requests
import json


def Comparison(access):
	azuretables = ConnectionHandler.createtable()
	
	resourcegroup = ConnectionHandler.resources()
	resourcegroupname = ConnectionHandler.resourcegroupobject()
	r1 = requests.get(resourcegroup, headers= {"Authorization" : 'bearer {}'.format(access)})
	r2 = requests.get(resourcegroupname, headers= {"Authorization" : 'bearer {}'.format(access)})
	jsonresponse1 = json.loads(r1.text)
	jsonresponse2 = json.loads(r2.text)
	if r1.status_code == 401:
		return(0)

	rgdict = []
	rgdict2 = []
	try:
		for value in jsonresponse1['value']:

			rgdict.append(value)
	except Exception as e:
		if str(e) == "'value'":
			print("No Resource Group Available")
			
	for id in rgdict:
		Pkey = id['name']
		RKey = jsonresponse2['name']
		Types = id['type']
		Location = id['location']
		identif = id['id']
		check = ConnectionHandler.CheckIDs(Pkey,RKey)
		rgdict2.append(identif)
		
		if check == None:
			ConnectionHandler.storageaccounthandler(Pkey,RKey,Types,Location, identif)
			ConnectionHandler.TeamsConnection("New Resource created: \n\n" + "**Name:** " + Pkey + "\n\n" + "**Resource Group:** " + RKey + "\n\n" + "**Resource Type:** " + Types + "\n\n" + "**Resource ID:** " + identif + "\n\n" + "**Location:** " + Location)

		
		
	Backstate = ConnectionHandler.CheckforDeleted()
	diffcheck = [item for item in Backstate if item not in rgdict2]
	if len(diffcheck) != 0:
		deletion = ConnectionHandler.DeleteEntity(diffcheck)
		print(deletion)
	else:
		print("No orphans")
	# Slow the rate of requests down.
	time.sleep(10)
	
def AZConnect():
	global tokens
	tokens = ConnectionHandler.AzureConnection()
	return(tokens)

def ensureConnection():
	global conn
	s = 1
	while s:
		conn = ConnectionHandler.AzureConnection()
		TokenCheck = ConnectionHandler.TokenCheck(conn)
		print(TokenCheck)
		Comparison(conn)
		#while TokenCheck == "Valid":
		#	Comparison(conn)
		#	TokenCheck = ConnectionHandler.TokenCheck(conn)
		#	print(TokenCheck)
		#	if TokenCheck == "Invalid":
		#		conn = ConnectionHandler.AzureConnection()
		#	Comparison(conn)
		
	return()


if __name__ == "__main__":
	
	ensureConnection()
