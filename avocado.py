"""Avocado use gacamole API to manage users and connections 
 
Usage: avocado.py --user <name> <password>
       avocado.py --connection <host> <microservice>
       avocado.py --associate <name> <connection_name>
       avocado.py --delete-connection <name>
       avocado.py --get-all-users
       avocado.py --associate-for-all <username>
       avocado.py --get-all-connections
       avocado.py --delete-all-connections
       avocado.py --set-all-connections <username>
       avocado.py --associate-for-all <microservice>
       avocado.py --get-all-connections
       avocado.py --delete-all-connections
       avocado.py --set-all-connections <username>
       avocado.py --master-association

Options:
  --user                    Create user, parameters username and password, At first connection, new password will be asked
  --connection              Create a new connection with host addr and microservice name
  --associate               Associate User with connection name 
  --delete-connection       Delete connection with name in parameters
  --delete-all-connections  Delete all connections
  --get-all-users           Get All users names
  --get-all-connections     Get All Connections names
  --set-all-connections     Get All connections and assocaite them to user name given in parameters
  --associate-for-all       Associate microservice name given for all users
  --master-association      For All microservices in guacamole, associate them to all users
  --version                 Show current versionn

  """
from client import Guacamole
from templates import *
from docopt_dispatch import dispatch
from config import *
import json

@dispatch.on('--user')
def user(name,password,**kwargs ):
    client = Guacamole(addr,login,passwd)
    data = {
    'username': name,
     'password': password,
     'attributes':  {
        'disabled': '',
        'expired': 'true',
        'access-window-start': '',
        'access-window-end': '',
        'valid-from': '',
        'valid-until': '',
        'timezone': ''}}
    client.add_user(data)


@dispatch.on('--connection')
def connection(host,microservice,**kwargs ):
    client = Guacamole(addr,login,passwd)
    sshkeyfile = open(path_ssh,"r")
    sshkey= sshkeyfile.read()
    ssh = {
    'activeConnections': 0,
    'attributes': {
        'max-connections': '',
        'max-connections-per-user': ''},
    'identifier': '',
    'name': microservice,
    'parameters': {
        'hostname': host,
        'pasphrase': '',
        'port': '22',
        'username': 'ubuntu',
        'private-key': sshkey,
        'passphrase': ''
    },
    'parentIdentifier': 'ROOT',
    'protocol': 'ssh'}

    client.add_connection(ssh)

@dispatch.on('--associate')
def associate(name,connection_name,**kwargs ):
    client = Guacamole(addr,login,passwd)
    number=client.get_connection_by_name(connection_name)
    identifi=number['identifier']
    asso=[{"op":"add","path":"/connectionPermissions/"+identifi,"value":"READ"}]
    client.add_connection_permission(name,asso)

@dispatch.on('--delete-connection')
def delete(name,**kwargs ):
    client = Guacamole(addr,login,passwd)
    number=client.get_connection_by_name(name)
    identifi=number['identifier']
    client.delete_connection(identifi)

@dispatch.on('--delete-all-connections')
def delete_all(name,**kwargs ):
    client = Guacamole(addr,login,passwd)
    connections=client.get_connections()
    list_connections = list(find('name', connections))
    new_list = [s.encode('utf-8') for s in list_connections]
    for x in new_list:
        if x == "ROOT":
            print 0
        else:
            delete(x)


@dispatch.on('--get-all-users')
def users(**kwargs ):
    client = Guacamole(addr,login,passwd)
    users=client.get_users()
    list_user = list(find('username', users))
    new_list = [s.encode('utf-8') for s in list_user]
    print(new_list)
    return new_list

@dispatch.on('--get-all-connections')
def connections(**kwargs ):
    client = Guacamole(addr,login,passwd)
    connections=client.get_connections()
    list_connections = list(find('name', connections))
    new_list = [s.encode('utf-8') for s in list_connections]
    print(new_list)
    return new_list

@dispatch.on('--set-all-connections')
def set_connections(username,**kwargs ):
    client = Guacamole(addr,login,passwd)
    connections=client.get_connections()
    list_connections = list(find('name', connections))
    print(list_connections)
    new_list = [s.encode('utf-8') for s in list_connections]
    print(new_list)
    for x in new_list:
        if x == "ROOT":
            print 0
        else:
            associate(username,x)

@dispatch.on('--associate-for-all')
def asso_all(microservice,**kwargs ):
    client = Guacamole(addr,login,passwd)
    users=client.get_users()
    list_user = list(find('username', users))
    new_list = [s.encode('utf-8') for s in list_user]
    for x in new_list:
        associate(x,microservice)

@dispatch.on('--master-association')
def master_asso(**kwargs ):
    client = Guacamole(addr,login,passwd)
    conns=connections()
    usrs=users()
    for x in conns:
        if x != "ROOT":
            for u in usrs:
                associate(u,x)

def find(key, dictionary):
    for k, v in dictionary.items():
        if k == key:
            yield v
        elif isinstance(v, dict):
            for result in find(key, v):
                yield result
        elif isinstance(v, list):
            for d in v:
                for result in find(key, d):
                    yield result



if __name__ == '__main__':
    dispatch(__doc__,version='Avocado 0.2.0')
