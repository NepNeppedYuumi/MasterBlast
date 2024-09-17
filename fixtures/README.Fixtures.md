### Info

Fixtures are dumps of the database.
They will allow it easily setup a testdatabase, and can be manually edited.

A fixture can be created using:
`py manage.py dumpdata auth.user Blaster --exclude=Blaster.entrezaccessioncache --indent 10 -o fixtures/dev/initial.json`
https://docs.djangoproject.com/en/5.0/ref/django-admin/
See the django docs for more information on this.

A fixture can be loaded using:
`py manage.py loaddata fixtures/filename.json`
This will load all the information of the fixture in the database.

If rows with the same pk already exist in the database, they will be overwritten.
This is not an issue as you should only be working on databases that work with the required loaded fixtures to begin with.

If changes are made to the models, these changes should be made to the fixtures initial.json, and these
changes should be committed. Changes can be made manually by editing the json or by dumping the database
after migration.

We should attempt to limit the size of the fixtures, to make it easier to edit them properly whenever the database
gets migrated.