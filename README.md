# API documentation

To make a request for all users: 
```/user/```  
Request for all events: 
```/events/```  
For a specific event or user: ```/events/1``` or ```/users/1```  
To login: ```/rest-auth/login```  

requires body:

{"email": "lucas", "password": "puppies"}

Register: ```/rest-auth/register```

requires body:

{"username": "", "email": "", "password1": "", "password2", "", "organization": ""}
