
cd incubator
mkvirtualenv -a . -p /usr/bin/python3 incubator 

pip install --editable .

echo "export FLASK_APP=flaskr 
export FLASK_DEBUG=true" >> ~/.virtualenvs/incubator/bin/postactivate

echo "export FLASK_APP=
export FLASK_DEBUG=" >> ~/.virtualenvs/incubator/bin/postdeactivate


database setup:
python
from incubator import db
db.create_all()
