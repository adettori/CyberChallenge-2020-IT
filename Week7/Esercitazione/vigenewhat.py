from string import ascii_lowercase

alph = "acegikmoqsuwyacegikmoqsuwy"
ciph = "eeqm{ocs_oaeiiamqqi_qk_moam!}"

def find_key(cur_str, ind, ciphtext, matr_diag):

    if(len(cur_str) == len(ciphtext)):
        print(cur_str)
        return

    if(ciph[ind] == "{" or ciph[ind] == "}" or ciph[ind] == "_" or ciph[ind] == "!"):
        find_key(cur_str+ciph[ind], ind+1, ciphtext, matr_diag)
        return

    for i in range(len(matr_diag)):
        if(matr_diag[i] == ciphtext[ind]):
            find_key(cur_str+ascii_lowercase[i], ind+1, ciphtext, matr_diag)

find_key("", 0, ciph, alph)
