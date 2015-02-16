#!/usr/bin/env python
#CODE HELP FROM https://code.google.com/p/threepress/source/browse/trunk/bookworm/database-backup.py


import sys
import os.path
import os
import logging
from datetime import datetime
from django.conf import settings
import boto.s3

logging.basicConfig(level=logging.INFO, stream=sys.stdout)

MYSQL_CMD = 'mysqldump'
ZIP_CMD = 'zip'

def _setup(backup_dir):
    if not os.path.exists(backup_dir):
        logging.debug("Created backup directory %s" % backup_dir)
        os.mkdir(backup_dir)
    else:
        logging.debug("Using backup directory %s" % backup_dir)
    
def _backup_name(prefix="database_backup"):

    now = datetime.now()
    now_string ="%s-%s-%s_%s-%s" % (now.year, str(now.month).zfill(2), str(now.day).zfill(2), str(now.hour).zfill(2), str(now.minute).zfill(2))
    file_name = "%s_%s.sql" % (prefix, now_string)

    logging.debug("Setting backup name for as %s" % (file_name))
    return file_name

def _run_backup(file_name, backup_dir, database_settings="default"):
    user = settings.DATABASES[database_settings]['USER']
    password = settings.DATABASES[database_settings]['PASSWORD']
    name = settings.DATABASES[database_settings]['NAME']
    port = '3306'#settings.DATABASES[database_settings]['PORT']
    host = settings.DATABASES[database_settings]['HOST']
    
    #mysqldump -P 3310 -h 127.0.0.1 -u mysql_user -p database_name table_name

    cmd = "%(mysqldump)s -P %(port)s -h %(host)s -u %(user)s --password=%(password)s %(database)s > %(log_dir)s/%(file)s" % {
        'mysqldump' : MYSQL_CMD,
        'port' : port,
        'host' : host,
        'user' : user,
        'password' : password,
        'database' : name,
        'log_dir' : backup_dir,
        'file': file_name}
    logging.debug("Backing up with command %s " % cmd)
    return os.system(cmd)

def _zip_backup(file_name, backup_dir):
    backup = "%s/%s" % (backup_dir, file_name)
    zipfile_name = "%s.zip" % (backup)

    if os.path.exists(zipfile_name):
        logging.debug("Removing previous zip archive %s" % zipfile_name)
        os.remove(zipfile_name)
    zip_cmds = {'zip' : ZIP_CMD, 'zipfile' : zipfile_name, 'file' : backup }

    # Create the backup
    logging.debug("Making backup as %s " % zipfile_name)
    os.system("%(zip)s -q -9 %(zipfile)s %(file)s" % zip_cmds)

    # Test our archive
    logging.debug("Testing zip archive")
    if not os.system("%(zip)s -T -D -q %(zipfile)s" % zip_cmds):
        # If there was no problem, then delete the unzipped version
        os.remove(backup)
        return zipfile_name
    else:
        return None

def _upload_backup(bucket_name, file_name, dest_dir):
    base_name = os.path.basename(file_name)
        
    conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
    bucket = conn.get_bucket(bucket_name)

    print 'Uploading %s to Amazon S3 from %s' % (base_name, file_name)

    import sys
    def percent_cb(complete, total):
        sys.stdout.write('.')
        sys.stdout.flush()

    from boto.s3.key import Key
    k = Key(bucket)
    k.key = u"%s%s"%(dest_dir, base_name)
    k.set_contents_from_filename(file_name, cb=percent_cb, num_cb=10)

    #Remove tmp file
    os.remove(file_name)

def backup_database(bucket_name, database_settings="default", dest_dir="database/", prefix="database_backup", tmp_dir="/tmp"):
    _setup(tmp_dir)
    file_name = _backup_name(prefix)
    
    _run_backup(file_name, tmp_dir, database_settings)
    zipped_file = _zip_backup(file_name, tmp_dir)

    _upload_backup(bucket_name, zipped_file, dest_dir)
        
    
if __name__ == '__main__':
    sys.exit(main(*sys.argv))  