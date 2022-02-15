import re,os
'''
    To use just run it however you like in the same directory as your target file, using the full name and extension of the target file as your input. Can be ran by double-clicking coincidentally lol. Output will be in a %filename%_results.txt
    Sample input/output below:
    
    D:\Labs\testing>strIP.py
    Filename.ext pls: 379-Lab14-Deloya.yaml

    Success!
    Press any key to continue . . .
'''

filename = input("Filename.ext pls: ")
with open(filename, 'r') as yaml:
    text = yaml.read()

#toggle one or the other regex block:
#---this one gives you results with the subnet mask---
regexd = re.findall(r'((\s*id\:.*\s*label\:.*\s*node_definition: (asav|iosv))|(interface.*(\/.*|Loopback.*)(\s*description.*)?(\s*bandwidth.*)?(\s*duplex full)?(\s*(no )?nameif.*)?(\s*(no )?security\-level.*)?\s*ip address \d{1,3}(\.\d{1,3}){3} \d{1,3}(\.\d{1,3}){3}))',text)

#---without subnet mask---
'''
regexd = re.findall(r'((\s*id\:.*\s*label\:.*\s*node_definition: (asav|iosv))|(interface.*(\/.*|Loopback.*)(\s*description.*)?(\s*bandwidth.*)?(\s*duplex full)?(\s*(no )?nameif.*)?(\s*(no )?security\-level.*)?\s*ip address \d{1,3}(\.\d{1,3}){3}))',text)
'''

#basically regex greps in the step before and write those here to a temporary file for cleaning up
with open('IP.tmp', 'w') as txt:
    for x in regexd:
        txt.write(x[0]+'\n')

#lines with bad_words will get deleted from the final _results.txt
#eg. add 'interface' to the list to get rid of the "interface GigabitEthernetX/X" lines
#remove ' node_definition' from bad_words if you want the type of device "ios or asav" printed right after the host name like:
#hostname: FW1
#type: asav

#if you want, try it with an empty list "[]" to see what the regex spat back to begin with
#bad_words = []
bad_words = ['id: ', 'description ', 'bandwidth', 'nameif', 'security-level', 'duplex full', ' node_definition']

with open('IP.tmp') as editfile:
    list_of_lines = editfile.readlines()
    new_list = list()
    for line in list_of_lines:
        if not any(bad_word in line for bad_word in bad_words):
            new_list.append(re.sub(r'\s*label:', '\nhostname:',line).replace("interface ", "      interface ").replace("    node_definition","type"))

#writes to the _results.txt using the same filename provided
with open(filename[:filename.rfind('.')]+'_results.txt', 'w') as editfile:
    editfile.writelines(new_list)

#deletes the temp file we used
try:
    os.remove('IP.tmp')
except OSError:
    pass

os.system("echo.&&echo Success!&&pause")