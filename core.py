import json


FILE_NAME = 'CIS_MS_Windows_10_Enterprise_Level_1_v1.10.1.audit'

def parse():
    with open(FILE_NAME) as file:
        lines = file.readlines()
        customs = []
        i = 0
        while i < len(lines):
            if lines[i].endswith('<custom_item>\n'):
                i += 1
                customs.append({})
                while not lines[i].endswith('</custom_item>\n'):
                    cur = lines[i].split(':')
                    cur[0] = cur[0].replace(' ', '')
                    cur[1] = cur[1].lstrip()
                    if cur[1].startswith('"') and not cur[1].endswith('"\n'):
                        while True:
                            i += 1
                            cur += lines[i]
                            if lines[i].endswith('"\n'): break

                    cur[1] = cur[1].replace('\n', '').replace('"', '')
                    customs[len(customs) - 1][cur[0]] = cur[1]
                    i += 1

            i += 1

    customs = list(filter(lambda d: 'reg_key' in d, customs))
    for index in range(0, len(customs)):
        customs[index]['index'] = index
    return customs
