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
        if '{' and '}' in full:
            ocb = full.find('{')
            atr = list_names(full[:ocb].strip())
            full = full[ocb+1:]

            while '}' in full:
                decl = full[:full.find(';')+1].strip()
                full = full[full.find(';')+1:]
                if decl in decl_dict:
                    for l in atr:
                        if l not in decl_dict[decl]:
                            decl_dict[decl].append(l)
                else:
                    decl_dict[decl] = atr

                if full.strip()[0] == '}':
                    full = full[full.find('}')+1:]

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