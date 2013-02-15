from base64 import b64encode
from Crypto.PublicKey import RSA
from Crypto.Util.randpool import RandomPool
from fabric.api import *
from fabric.operations import *
from fabric.colors import green as _green
from fabric.colors import yellow as _yellow
from fabric.colors import red as _red
from fabric.contrib.files import *
import fabric

import dodo
import os
import sys
import time

env.project_name = 'gmailarchive'
droplet_name = 'gmailarchive'
ssh_key_name = 'gmailarchive'

def _always_run():
    print 'ALWAYS RUNNING'

def _dodo_servers():
    """
    return a list of servers named <droplet_name>
    """
    conn = dodo.connect()
    droplets = [d for d in conn.droplets() if d['name'] == droplet_name]
    return droplets

def _dodo_ssh_key_id():
    """
    Get the ID of the ssh_key up on DigitalOcean
    """
    conn = dodo.connect()
    keys = [s for s in conn.ssh_keys() if s['name'] == ssh_key_name]

    if len(keys) > 0:
        ssh_key = conn.ssh_key(keys[0]['id'])

        if ssh_key and ssh_key['ssh_pub_key'] == _dodo_public_key():
            return ssh_key['id']

    return None

def _dodo_create_ssh_key():
    """
    Crate SSH key locally
    """
    key_size = 1024
    pool = RandomPool(key_size)
    pool.stir()
    rsakey = RSA.generate(key_size, pool.get_bytes)

    with open('private/gmailarchive_rsa', 'w') as k:
        k.write(rsakey.exportKey('PEM'))
    with open('private/gmailarchive_rsa.pub', 'w') as k:
        k.write(rsakey.publickey().exportKey('OpenSSH'))

def _dodo_public_key():
    """
    Get the local public key string
    """
    key = ""
    with open('private/gmailarchive_rsa.pub', 'r') as k:
        key = k.read()
    return key

def _dodo_create_server():
    conn = dodo.connect()
    conn.new_droplet(droplet_name, size_id, 25306, 1, 4648)

def dodo_start():
    if not os.path.exists('private/gmailarchive_rsa.pub'):
        _dodo_create_ssh_key()

    # Make sure SSH KEY is there
    ssh_key_id = _dodo_ssh_key_id()
    if not ssh_key_id:
        print "\nPlease go to the DigitalOcean website and make sure you have",
        print "an SSH key with the followign:\n"
        print "name: \n" + ssh_key_name
        print "\nvalue: \n" + _dodo_public_key()
        fabric.utils.abort("SSH keys")

    # check for server
        # check for backup
            # restore backup
        # create cerver
        # start server

    conn = dodo.connect()
    droplets = _dodo_servers()

    # dodo_create_server()

    """
    while len(droplets) < 0:
        time.sleep(5)
        droplets = _dodo_servers()
    """



_always_run()
