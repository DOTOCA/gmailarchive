from fabric.api import *
from fabric.colors import green as _green
from fabric.colors import yellow as _yellow
from fabric.colors import red as _red
from fabric.contrib.files import append, exists

import fabric
import os.path
import sys
import time

import digio

digio.droplet_name = 'gmailarchive'
digio.ssh_key_name = 'gmailarchive'

#---------------------------
# DigitalOcean
#---------------------------
def docean_start():
    """
    Start the DigitalOcean server. Restored from backup if exists
    """
    if not os.path.exists('private/gmailarchive_rsa.pub'):
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
        print _green("Creating droplet...")
        droplet = digio.create_droplet(ssh_key=ssh_key_id)
        print _green("Created server with id: %s" % (droplet['id']))

    # Wait for droplet to boot or restore
    while droplet['status'] == 'new':
        print _yellow("Droplet status is '%s' waiting for boot..." % \
                (droplet['status']))
        time.sleep(10)
        droplet = digio.droplet(droplet['id'])

def docean_destroy():
    """
    Delete the DigitalOcean droplet
    """
    digio.destroy_droplet()

def docean():
    """
    Set the environment to work with DigitalOcean
    """
    droplet = digio.droplet()
    if not droplet:
        fabric.utils.abort("Droplet is not running. Start it with docean_start task")

    env.key_filename = 'private/gmailarchive_rsa'
    env.hosts = [droplet['ip_address']]
    env.user = 'root'
    env.disable_known_hosts = True

def add_my_key():
    """
    Adds your id_rsa.pub to server
    """
    with open(os.path.expanduser('~/.ssh/id_rsa.pub'), 'r') as key:
        pub = key.read()
        append('~/.ssh/authorized_keys', pub)

#---------------------------
# Vagrant
#---------------------------

#---------------------------
# Gmail Backup
#---------------------------
def install():
    """
    Install the gmailbackup scripts and all required software
    """
    sudo('apt-get -y install git')
    append('~/.ssh/config', 'Host github.com')
    append('~/.ssh/config', '\tStrictHostKeyChecking no')

    if not exists('gmailbackup'):
        print _green("Getting gmaailbackup")
        run('git clone https://github.com/adamw523/gmailbackup.git')
    else:
        print(_red('Already have gmailbackup'))

def run_backup():
    """
    Run the backup script
    """
    if not exists('gmailbackup'):
        install()

    with cd('gmailbackup'):
        run('./backup_gmail.py')

def status():
    """
    Summarry of the backup on the server
    """
    running = len(run("ps aux |grep backup_gmail | grep -v grep", warn_only=True)) > 0
    num_emails = run("find gmailbackup/gmail/MailStore -name '*eml' 2> /dev/null | wc -l")
    size = run("du -sh gmailbackup/gmail/MailStore | awk '{print $1}'")

    print _green("Status:")
    print "backup running       : %s" % ('yes' if running else 'no')
    print "number of emails     : %s" % (num_emails)
    print "size on disk         : %s" % (size)

