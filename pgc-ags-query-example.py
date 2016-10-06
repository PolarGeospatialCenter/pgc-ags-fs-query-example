'''
PGC ArcGIS Server Feature Service Query Example
pgc-ags-query-example.py

See readme.md for documentation
'''

import os, sys
import arcpy
import getpass
import httplib,urllib
import json, io
from datetime import datetime

def main(argv=None):

    # Parameters for ArcGIS Server (or any server, for that matter)
    serverName = "discovery.pgc.umn.edu"
    serverPort = None
    useSSL = False

    # Step 1:   Get account information from the prompt
    #           Hard-code these values at your own risk (!)
    print "Getting account information..."
    #username = raw_input("Enter username: ")
    #password = getpass.getpass("Enter password: ")
    username = 'herri147'
    password = 'HEYDUKroy44!'

    # Step 2:   Establish http(s) connection to ArcGIS server
    conn = createHttpConnection(serverName,serverPort,useSSL)

    # Step 3:   Request a token from the ArcGIS server
    #           Required for ArcGIS secure services
    token = getToken(conn,username,password)

    # Step 4a:  Example query
    result = None
    result = featureServiceQueryExample(conn,token)

    # Step 4b:  Example save locally
    #featureServiceQueryExampleSave(conn,serverName,serverPort,useSSL,token)

    # Step 5:   Close http(s) connection
    conn.close()

    # --- Working with the results 4a --- #
    # RESULTS EXAMPLE: Print number of features (records) returned
    if result is not None:
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
public method featureServiceQueryExample(httpConn,token)
'''
def featureServiceQueryExample(httpConn,token=None):
    try:
        print "Performing Feature Service query..."

        if token is None:
            print "ERROR: This method requires a valid ArcGIS Server token. Run getToken prior to this call."
            sys.exit("Terminating script.")

        # Must include the beginning forward slash
        queryUrl = "/arcgis/rest/services/vendor/pgc_dg_stereo_catalogids_with_pairname/FeatureServer/0/query"

        params = urllib.urlencode({
            "where"         : "catalogid='1010010000177C00'",
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

# '''
# public method featureServiceQueryExampleSave(token)
# '''
# def featureServiceQueryExampleSave(httpConn,serverName,serverPort,useSSL,token=None):
#     try:
#         print "Performing Feature Service query..."
#
#         if token is None:
#             print "ERROR: This method requires a valid ArcGIS Server token. Run getToken prior to this call."
#             sys.exit("Terminating script.")
#
#         # Create the geodatabase
#         print "-- Establishing geodatabase"
#         gdb_path = os.path.dirname(os.path.realpath(__file__))
#         gdb_name = "results.gdb"
#         fc_name = "results_" + datetime.now().strftime('%Y%m%d%H%M%S')
#         gdb = arcpy.env.workspace = os.path.join(gdb_path,gdb_name)
#         arcpy.env.overwriteOutput = True
#         if not arcpy.Exists(gdb):
#             print "-- Geodatabase created (%s)"%(gdb)
#             arcpy.CreateFileGDB_management(gdb_path,gdb_name)
#
#
#
#         # Get list of objectids
#         # Must include the beginning forward slash
#         print "-- Getting objectids"
#         queryUrl = "/arcgis/rest/services/vendor/pgc_dg_stereo_catalogids_with_pairname/FeatureServer/0/query"
#
#         params = urllib.urlencode({
#             "where"         : "objectid<3",
#             "returnIdsOnly" : True,
#             "token"         : token,    # Do not change
#             "f"             : "json"    # Do not change
#         })
#
#         headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
#
#         httpConn.request("POST",queryUrl,params,headers)
#
#         response = httpConn.getresponse()
#
#         print "-- Server responded with status %s (%s)."%(response.status,response.reason)
#
#         if (response.status != 200):
#             print "-- ERROR: Could not perform query on specified URL. Please check and try again."
#             sys.exit("Terminating script.")
#
#         else:
#             data = response.read()
#
#             # Check that data returned is not an error object
#             if not assertJsonSuccess(data):
#                 print "-- ERROR: JSON object returned an error"
#                 sys.exit("Terminating script.")
#
#             result = json.loads(data)
#             num_oids = len(result["objectIds"])
#             print "-- Valid result."
#             print "-- %s objectids."%(num_oids)
#             oids = result["objectIds"]
#
#
#         result = arcpy.FeatureSet()
#
#         ib=0
#         ie=n=1000
#
#         count=1
#         num_queries = num_oids/n
#         while ib < num_oids:
#             oid_set = oids[ib:ie]
#
#             # Build the query
#             print "-- Performing query (%s of %s)"%(count,num_queries+1)
#
#             objectIds = ",".join(str(x) for x in oid_set)
#             outFields = "objectid,catalogid,pairname,shape"
#
#             queryUrl = "/arcgis/rest/services/vendor/pgc_dg_stereo_catalogids_with_pairname/FeatureServer/0/query"
#
#             params = urllib.urlencode({
#                 "objectIds"     : objectIds,
#                 "outFields"     : outFields,
#                 "returnGeometry": True,
#                 "token"         : token,    # Do not change
#                 "f"             : "json"    # Do not change
#             })
#
#             headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
#
#             r = httpConn.request("POST",queryUrl,params,headers)
#
#             response = httpConn.getresponse()
#
#             if (response.status != 200):
#                 print "-- ERROR: Could not perform query on specified URL. Please check and try again."
#                 sys.exit("Terminating script.")
#
#             else:
#                 data = response.read()
#
#                 # Check that data returned is not an error object
#                 if not assertJsonSuccess(data):
#                     print "-- ERROR: JSON object returned an error"
#                     sys.exit("Terminating script.")
#
#                 r = json.loads(data)
#                 try:
#                     print "Results Example (write to file):"
#                     print "-- Writing to file..."
#                     #outfile = r"C:/temp/query-example-result.json"
#                     outfile = os.path.join(os.path.dirname(os.path.realpath(__file__)),"temp.json")
#                     pretty = True # Set to True for pretty printing
#                     with io.open(outfile,"wb") as stream:
#                         if pretty == True:
#                             json.dump(r,stream,indent=4,separators=(',',': '))
#                         else:
#                             json.dump(r,stream)
#                     print "-- JSON file saved. (%s)"%(outfile)
#                 except Exception as e:
#                     print "-- ERROR: %s"%(e)
#
#                 arcpy.JSONToFeatures_conversion(outfile,"temp_fc")
#                 result.load("temp_fc")
#                 arcpy.Delete_management("temp_fc")
#
#             ie+=n
#             ib+=n
#             count+=1
#
#         print "-- Copying to geodatabase"
#         #result.save(os.path.join(gdb,fc_name))
#         arcpy.CopyFeatures_management(result,fc_name)
#         print "-- Done"
#
#
#
#     except Exception as e:
#         print "-- ERROR: %s"%(e)
#         return

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
