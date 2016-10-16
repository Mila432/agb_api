import requests
import json
import argparse

s = requests.session()

'''
<-------- short info -------->
app = the app id: com.google.app
version = 1.0
map_name = native:app lib, unity:anon:libc_malloc
pkg_name = com.google.app
patch_type = native:lib, unity:unity
--->patch:
--->pattern = has to be a list ['0x13 0x37']
--->patch = the patched bytes 1337
<---------------------------->
'''

api_token='1234' #your api token
s.headers.update({'Content-Type': 'application/json', 'api_token': api_token})

base = 'http://mila432.xyz:5000'

def getCurrentPatches(app):
    url = base + '/%s/get' % (app)
    return s.get(url).content

def addNewPatch(app,version):
    url = base + '/%s/add' % (app)
    payload = {'app': app,
               'version': version,
               'map_name':'anon:libc_malloc', #change this
               'pkg_name':app,
               'patch_type':'unity',#change this
               'patch': [{
                   'name': 'patch1',
                   'pattern': ['0x40 0x40 0x40 0x40'],
                   'patch': ['01234567']
               }, {
                   'name': 'patch2',
                   'pattern': ['0x41 0x41 0x41 0x41'],
                   'patch': ['76543210']
               }]}
    for p in payload['patch']:
        if '0x40 0x40 0x40 0x40' in p['pattern']:
            print '[-] default patch... change it'
            exit(1)
    return s.post(url, data=json.dumps(payload)).content

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-app', action='store', dest='app', help='App id')
    parser.add_argument('-version', action='store', dest='version', help='App version')
    parser.add_argument('-add', dest='add', action='store_true',help='Adds new patch')
    parser.add_argument('-show', dest='show', action='store_true',help='Show current patches')
    args= parser.parse_args()
    if args.app and args.version:
        if args.add:
            print addNewPatch(args.app,args.version)
        if args.show:
            print getCurrentPatches(args.app)
    else:
        print '[-] please provide app version/id'

if __name__ == '__main__':
    main()