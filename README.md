
cd incubator
mkvirtualenv -a . -p /usr/bin/python3 incubator 

pip install --editable .

database setup:
```
python
from incubator import db
db.create_all()
```

Start incubator flask app with:
`python incubator.py`

Then reset the ESP8266-12e so that it registers with this flask app.
