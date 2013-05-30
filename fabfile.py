from boto.s3.connection import S3Connection
from fabric.api import *
from fabric.colors import green as _green
from fabric.colors import yellow as _yellow
from fabric.colors import red as _red
from fabric.contrib.files import append, exists

import ConfigParser
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

def docean_stop():
    """
    Shutdown the currently running droplet
    """
    digio.shutdown_droplet()


def docean_backup():
    """
    Create a backup of the DigitalOcean droplet
    """
    digio.backup_droplet()

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

#---------------------------
# S3 Backup
#---------------------------
def _s3_read_config():
    config = ConfigParser.ConfigParser()
    config.read(['private/s3.cfg'])

    # set values from config
    env.aws_id = config.get('s3', 'aws_access_key_id')
    env.aws_key = config.get('s3', 'aws_secret_access_key')
    env.s3_bucket = config.get('s3', 's3_bucket')

def s3_install():
    sudo('apt-get -y install python-pip')
    sudo('pip install boto boto_rsync')

def s3_put():
    _s3_read_config()
    
    # create bucket if it doesn't exist
    conn = S3Connection(env.aws_id, env.aws_key)
    conn.create_bucket(env.s3_bucket)

    # sync MailStore directory to S3
    run('boto-rsync -a %s -s %s /root/gmailbackup/gmail/MailStore \
            s3://%s/MailStore' % (env.aws_id, env.aws_key, env.s3_bucket))

def s3_get():
    _s3_read_config()
    
    # create bucket if it doesn't exist
    conn = S3Connection(env.aws_id, env.aws_key)
    conn.create_bucket(env.s3_bucket)

    # sync MailStore directory to S3
    run('boto-rsync -a %s -s %s s3://%s/MailStore \
            /root/gmailbackup/gmail/MailStore' % (env.aws_id,
                env.aws_key, env.s3_bucket))







