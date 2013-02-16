from fabric.api import *
# from fabric.operations import *
from fabric.colors import green as _green
from fabric.colors import yellow as _yellow
from fabric.colors import red as _red
# from fabric.contrib.files import *
import fabric

from os.path import exists
import sys
import time
import digio

env.project_name = 'gmailarchive'

digio.droplet_name = 'gmailarchive'
digio.ssh_key_name = 'gmailarchive'

#---------------------------
# DigitalOcean
#---------------------------
def docean_start():
    if not exists('private/gmailarchive_rsa.pub'):
        digio.create_ssh_key()

    # Make sure SSH KEY is there
    ssh_key_id = digio.ssh_key_id()
    if not ssh_key_id:
        print _yellow("\nPlease go to the DigitalOcean " + \
                "website and make sure you have"),
        print _yellow("an SSH key with the following:\n")
        print _green("name: \n") + digio.ssh_key_name
        print _green("\nvalue: \n") + digio.public_key()
        fabric.utils.abort("SSH keys")

    droplet = digio.droplet()

    # Need to boot a droplet
    if droplet is None:
        # check for backup
            # restore
        print _green("Creating droplet")
        droplet = digio.create_droplet(ssh_key=ssh_key_id)
        print _green("Created server with id: %s" % (droplet['id']))

    # Wait for droplet to boot or restore
    while droplet['status'] == 'new':
        print _yellow("Droplet status is '%s' waiting for boot..." % \
                (droplet['status']))
        time.sleep(10)
        droplet = digio.droplet(droplet['id'])

def docean():
    droplet = digio.droplet()

    env.key_filename = 'private/gmailarchive_rsa'
    env.hosts = [droplet['ip_address']]
    env.user = 'root'
    env.disable_known_hosts = True

#---------------------------
# Gmail Backup
#---------------------------
def gmailbackup_install():
    sudo('apt-get -y install git')

    if not exists('gmailbackup'):
        print _green("Getting gmaailbackup")
        # run('mkdir gmailbackup')
        run('wget http://gmailbackup.googlecode.com/files/gmailbackup-20100324_0051.tgz')
        run('tar -xzf gmailbackup-20100324_0051.tgz')
    else:
        print(_red('Already installed'))

