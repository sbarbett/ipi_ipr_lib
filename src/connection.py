# Copyright 2014 NeuStar, Inc.All rights reserved.
# NeuStar, the Neustar logo and related names and logos are registered
# trademarks, service marks or tradenames of NeuStar, Inc. All other
# product names, company names, marks, logos and symbols may be trademarks
# of their respective owners.
__author__ = 'Shane Barbetta'

import urllib, urllib2, md5, time, json, ConfigParser

class ApiConnection:
    def __init__(self):
        config = ConfigParser.ConfigParser()
        config.read('config.ini')
        self.api_key = config.get('Credentials', 'APIKey')
        self.secret = config.get('Credentials', 'Secret')
        self.base_url = 'http://api.neustar.biz/ipi/'
        if config.get('Credentials', 'GPP') == 'True':
            self.ipi_endp = 'gpp/v1/ipinfo/'
        else:
            self.ipi_endp = 'std/v1/ipinfo/'
        self.ipr_endp = 'v1/ipscore/'
        self.sig = ''
        self._auth()

    def _auth(self):
        timestamp = str(int(time.time()))
        self.sig = md5.new(self.api_key + self.secret + timestamp).hexdigest()
        
    def _refresh(self, ip, reputation=False):
        self._auth()
        return self._do_call(ip, reputation, False)
        
    def get(self, ip, reputation=False):
        return self._do_call(ip, reputation)
        
    def _do_call(self, ip, reputation=False, retry=True):
        query = { "sig": self.sig, "apikey": self.api_key, "format": "json" }
        query = urllib.urlencode(query)
        if reputation == True:
            uri = self.base_url + self.ipr_endp + ip + '?' + query
        else:
            uri = self.base_url + self.ipi_endp + ip + '?' + query
        # For debugging
        # print uri
        req = urllib2.Request(uri)
        time.sleep(2)
        try:
            resp = urllib2.urlopen(req)
        except urllib2.URLError, e:
            if e.code == 403 and retry != False:
                return self._refresh(ip, reputation)
            else:
                return 'Error: HTTP status code %s.' % str(e.code)
        else:
            data = json.load(resp)
            return data