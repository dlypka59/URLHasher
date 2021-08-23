"""
File: testurlhasherapi.py
Author: David Lypka
Description: Script to test urlhasher.py
Example usage (run these 2 commands in a command shell (can run both in the same shell instance)):
  python3 urlhasher.py
  python3 testurlhasherapi_local.py
  
The 1st line starts the urlhasher rest api server running.
The 2nd line sends a POST request to hash as sample URL and store the sample in a datastore, keyed by the new hash which is returned in the result json.
NOTE: Using the hardcoded sample input url, the resulting hash will be 9m35Laf.

Then open a browser and navigate to
  http://127.0.0.1/urlhash/9m35Laf
This will send a GET request to retrieve the sample URL given the hash "9m35Laf.
You can then keep the server process running (the process created from "python3 urlhasher.py")
and now run the 2nd command again (python3 testurlhasherapi_local.py)
which will demonstrate that *different* hash will be created upon subsequent urlhash requests for the same input url.
This is the same behavior that tinyurl.com has.

** See file README.md for more details.
"""
import requests
import sys
import datetime
import json

if len(sys.argv) > 1:
    port = sys.argv[1]
else:
    port = 5000 # input('Enter port (E.g. 5000):')
    
host = '127.0.0.1'

def get_strdatetime():
    
    """Compute current datetime in a convenient format."""
    
    strdatetime = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()).replace(':','-').replace(' ','_')
    return strdatetime

  
is_urlhash_post_enabled = True
if is_urlhash_post_enabled:
    apiurl = 'http://%s:%s/urlhash' % (host, port)

    inputurl = 'https://www.google.com/search?q=new+york+city+weather&oq=&aqs=chrome.2.69i59i450l8.392358635j0j7&sourceid=chrome&ie=UTF-8'
    
    postjson={'url': inputurl}

    r = requests.post(apiurl, json=postjson)
    
    print(r.status_code)
    print(f"Response from the POST: {r.json()}")
    print(f"URL to retrieve Original URL: {r.headers['Location']}")
    print('--End of call to POST apiurlhasher()--\n\n')
    #input('Press any key to Terminate:')
    exit(0)
   
is_urlhash_post_enabled = False
if is_urlhash_post_enabled:
    # NOTE: An easier alternative to running the following script is to
    #       run this url in a browser: 
    #       http://127.0.0.1/urlhash/9m35Laf
    urlhash = '9m35Laf'
    apiurl = 'http://%s:%s/urlhash/%s' % (host, port, urlhash)
    r = requests.get(apiurl)
    print(r.status_code)
    print(json.dumps(r.json())) # dumps() is needed to format using double quotes (") required by json standard
    print('--End of call to GET apiurlhasher()--\n\n')



   
    
