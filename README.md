# dbSNP variants in MongoDB

## Initialising the database and loading in data
Clone the repository with git clone 

In a terminal, navigate to the local folder where the code is cloned to:
```
pip install django
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
Open a web browser and navigate to http://127.0.0.1:8000/ then select the 'Create database' option.
Upload the variants.json file available from the /resources folder to seed the database.

## User Guide
This database contains information about variants reported internationally.
Information is available about the variants and how they have been classified by clinical interpretation.

### Future improvement
* Ability to search by gene or genomic region
* if it were to be deployed, access should be password-protected and Debug mode should be turned off.
