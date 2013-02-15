from base64 import b64encode
from Crypto.PublicKey import RSA
from Crypto.Util.randpool import RandomPool
from fabric.api import *
from fabric.operations import *
from fabric.colors import green as _green
from fabric.colors import yellow as _yellow
from fabric.colors import red as _red
from fabric.contrib.files import *

import dodo
import os
import sys
import time

env.project_name = 'gmailarchive'
droplet_name = 'gmailarchive'

def _always_run():
    print 'ALWAYS RUNNING'

def _dodo_servers():
    droplets = [d for d in conn.droplets() if d['name'] == droplet_name]
    return droplets

def dodo_create_ssh_key():
    #keystring = 'ssh-rsa %s ' % (b64key)

    key_size = 1024

    pool = RandomPool(key_size)
    pool.stir()

    rsakey = RSA.generate(key_size, pool.get_bytes)

    with open('private/gmailarchive_rsa', 'w') as k:
        k.write(rsakey.exportKey('PEM'))
    with open('private/gmailarchive_rsa.pub', 'w') as k:
        k.write(rsakey.publickey().exportKey('OpenSSH'))

def dodo_create_server():
    conn = dodo.connect()
    conn.new_droplet(droplet_name, size_id, 25306, 1, 4648)

def dodo_start_server():

    conn = dodo.connect()
    droplets = _dodo_servers()

    dodo_create_server()

    while len(droplets) < 0:
        time.sleep(5)
        droplets = _dodo_servers()



_always_run()
