'''
PGC ArcGIS Server Feature Service Query Example
pgc-ags-query-example.py

See readme.md for documentation
'''

import os, sys
import getpass
import httplib,urllib
import json, io

def main(argv=None):

    # Parameters for ArcGIS Server (or any server, for that matter)
    serverName = "discovery.pgc.umn.edu"
    serverPort = None
    useSSL = False

    # Step 1:   Get account information from the prompt
    #           Hard-code these values at your own risk (!)
    print "Getting account information..."
    username = raw_input("Enter username: ")
    password = getpass.getpass("Enter password: ")

    # Step 2:   Establish http(s) connection to ArcGIS server
    conn = createHttpConnection(serverName,serverPort,useSSL)

    # Step 3:   Request a token from the ArcGIS server
    #           Required for ArcGIS secure services
    token = getToken(conn,username,password)

    # Step 4:   Example query
    result = featureServiceQueryExample(conn,token)

    # Step 5:   Close http(s) connection
    conn.close()

    # --- Working with the results --- #
    # RESULTS EXAMPLE: Print number of features (records) returned
    try:
        features = result["features"]
        print "Results Example (number of features returned):"
        print "-- %s features returned"%(len(features))
    except Exception as e:
        print "--ERROR: %s"%(e)

    # RESULTS EXAMPLE: Print the pairname field for each feature
    # objectid, pairname fields must be included in the query parameter "outFields"
    try:
        features = result["features"]
        num_disp = 10
        print "Results Example (first %s and last %s features with pairname field value):"%(num_disp,num_disp)
        count=0
        for feat in features:
            count+=1
            if count <= num_disp or count > len(features)-num_disp:
                print "-- objectid %s: %s"%(str(feat["attributes"]["objectid"]).ljust(len(str(len(features)))),feat["attributes"]["pairname"])
            else:
                if count == num_disp+1:
                    print "-- .."
    except Exception as e:
        print "-- ERROR: %s"%(e)
    
    # RESULTS EXAMPLE: Serialize result json object to .json file
    try:
        print "Results Example (write to file):"
        print "-- Writing to file..."
        #outfile = r"C:/temp/query-example-result.json"
        outfile = os.path.join(os.path.dirname(os.path.realpath(__file__)),"query-example-result.json")
        pretty = True # Set to True for pretty printing
        with io.open(outfile,"wb") as stream:
            if pretty == True:
                json.dump(result,stream,indent=4,separators=(',',': '))
            else:
                json.dump(result,stream)
        print "-- JSON file saved. (%s)"%(outfile)
    except Exception as e:
        print "-- ERROR: %s"%(e)

    
    print "Script complete."
    
'''
public method featureServiceQueryExample(token)
'''
def featureServiceQueryExample(httpConn,token=None):
    try:
        print "Performing Feature Service query..."
        
        if token is None:
            print "ERROR: This method requires a valid ArcGIS Server token. Run getToken prior to this call."
            sys.exit("Terminating script.")

        # Must include the beginning forward slash
        queryUrl = "/arcgis/rest/services/vendor/index_dg_comm_opt_stereo_strip_all_all_pairname/FeatureServer/0/query"

        params = urllib.urlencode({
            "where"         : "objectid<150",
            "outFields"     : "objectid,catalogid,acqdate,pairname",
            "orderByFields" : "objectid ASC",
            "returnGeometry": False,
            "token"         : token,    # Do not change
            "f"             : "json"    # Do not change
        })

        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
            
        httpConn.request("POST",queryUrl,params,headers)

        response = httpConn.getresponse()
        
        print "-- Server responded with status %s (%s)."%(response.status,response.reason)

        if (response.status != 200):
            print "-- ERROR: Could not perform query on specified URL. Please check and try again."
            sys.exit("Terminating script.")
            
        else:
            data = response.read()

            # Check that data returned is not an error object
            if not assertJsonSuccess(data):
                print "-- ERROR: JSON object returned an error"
                sys.exit("Terminating script.")

            result = json.loads(data)
            print "-- Valid result."
            return result
    except:
        return
    
'''
public method getToken(conn,username,password)
'''
def getToken(conn,username,password):
    try:
        print "Getting ArcGIS Server token..."
        
        tokenUrl = "/arcgis/tokens/generateToken"

        params = urllib.urlencode({
            "username"  : username,
            "password"  : password,
            "client"    : "requestip",
            "f"         : "json"
        })

        headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
            
        conn.request("POST",tokenUrl,params,headers)

        response = conn.getresponse()
        
        print "-- Server responded with status %s (%s)."%(response.status,response.reason)

        if (response.status != 200):
            print "-- ERROR: Could not fetch token from specified URL. Please check and try again."
            sys.exit("Terminating script.")
            
        else:
            data = response.read()

            # Check that data returned is not an error object
            if not assertJsonSuccess(data):
                sys.exit("Terminating script.")

            # Deserialize the json object to Python data structure
            result = json.loads(data)
            print "-- Valid token."
            return result["token"]
    except:
        return

'''
public method createHttpConnection(serverName,serverPort=None,useSSL=False)
'''
def createHttpConnection(serverName,serverPort=None,useSSL=False):
    try:
        httpConn = None

        print "Establishing connecting to server..."

        # Configurable for varying port numbers and both http and https connections
        if serverPort is not None:
            if useSSL == True:
                httpConn = httplib.HTTPSConnection(serverName,serverPort)
            else:
                httpConn = httplib.HTTPConnection(serverName,serverPort)
        else:
            if useSSL == True:
                httpConn = httplib.HTTPSConnection(serverName)
            else:
                httpConn = httplib.HTTPConnection(serverName)

        return httpConn
    except:
        return

'''
public method assertJsonSuccess(data)
'''
def assertJsonSuccess(data):
    try:
        obj = json.loads(data)

        if "status" in obj and obj["status"] == "error":
            print "ERROR: json object returned an error."
            return False
        elif "error" in obj:
            print "ERROR: %s. %s."%(obj["error"]["message"], obj["error"]["details"])
            return False
        else:
            return True
    except:
        return False
    
'''
script start
'''
if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))


