# How to deploy your cs50 web to heroku

## General info
> This README is about step by step how to deploy your cs50 web exercises (django app) to heroku.

## Table of contents
- [How to deploy your cs50 web to heroku](#how-to-deploy-your-cs50-web-to-heroku)
  - [General info](#general-info)
  - [Table of contents](#table-of-contents)
  - [Setup](#setup)
  - [Deployment](#deployment)

## Setup

1. ### [Download and Install Heroku](https://devcenter.heroku.com/articles/heroku-cli#download-and-install)

2. ### [Verify installation](https://devcenter.heroku.com/articles/heroku-cli#verifying-your-installation)
   ```bash
   heroku --version
   ```

3. ### Login to heroku
   ```bash
   heroku login
   ```
   and enter your username and password

4. ### Go to project folder
   1. #### Add Procfile
      * Bash
      ```bash
      echo "web: gunicorn (your app name here).wsgi --log-file -" >  Procfile
      ```
      * Powershell
      ```powershell
      Write-Output "web: gunicorn (your app name here).wsgi --log-file -" > Profile
      ```   
   2. #### Add these packages below to requirements.txt
      * django
      * gunicorn 
      * whitenoise (static file)
      * dj-database-url (**This simple Django utility allows you to utilize the 12factor inspired DATABASE_URL environment variable to configure your Django application.**)
      * psycopg2-binary (postgres lib)
      
      Or using command below

      * Bash
      ```bash
      echo "django\ngunicorn\nwhitenoise\ndj-database-url\npsycopg2-binary" > requirements.txt
      ```
      * Powershell
      ```powershell
      Write-Output "django\ngunicorn\nwhitenoise\ndj-database-url\npsycopg2-binary" > requirements.txt
      ```
   3. #### Add runtime.txt
      * Bash
      ```bash
      echo "python-(insert version here)" >  Procfile
      ```
      * Powershell
      ```powershell
      Write-Output "python-(insert version here)" > Profile
      ```
   4. #### Open Settings.py in your root app
      1. ##### Add this line
      ```python
      import dj_database_url
      ```
      2. ##### Copy your **SECRET_KEY** to another file and change line below
      ```python
      SECRET_KEY = 'Your sercret key here'
      ```
      To
      ```python
      SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
      ```
      3. ##### Set Debug mode equals to False
      ```python
      DEBUG = config('DEBUG', default=False, cast=bool)
      ```
      4. ##### Allow .herokuapp.com
      ```python
      ALLOWED_HOSTS = [".herokuapp.com"]
      ```
      5. ##### Add this line to MIDDLEWARE
      ```python
      'whitenoise.middleware.WhiteNoiseMiddleware'
      ```
      6. ##### Change these lines below from
      ```python
      DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
         }
      }
      ```
      To 
      ```python
      DATABASES = {
          'default': dj_database_url.config(conn_max_age=600, ssl_require=True)
      }
      ```
      Or 
      ```python
      DATABASES = {
         'default': dj_database_url.config(
            default=config('DATABASE_URL')
         )
      }
      ```
      1. ##### Add these lines
      ```python
      STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

      STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
      ```
      * Above line
      ```python
      STATIC_URL = '/static/'
      ```

## Deployment

1. ### Create a Heroku App

```bash
heroku create (your app name here)
```

2. ### Add a PostgresSQL database to your app

```bash
heroku addons:create heroku-postgresql:hobby-dev -a (your app name here)
```

3. Login to [Heroku Dashboard](https://id.heroku.com/login) and access your recently created app
   
4. Click on the **Settings** menu and then on the button **Reveal Config Vars**

5. Add all the Environment variables (example SECRET_KEY, DATABASE_URL)

6. Run command below in your current project folder
```bash
git init
git remote add heroku https://git.heroku.com/your-app-name.git
git add .
git commit
git push heroku master
```

7. Run migration for your app
```bash
heroku run python manage.py migrate -a (your app name here)
```
8. Enjoy your app at 
```
https://your-app-name.herokuapp.com/.
```
