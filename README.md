# django-forum-project
This is university project

## SETUP INSTRUCTIONS
python version >=3.8 
Create virtual environment<br>
python -m venv venv<br>
activate by executing this command<br><br>
venv/scripts/activate <br>

clone the project<br>
git clone https://github.com/chandru-shane/django-forum-project.git <br>

change to the project dir <br>
cd django-forum-project <br>
python manage.py makemigrations <br>
python manage.py migrate <br>
python manage.py runserver <br>



## API DOCUMENTATION
### API Endpoints


#### Accounts
 1. api/accounts/register/ -> POST<br>
    {
    "username":"XXXXXX",
    "email":"XXXXX@example.com",
    "password":"XXXXXXXX"
    }
 2. api/accounts/login/ -> POST<br>
    {
    "username_or_email":"XXXXX",
    "password":"XXXXXX"
    }
 3. api/accunts/login -> GET -> status code 200 successfully logged out

#### Profiles
  1. api/userprofile/username/ -> GET
  2. api/userprofile/username/<str:username>/ ->
  3. api/userprofile/follow/
  4. api/userprofile/followers/
  5. api/userprofile/following/
  6. api/userprofile/followers/<str:username>/
  7. api/userprofile/following/<str:username>/
  8. api/userprofile/isauth/
  9. api/userprofile/updateprofilepicture/
  10. api/userprofile/updateprofile/
  11. api/userprofile/search/
  12. api/userprofile/changepassword/
  
  
#### Forum (posts, comments)
  1. api/forum/home/
  2. api/forum/post/create/
  3. api/forum/comment/create/
  4. api/forum/post/<int:id>/
  5. api/forum/comment/<int:id>/
  6. api/forum/post/upvote/
  7. api/forum/post/downvote/
  8. api/forum/comment/upvote/
  9. api/forum/comment/downvote/

#### Forum Group (group, join requests)
  1. api/groups/create/
  2. api/groups/<int:id>/
  3. api/groups/join/
  4. api/groups/response/
  5. api/groups/remove/
  6. api/groups/removefromgroup/
