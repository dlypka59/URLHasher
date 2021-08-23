# How to setup and run the urlhash service

Author / Developer:</br>
David Lypka</br>
email: dlypka@gmail.com

Clone or Download the code from https://github.com/dlypka59/URLHasher</br>
to a new local folder 'URLHasher'

```
git clone https://github.com/dlypka59/URLHasher.git
```

Open a command prompt in the URLHasher folder

Install required python packages
```
pip install -r requirements.txt
```

Run
```
python urlhasher.py
```
(NOTE: it may be necessary to type python3 rather than python)

Sample console output:
```
dlypka@dlypka-ubuntu:~/URLHasher$ python3 urlhasher.py
* Serving Flask app "urlhasher" (lazy loading)
* Environment: production
* WARNING: This is a development server. Do not use it in a production deployment.
* Use a production WSGI server instead.
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 114-112-787`
```

You may use the provided script in file testurlhasher.py</br>
to post request to the urlhasher REST API at http://127.0.0.1:5000</br>
Here is the core code fragment from testurlhasher.py:
```
    apiurl = 'http://%s:%s/urlhash' % (host, port)
    
    inputurl = 'https://www.google.com/search?q=new+york+city+weather&oq=&aqs=chrome.2.69i59i450l8.392358635j0j7&sourceid=chrome&ie=UTF-8'
    
    postjson={'url': inputurl}    

    r = requests.post(apiurl, json=postjson)
    
    print(r.status_code)
    print(f"Response from the POST: {r.json()}")
    print(f"URL to retrieve Original URL: {r.headers['Location']}")
    print('--End of call to POST apiurlhasher()--\n\n')
```

To run testurlhasher.py:</br>
Open a 2nd Command prompt in the the same folder as is the 1st command prompt and type:
```
python3 testurlhash.py
```
Sample output:
```
dlypka@dlypka-ubuntu:~/URLHasher$ python3 testurlhasherapi_local.py
200
Response from the POST: {'url': 'https://www.google.com/search?q=new+york+city+weather&oq=&aqs=chrome.2.69i59i450l8.392358635j0j7&sourceid=chrome&ie=UTF-8', 'urlhash': '9m35Laf', 'Location': '/urlhash/9m35Laf'}
URL to retrieve Original URL: http://127.0.0.1:5000/urlhash/9m35Laf
--End of call to POST apiurlhasher()--
```

Now go to your browser and enter this url:
```
http://127.0.0.1:5000/urlhash/9m35Laf
```

Sample Output:
```
{"urlhash": "9m35Laf", "urlshortened": "http://127.0.0.1:5000/urlhash/9m35Laf", "url": "https://www.google.com/search?q=new+york+city+weather&oq=&aqs=chrome.2.69i59i450l8.392358635j0j7&sourceid=chrome&ie=UTF-8"}
```



