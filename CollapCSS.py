import sys
from collections import defaultdict

'''
This function extracts the names of the classes, ids, tags, etc., places them in a list, and then returns the list.
'''
def list_names(names):
    l = []
    while ',' in names:
        first_comma = names.find(',')
        l.append(names[:first_comma])
        names = names[first_comma+1:].strip()
    l.append(names)
    return l

def collapse(path):
    css = open(path, "r")
    
    full = ''
    decl_dict = {}

    for line in css:
        full += line
        full = full.strip('\n')
        while '{' and '}' in full:
            ocb = full.find('{')
            atr = list_names(full[:ocb].strip())
            full = full[ocb+1:]
            j = True
            while ('}' in full) and j:
                decl = full[:full.find(';')+1].strip()
                full = full[full.find(';')+1:]
                if decl in decl_dict:
                    for l in atr:
                        if l not in decl_dict[decl]:
                            print(decl + ":" + str(decl_dict))
                            decl_dict['random1;'].append(l)
                            print(decl + ":" + str(decl_dict))
                else:
                    # originally did decl_dict[decl] = atr, but this caused the dictionary keys
                    # to just point to the address of atr instead of creating their own copy and
                    # this means that every single time it would run this else-statement with the
                    # same atr every key that was created by doing so would point to the same atr.
                    # And therefore, when appending to that key value later, we would end up
                    # changing all the keys that POINT to this value. Causing unintended behaviour.
                    # The reason why we add atr to an empty dictionary is to force python to create
                    # a copy.
                    decl_dict[decl] = [] + atr

                if full.strip()[0] == '}':
                    full = full[full.find('}')+1:]
                    j = False

    css.close()
    return decl_dict

'''
Sorts the list values in the provided dictionary, then converts these lists into a string.
'''
def sort_and_stringify_dlists(d):
    for key in d:
        v = ''
        d[key].sort()
        for i in d[key]:
            v += i
            if i != d[key][-1]:
                v += ", "
        d[key] = v

def reverse_keys_and_values(d):
    d_inverted = defaultdict(list)
    {d_inverted[v].append(k + '\n') for k, v in d.items()}
    return dict(d_inverted)

def write_collapse(d, path):
    css = open(path, 'w')
    for k in d:
        css.write(k+" {\n")
        css.writelines(d[k])
        css.write("}\n\n")
    css.close()

if (len(sys.argv) != 2) and (len(sys.argv) != 3):
    print("Insufficient number of arguments! Terminating program...")
    quit()

d = collapse(sys.argv[1])
print(d)
sort_and_stringify_dlists(d)
print(d)
d = reverse_keys_and_values(d)
print(d)

if (len(sys.argv) == 2):
    write_collapse(d, sys.argv[1])
else:
    write_collapse(d, sys.argv[2])