# {{ project_name }} - API

## How to install

```bash
$ django-admin.py startproject \
  --template=https://github.com/ivlevdenis/django_template/archive/master.zip \
  --extension=py,md,env,html,yml \
  project_name
$ cp docker/.dockerenv.example .dockerenv
$ python3.7 -m venv venv
$ source venv/bin/activate
$ pip install -r project/requrements.txt
```