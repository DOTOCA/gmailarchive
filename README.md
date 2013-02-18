# gmailarchive - Gmail Archiving for Backup and Analysis

## TODO

* creating backup
* running backup in background

## Requirements
* [fabric](http://docs.fabfile.org/en/1.5/)
* [dodo](https://github.com/adamw523/dodo)

```
pip install -r requirements.txt
```

Configuration of `dodo` in `~/.dodo` if using DigitalOcean

## Example workflow

Clone repo

```
$ git clone https://github.com/adamw523/gmailarchive.git
```

Install requiremnets

```
$ sudo pip install -r requirements.txt
```

Check out the available actions

```
$ fab -l
Available commands:

    add_my_key      Adds your id_rsa.pub to server
    docean          Set the environment to work with DigitalOcean
    docean_destroy  Delete the DigitalOcean droplet
    docean_start    Start the DigitalOcean server. Restored from backup if exists
    install         Install the gmailbackup scripts and all required software
    run_backup      Run the backup script
    status          Summarry of the backup on the server
```

Start the server

```
$ fab docean_start

Please go to the DigitalOcean website and make sure you have an SSH key
with the following:

name: 
gmailarchive

value: 
ssh-rsa
AAAAB3NzaC1yc2EAAAADAQABAAAAgQDUn+Hz2XvDKhyb+m/Mc3X/JpwGnygCpunFGfpP38cEiFqE/sIa6ozNm/XBEyWAHP6HKHRv1xAzQIQ9qKY3/06LvJZHq10DNdeEk7IfoITKKtwwA2bEEGyTzhzPdyGx3dx8+pbtFrZZ8tvayhapWggF1l4Etovk9iep2KgeuExQhw==

Fatal error: SSH keys

Aborting.
```

Create the given SSH key at DigitalOcean and try again

```
$ fab docean_start
Creating droplet...
Created server with id: 105071
Droplet status is 'new' waiting for boot...
Droplet status is 'new' waiting for boot...
Droplet status is 'new' waiting for boot...

Done.
```

Run the backup. This could take a while.

```
$ fab docean run_backup
# required software is installed on server
192.81.213.165] Executing task 'run_backup'
[192.81.213.165] sudo: apt-get -y install git
[192.81.213.165] out: 
[192.81.213.165] out: Reading package lists... 0%
...

# the gmailbackup scripts are cloned to the server
Getting gmaailbackup
[192.81.213.165] run: git clone
https://github.com/adamw523/gmailbackup.git
[192.81.213.165] out: Cloning into 'gmailbackup'...
[192.81.213.165] out: remote: Counting objects: 1281, done.
...

# email is backed up
[192.81.213.165] out: Do you want to create a new account? [Yn] y
[192.81.213.165] out: Email: adamw523.test@gmail.com
[192.81.213.165] out: Username: [adamw523.test@gmail.com] 
[192.81.213.165] out: Server:   [imap.gmail.com] 
[192.81.213.165] out: Port:     [993] 
[192.81.213.165] out: SSL:      [True] 
[192.81.213.165] out: ### Let's rock! ###
[192.81.213.165] out: Password for "adamw523.test@gmail.com": 
[192.81.213.165] out:  NOTICE: folder 'INBOX', uidvalidity 1, last_uid 0
[192.81.213.165] out: NOTICE: folder '[Gmail]/All Mail', uidvalidity 11,
last_uid 0
[192.81.213.165] out: NOTICE: folder '[Gmail]/Drafts', uidvalidity 6,
last_uid 0
[192.81.213.165] out: NOTICE: folder '[Gmail]/Important', uidvalidity 9,
last_uid 0
[192.81.213.165] out: NOTICE: folder '[Gmail]/Sent Mail', uidvalidity 5,
last_uid 0
[192.81.213.165] out: NOTICE: folder '[Gmail]/Spam', uidvalidity 3,
last_uid 0
[192.81.213.165] out: NOTICE: folder '[Gmail]/Starred', uidvalidity 4,
last_uid 0
[192.81.213.165] out: NOTICE: folder '[Gmail]/Trash', uidvalidity 2,
last_uid 0
[192.81.213.165] out: ### BACKUP INBOX ###
[192.81.213.165] out: NOTICE: uid 1, downloading message.
[192.81.213.165] out: NOTICE: uid 1, stored message as '/root/gmailbackup/gmail/MailStore/20130216-125949-mail-noreply@google_com-Get_Gmail_on_your_mobile_phone-1.eml'.
[192.81.213.165] out: NOTICE: folder 'INBOX', last_uid 1 
...
```

Check the status of your backup

```
$ fab docean status
....

Status:
backup running       : no
number of emails     : 74
size on disk         : 796K
```


## License

MIT
