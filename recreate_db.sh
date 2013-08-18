psql -t template1 < recreate_db.sql
./manage.py syncdb
./manage.py migrate
