<h1>Introduction</h1> 

Interview API provides filtering on Interview Table and creating interview data for interviewers and candidates.
Person who first acts picks the time slot and the other should use interview id and submit personal data. 
Each interview would be scheduled and ready to return as a result for Interview API when both side submitted their data.

## Installation

First, start by closing the repository:

```
git clone https://github.com/zeyytas/Interview-API.git
```

- Build the instances
```
docker-compose build
```

- Start-up
```
docker-compose up
```
## Tests 

``` python manage.py test interviewapp.tests.InterviewTests ```


## Requests

<small>

```
GET         /api/{api-version}/interview/? </small> </br>
POST        /api/{api-version}/interview/ </small> </br>
PUT         /api/{api-version}/interview/:id/ </small> </br>
```

## Attributes

<small>
   
   - Interview id

    ```e.g.   ?id=20```
   
   - Slot </br>
   Since working hours generally between 9am to 6pm, time slot choices are available between 9 to 18.

    ```e.g.   ?slot=18```
   
   - Interviewer email </br>
   This attribute can contain one or more interviewer emails.

    ```e.g.   ?interviewer_email=interviewer1@gmail.com,interviewer2@gmail.com```


   - Candidate email

    ```e.g.   ?candidate_email=candidate@gmail.com```
   
   - Page & per_page </br>
   Default page size is 100.

    ```e.g.   ?page=2&per_page=50```
  
</small>
