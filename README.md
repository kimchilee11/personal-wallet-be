
## For installing project environment, run following scripts in your terminal:

### On Windows:
**Create virtual env:**
```
python -m venv env
```

**Activate virtual env:**
```
env\Scripts\activate
```

*(option) If you want to deactivate:*
```
env\Scripts\deactivate
```

---

### On Linux:
**Create virtual env:**
```
python3 -m venv env
```

**Activate virtual env:**
```
source env/bin/activate
```

*(option) If you want to deactivate:*
```
source env\bin\deactivate
```

---

### Install some requirements:
```
pip install -r requirements.txt
```

---

### Migration
**Make migration file on changes:**
```
python manage.py makemigrations
```

**Make migration file on changes:**
```
python manage.py migrate
```

**Creating a empty migration file manually:**
```
python manage.py makemigrations <app> --empty
```

---

### Load initial data
**Dump data:**
```
python manage.py dumpdata --natural-foreign --natural-primary -e contenttypes -e auth.Permission --indent 2 > databsedump.json
```

**Load data:**
```
python manage.py loaddata base/fixtures/databasedump.json
```