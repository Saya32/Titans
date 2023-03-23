# Titans: Personal Spending Tracker
## 2.1. A1: Personal Spending Tracker
The goal of this project is to create an application that lets users keep track of their spending.
The expense may fall under a variety of areas.
These categories ought to be able to be added, changed, and removed by the user.
There should be an opportunity to include a title, a brief explanation, and an optional photo or file of the receipt when adding new expenditure.
Additionally, the user must to have the ability to set spending caps for each category as well as for the total expenditure over a chosen period of time.
The system ought to alert the user when the set limitations are being approached or exceeded.
Through gamification, the software should encourage the user to adhere to the objectives.
Last but not least, the user should have access to reports and visualisations for their spendings.

## Team Names
- SAYAKA BHANDARI
- JANET THOMAS ALBERT 
- JIAHAO CUI
- APRIA BENMBAREK 
- AAYUSH DWIVEDI 
- JAEHO LEE 
- CHULIANG LI 

## Installation instructions
To install the software and use it in your local development environment, you must first set up and activate a local development environment.  From the root of the project:

```
$ virtualenv venv
$ source venv/bin/activate
```

Install all required packages:

```
$ pip3 install -r requirements.txt
```

Migrate the database:

```
$ python3 manage.py migrate
```

Run all tests with:
```
$ python3 manage.py test
```

## Deployed Version
- http://sayaka.pythonanywhere.com/

User Account to login with:
- Name: Sarah
- Last: Higgins
- Email: sarah@test.com
- Password: Password123!!
- Pin: 2ersj("YY"£

## References
- We used out Knowledge from ```Clucker``` and what we learned from ```Music School Management``` to give us a structure on how to format some models, forms, views, templates and testcases for our project.
- https://stackoverflow.com/questions/52126753/understanding-image-fields-media-root-media-url
- https://simpleisbetterthancomplex.com/tutorial/2020/01/19/how-to-use-chart-js-with-django.html
