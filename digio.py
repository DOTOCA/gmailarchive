from Crypto.PublicKey import RSA
from Crypto.Util.randpool import RandomPool
import dodo

ssh_key_name = 'digio_default_ssh'
droplet_name = 'digio_default_name'

def status():
    pass

# Droplet

def backup_droplet():
    d = droplet()
    conn = dodo.connect()
    res = conn.snapshot_droplet(d['id'])

def create_droplet(size=66, ssh_key=None, region=1, image=25306):
    conn = dodo.connect()
    dstart = conn.new_droplet(droplet_name, size, image, region, ssh_key)
    return droplet(dstart['id'])

def destroy_droplet():
    d = droplet()
    if d:
        conn = dodo.connect()
        dstart = conn.destroy_droplet(d['id'])

def droplet_ids():
    """
    return a list of droplets named <droplet_name>
    """
    conn = dodo.connect()
    return [d for d in conn.droplets() if d['name'] == droplet_name]

def droplet(droplet_id=None):
    # get droplet_id if not passed in
    if droplet_id is None:
        ds = droplet_ids()
        if len(ds) > 0:
            droplet_id =  ds[0]['id']
        else:
            return None

    conn = dodo.connect()
    droplet = conn.show_droplet(droplet_id)
    return droplet

# SSH

def ssh_key_id():
    """
    Get the ID of the ssh_key up on DigitalOcean
    """
    conn = dodo.connect()
    keys = [s for s in conn.ssh_keys() if s['name'] == ssh_key_name]

    if len(keys) > 0:
        ssh_key = conn.ssh_key(keys[0]['id'])

        if ssh_key and ssh_key['ssh_pub_key'] == public_key():
            return ssh_key['id']

    return None

def create_ssh_key():
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

    run('chmod 600 private/gmailarchive_rsa*')

def public_key():
    """
    Get the local public key string
    """
    key = ""
    with open('private/gmailarchive_rsa.pub', 'r') as k:
        key = k.read()
    return key

