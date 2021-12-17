import json
import os
import subprocess
import re
import winreg

FILE_NAME = 'audit_files/CIS_MS_Windows_10_Enterprise_Level_1_v1.10.1.audit'
TEMP_FILE = 'temp.json'


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


data = parse()


def write_export(ids):
    if os.path.exists(TEMP_FILE):
        os.remove(TEMP_FILE)

    result = list(filter(lambda p: p['index'] in ids, data))
    if len(result) == 1: result = result[0]
    with open(TEMP_FILE, 'w') as output:
        json.dump(result, output)


def check_policies(ids):
    policies = list(filter(lambda p: p['index'] in ids, data))
    result = []
    for policy in policies:
        response = subprocess.run(['reg', 'query', policy['reg_key'], '/v', policy['reg_item']], capture_output=True)
        if response.returncode == 1:
            result.append(error(policy, response.stderr.decode('utf-8')[7:]))
            continue

        value = response.stdout.decode('utf-8').split('\n')[2].strip().split(4 * ' ').pop()
        result.append(check_value(policy, value))
    return result


def error(policy, error):
    return {'policy': policy, 'success': False, 'message': error}


def plain_response():
    return {'policy': None, 'success': False, 'message': ''}


def check_value(policy, value):
    type = policy['value_type']

    result = plain_response()
    result['policy'] = policy
    if policy['check_type'] == 'CHECK_REGEX':
        exp = re.compile(policy['value_data'])
        if exp.match(value) is not None:
            result['success'] = True
        else:
            result['message'] = f'Value {value} doesn\'t pass the policy.'
    elif type == 'POLICY_DWORD' or type == 'POLICY_TEXT' or type == 'POLICY_MULTI_TEXT':
        if type == 'POLICY_DWORD':
            value = str(int(value, 16))
        if policy['value_data'] == value:
            result['success'] = True
        else:
            result['message'] = f'Expected value: {policy["value_data"]}. Actual: {value}.'
    else:
        return error(policy, 'Unknown policy type')

    return result


def enforce(ids):
    policies = list(filter(lambda p: p['index'] in ids, data))

    # import winreg
    # key = winreg.OpenKeyEx(winreg.HKEY_LOCAL_MACHINE, "System\CurrentControlSet\Control\Lsa")
    # value, type = winreg.QueryValueEx(key, "SecureBoot")
    # result = winreg.SetValueEx(key, "SecureBoot", 0, winreg.REG_DWORD, 2)

    for policy in policies:
        response = subprocess.run(
            ['reg', 'add', "HKLM\System\CurrentControlSet\Control\Lsa",'/f', '/v', "SecureBoot", '/d', '"2"'],
            capture_output=True
        )
