# Avocado
Avocado is a command line python program, that permit you to manage apache guacamole.

## Why

In some cases you may want to dynamically add machines. In my case, with terraform and ansible, I create machines on the fly, for different platforms, Quality, developers, integration and production. For each of these platforms, I want a single entry point for my backend users. So I create an API based on fabulous work of https://github.com/pschmitt/guacapy

Each time a microservice is builded on jenkins I use a build ran avocado to integrate each microservices on guacamole.

## Installation

Install requirements 
    `pip install -r requirements.txt`
Python version 2.7, mirgration to 3.5 can be done, but json parsing is differnt so somes string manipulation have to be done

## Usage

       avocado.py --user <name> <password>
       avocado.py --connection <host> <microservice>
       avocado.py --associate <name> <connection_name>
       avocado.py --delete-connection <name>
       avocado.py --get-all-users
       avocado.py --associate-for-all <username>
       avocado.py --get-all-connections
       avocado.py --delete-all-connections
       avocado.py --set-all-connections <username>
       avocado.py --master-association

## Options

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
        
## Version

# TODO

    - Only One user is used, user Ubuntu
    - Implement S3 read write repo to upload and download rsa keys

## v0.2.0

    - Used is dev and qa plateform
    - ADD: --master-association -> For All microservices in guacamole, associate them to all users
    - FIX: --associate-for-all  -> Associate microservice name given for all users
    
## v0.1.5

    - password is expired by default in user creation

## v0.1.4

    - Add config file
