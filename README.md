### PGC ArcGIS Server
# Feature Service Query Example
*pgc-ags-query-example.py*

[![Latest Release](https://img.shields.io/badge/version-1.0-blue.svg?style=flat-square)](https://github.com/PolarGeospatialCenter/pgc-ags-fs-query-example/releases/tag/v.1.0)
[![Latest Release](https://img.shields.io/badge/released-2015--07--17-brightgreen.svg?style=flat-square)](https://github.com/PolarGeospatialCenter/pgc-ags-fs-query-example/releases/tag/v.1.0)

### Description
Stand-alone script for performing an HTTP(S) call to ArcGIS Server REST API.  
Includes methods for establishing HTTP(S) connection and getting ArcGIS Server token.  

Default PGC ArcGIS Server connection and service:  
- Server: [discovery.pgc.umn.edu](http://discovery.pgc.umn.edu/arcgis/rest/services) (10.1)
- Feature Service: [DigitalGlobe Stereo Index (pairnames)](http://discovery.pgc.umn.edu/arcgis/rest/services/vendor/index_dg_comm_opt_stereo_strip_all_all_pairname/FeatureServer) (requires authentication)

Example method included for performing a query to a Feature Service:
```
featureServiceQueryExample()
```

Example results from query in this repo as [query-example-result.json](query-example-result.json) for reference, based on this query:
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

### Account Registration
Requires an **approved account** with the Polar Geospatial Center for ArcGIS Services and requires proper **role assignment** for secure services. Accounts can be requested at the URL below, but require approval from the Polar Geospatial Center (please include your U.S. federal research award number). If you already have an account and need access to secure services, please email [Brad Herried](mailto:herri147@umn.edu).

Account Registration: https://users.pgc.umn.edu/request

### Requirements and Usage 
- Requires Python 2.6+ 
- Incompatible with Python 3.0 (httplib, urllib) 
- **Command line** `python path/to/script/pgc-ags-query-example.py`
    - During script execution, you will be prompted for your username and password

### Methods
##### :large_blue_diamond: featureServiceQueryExample(*token*)
Queries an ArcGIS Feature Service layer via an HTTP(S) call.
> **Request Parameter Docs**  
> http://discovery.pgc.umn.edu/arcgis/sdk/rest/index.html?fsquery.html   
> **Browser-based Test**  
> http://discovery.pgc.umn.edu/arcgis/rest/services/vendor/index_dg_comm_opt_stereo_strip_all_all_pairname/FeatureServer/0/query  
> 
> **Parameters**  
> `conn` http(s) connection object  
> `token` valid ArcGIS Server token string   
> **Returns**  
> Deserialized JSON object to Python data structure  

##### :large_blue_diamond: getToken(*conn*,*username*,*password*)
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

##### :large_blue_diamond: createHttpConnection(*serverName*,*serverPort*,*useSSL*)
Initiates an HTTP or HTTPS connection to the specified host server.
> **Parameters**  
> `serverName` ArcGIS Server domain (e.g. `overlord.pgc.umn.edu`)  
> `serverPort` ArcGIS Server port for access. Defaults to `None` but some ArcGIS Servers use `6080``6443``80`  
> `useSSL` connect using a secure (HTTPS) connection `True|False`  
> **Returns**  
> `httpConn` Python HTTP(S) connection object  

##### :large_blue_diamond: assertJsonSuccess(*data*)
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
