import boto
from optparse import make_option
import os
import time
from time import mktime
from datetime import datetime

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


from carbon.utils.data.backup_mysql import backup_database as backup_database_mysql
from carbon.utils.data.backup_postgres import backup_database as backup_database_postgres
from carbon.utils.data.backup_sqlite import backup_database as backup_database_sqlite

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--bucket',
            action='store_true',
            dest='storage_bucket',
            default=None,
            help='AWS Storage Bucket'),
        make_option('--db',
            action='store_true',
            dest='database_name',
            default='default',
            help='Database to backup'),
        make_option('--prefix',
            action='store_true',
            dest='prefix',
            default='database_backup',
            help='Filename prefix'),
        make_option('--temp_dir',
            action='store_true',
            dest='temp_dir',
            default='/tmp',
            help='Temporary store directory'),
        make_option('--dest_dir',
            action='store_true',
            dest='dest_dir',
            default='database/',
            help='Subdirectory on AWS bucket to store backup'),
        make_option('--delete_old_backups',
            action='store_true',
            dest='delete_old_backups',
            default=True,
            help='Delete old back-ups in bucket'),
        make_option('--backups_days',
            action='store_true',
            dest='backups_days',
            default=30,
            help='How many days to keep old backups if delete_old_backups==True'),
    )

    def handle(self, *args, **options):

        if options['storage_bucket'] == None:
            try:
                bucket_name = settings.AWS_STORAGE_BUCKET_NAME_MEDIA_SECURE
            except:
                try:
                    bucket_name = settings.AWS_STORAGE_BUCKET_NAME
                except:
                    bucket_name = None
        else:
            bucket_name = options['storage_bucket']

        if bucket_name:
            print "Going to dump database %s into bucket %s using file prefix %s temp store to %s then store in folder %s"%(options['database_name'], bucket_name, options['prefix'], options['temp_dir'], options['dest_dir'])

            

            if options['database_name'] in settings.DATABASES:
                db = settings.DATABASES[options['database_name']]
                db_engine = db['ENGINE']
                if 'mysql' in db_engine.lower():
                    backup_database_mysql(bucket_name, options['database_name'], options['dest_dir'], options['prefix'], options['temp_dir'])

                elif 'postgresql_psycopg2' in db_engine.lower():
                    backup_database_postgres(bucket_name, options['database_name'], options['dest_dir'], options['prefix'], options['temp_dir'])

                elif 'sqlite3' in db_engine.lower():
                    backup_database_sqlite(bucket_name, options['database_name'], options['dest_dir'], options['prefix'], options['temp_dir'])
                    
            else:
                print "ERROR: No database found with name %s in settings.DATABASES"%(options['database_name'])

            if options['delete_old_backups']:
                conn = boto.connect_s3(settings.AWS_ACCESS_KEY_ID, settings.AWS_SECRET_ACCESS_KEY)
                bucket = conn.get_bucket(bucket_name)
                max_days = int(options['backups_days'])
                now = datetime.now()
                if max_days > 0:                    
                    for key in bucket:                                          
                        if options['prefix'] in key.name:

                            try:
                                #Unfortunately S3/boto doesn't provide a created date and the modified date updates anytime you look at it
                                #So we're going off the filename
                                created = time.strptime(key.name, options['dest_dir']+options['prefix']+'_%Y-%m-%d_%H-%M.sql.zip')
                                
                                #convert to datetime
                                created_dt = datetime.fromtimestamp(mktime(created))
                                diff_dy = now - created_dt
                                if diff_dy.days > max_days:
                                    print "Delting %s, which is %s days old"%(key.name, diff_dy.days)
                                    key.delete()
                            except:
                                pass
                        



