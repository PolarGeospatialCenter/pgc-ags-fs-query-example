### PGC ArcGIS Server
# Feature Service Query Example
*pgc-ags-query-example.py*

![Latest Release](https://img.shields.io/badge/version-1.0-blue.svg)
![Release Date](https://img.shields.io/badge/released-2015--07--17-brightgreen.svg)

### Description
Stand-alone script for performing an http(s) call to ArcGIS Server REST API.  
Includes methods for establishing http(s) connection and getting ArcGIS token.  

Example method for performing a query to a Feature Service:
```
featureServiceQueryExample()
```

Example results from query included as `query-example-result.json` for reference:
```python
params = urllib.urlencode({
    "where"         : "objectid<150",
    "outFields"     : "objectid,catalogid,acqdate,pairname",
    "orderByFields" : "objectid ASC",
    "returnGeometry": False,
    "token"         : token,    # Do not change
    "f"             : "json"    # Do not change
})
```

### Requirements
Requires an **approved account** with the Polar Geospatial Center for ArcGIS Services and requires proper **role assignment** for secure services. Email [Brad Herried](mailto:herri147@umn.edu) for instructions for how to create an account and request the proper role for secure services.

### Usage 
- Requires Python 2.6+ 
- Incompatible with Python 3.0 (httplib, urllib) 
- **Command line** `python path/to/script/pgc-ags-query-example.py` 

### Methods


##### featureServiceQueryExample(*token*)
Queries an ArcGIS Feature Service via an http(s) call.
> **Request Parameter Docs**  
> https://overlord.pgc.umn.edu/arcgis/sdk/rest/index.html#//02ss0000002r000000  
> **Browser-based Test**  
> https://overlord.pgc.umn.edu/arcgis/rest/services/vendor/index_dg_comm_all_stereo_strip_all_all_pairname/FeatureServer/0/query
> 
> **Parameters**  
> `conn` http(s) connection object  
> `token` valid ArcGIS Server token string   
> **Returns**  
> Deserialized JSON object to Python data structure  


##### getToken(*conn*,*username*,*password*)
Requests an authorization token from the ArcGIS Server API by username and password.
> **Request Parameters**  
> `"client"` set to "requestip"  
> `"f"` set to "json"  
> 
> **Parameters**  
> `conn` http(s) connection object  
> `username` registered PGC ArcGIS Server username  
> `password` associated PGC ArcGIS Server password  
> **Returns**  
> `result["token"]` token string from the result JSON object  


##### createHttpConnection(*serverName*,*serverPort*,*useSSL*)
Initiates an HTTP or HTTPS connection to the specified host server.
> **Parameters**  
> `serverName` ArcGIS Server domain (e.g. `overlord.pgc.umn.edu`)  
> `serverPort` ArcGIS Server port for access. Defaults to `None` but some ArcGIS Servers use `6080``6443``80`  
> `useSSL` connect using a secure (https) connection `True|False`  
> **Returns**  
> `httpConn` Python HTTP(S) connection object  


##### assertJsonSuccess(*data*)
Basic check for errors in the return JSON response data.
> **Parameters**  
> `data` JSON response data from HTTP(S) request  
> **Returns**  
> `True|False` boolean value. `True` for success, `False` for error  

---

**Author**  
Brad Herried  
herri147@umn.edu  
Polar Geospatial Center  
University of Minnesota  

**GitHub Repository**  
*Polar Geospatial Center*   
https://github.com/PolarGeospatialCenter/pgc-ags-fs-query-example.git
