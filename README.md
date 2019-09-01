# SRM Academia API - Python
This Repository is an unofficial API for Academia which is Online Portal developed by ZOHO for SRM University Katankulathur in order to show students their Attendance, Marks, TimeTable and other useful details. There was no official API of Academia when I wrote this piece of code but as of now WISOPT approached ZOHO and got their API.

## DEMO 
```
https://academia-yogesh.herokuapp.com
```

## Getting Access Token Of User
```
https://academia-yogesh.herokuapp.com/token?email=****@srmuniv.edu.in&pass=***
```
Here I am using GET request but you may change the code to use POST requests.
The above url would the token if the request was successful.
Store the token to use it in the future.

## Getting Attendance and Marks Of User
```
https://academia-yogesh.herokuapp.com/AttAndMarks?token={{token}}
```
This would give you the Attendance and the Marks of the User.

## Getting Personal Details Of User
```
https://academia-yogesh.herokuapp.com/PersonalDetails?token={{token}}
```
This would give you the Personal Details of the User.

## Getting TimeTable Of User
```
https://academia-yogesh.herokuapp.com/TimeTable?token={{token}}&batch={{1 or 2}}
```
This would give you the TimeTable of the User based on the batch.

#### The code might need to be changed if any changed have been made in the Academia website. If you find any bug please write to me about it.



