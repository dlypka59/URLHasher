"""
File: urlhasher.py
Author: David Lypka
Description: python web app to implement a REST API for creating shortened urls and querying for the original url.
For details, refer to README.md.
"""
import json
import datetime
import flask
from flask import Flask, request
from flask_cors import CORS

from bitcoin import *

# This is a small REST API not requiring flask templates and views.

# This REST API should be deployed to production as a Cloud Function,
# where the data would be persisted in a NoSQL datastore such as Google BigTable (in its latest incarnation)
# and I believe the Google Cloud is the best choice based on Google's long support of python in the cloud
# as per the example here: https://github.com/GoogleCloudPlatform/cloud-bigtable-examples/blob/master/python/thrift/flask_thrift.py
# For now I have implemented a NoSQL datastore simply as an inmemory dict named URLDATASTORE.
# There is no expiration feature in this implementation. That kind of feature should likely be part of a separate service
# in order to maintain the separation of concerns.

# There would be a configuration file such as .env
# containing the settings values shown in uppercase vars such as LOGPATHROOT
# Example:
#import logging.handlers
#:
#:
#from environs import Env
#env_filepath = './config.env'
#env = Env()
#env.read_env(env_filepath, recurse=False)
#LOGPATHROOT = env('LOGPATHROOT')
#:
#:
#handler = handlers.RotatingFileHandler

#handler = logging.handlers.RotatingFileHandler(
     #'%s\gizmo-service_%d_%s.log' % (LOGPATHROOT, threading.get_indent(), CURRENT_DATETIME),
     #maxBytes=eval(LOGMAXBYTES), mode='w', backupCount=500)
#handler.setLevel(logging.INFO)
#formatter = logging.Formatter(fmt='%(asctime)s %(process)d %s(levelname)-8s %(message)s')
#handler.setFormatter(formatter)
#app.logger.addHandler(handler)

#app.logger.info('Starting flask logger: messages go to stderr and app.log!')
#also see @app.before_request below...

URL_HASH_SIZE = 7   # 7 chars long following the sample shortend url size from bit.ly
                    # TODO: Read URL_HASH_SIZE from a .env file

app = Flask(__name__)
CORS(app)

app.debug = True  # default to using the Flask Debugger

OS_HOME_PATH = os.path.expanduser('~/')

URLDATASTORE = dict()

def get_strdatetime():
        
    """Compute current datetime in a convenient format."""
        
    strdatetime = '{0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now()).replace(':','-').replace(' ','_')
    return strdatetime

def notify(msg):
    
    """Convenient notification method."""
        
    print('%s %s' % (get_strdatetime(), msg))


#@app.before_request
#def before_request_func()
    #clientip = request.remote_addr
    #msg = 'ClientIP Address %s requested %s' % (clientip, request.url)
    #app.logger.info(msg)
    #return

@app.route('/urlhash', methods = ['POST']) 
@app.route('/urlhash/<string:urlhash>', methods = ['GET'])
def apiurlhasher(urlhash=None):
    
    """Hash a url to a short url of 7 chars and also get the original url given the short url."""
    
    response = flask.make_response()
    if request.method in ('POST'):
        url = request.json['url']
        my_private_key = sha256(url) # e.g. ‘57c617d9b4e1f7af6ec97ca2ff57e94a28279a7eedd4d12a99fa11170e94f5a4’

        #print(my_private_key)  # d90dc773daa4bfc6afeda8c4d89ccfa15312b38b6567d98b17912586ea084676
          
        my_public_key = privtopub(my_private_key)
        
        my_bitcoin_address = pubtoaddr(my_public_key) # e.g. 1wEbxZs58GJHp4be7ELehXycDkvLYakpR
        # derive the urlhash from a bitcoin address to leverage the base58 encoding. 
        # Base58 encoding uses a robust human-readable character set containing all alphanumeric characters except 0, O, I, and l. 
        
        #print(my_bitcoin_address[1:])  # wEbxZs58GJHp4be7ELehXycDkvLYakpR
        
        urlhash = my_bitcoin_address[1:URL_HASH_SIZE+1]  # dropping the initial leading constant prefix '1' of the bitcoin address standard
               
        if urlhash in URLDATASTORE:
            # Skip saving the url keyed by the hash because it already exists in the datastore.
            pass
        else:
            # Save the url to the datastore, keyed by the new hash, , for later query
            URLDATASTORE[urlhash] = url
           
        response.headers['Location'] = '/urlhash/%s' % urlhash
        response.set_data('{"url": "%s", "urlhash": "%s", "Location": "%s"}' % (url, urlhash, response.headers['Location']))
        
    elif request.method == 'GET':
        urldatastore = URLDATASTORE
        notify(request.url)
        notify(request.path)
        responsedict = dict(urlhash=urlhash, urlshortened = request.url, url=urldatastore[urlhash])
        responsejson = json.dumps(responsedict)
        response.set_data(responsejson)
    return response

#Exception handling can be implemented similar to the follow example code:
#@app.errorhandler(werkzeug.exceptions.BadRequest)
#def handle_bad_request(e):
    #return 'bad request!', 400

if __name__ == "__main__":
    # execute only if run as a script
    if 'WINGDB_ACTIVE' in os.environ:
        app.debug = False # Disable using Flask Debugger so that WINGIDE Debugger will be used
    app.run(host='127.0.0.1', port=5000)  # flask debug web server

# TODO: Code unit tests using pytest
    