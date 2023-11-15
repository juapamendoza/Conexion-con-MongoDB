from fastapi import FastAPI, HTTPException, status
from db.models.User import User
from db.schemas.userSchema import user_schema
from db.db import connection

app = FastAPI()

@app.get("/userdb/")
async def usersclass():
    users_list = []
    try:
        for userdb in connection.Computacion.ModelosWEB.find():
            userJSON = user_schema(userdb)
            users_list.append(User(**userJSON))
        return users_list
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.get("/userdb/{username}")
async def usersclass(username:str):
    try:
        new_user = user_schema(connection.Computacion.ModelosWEB.find_one({"username":username}))
        return User(**new_user)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
        
@app.post("/userdb/")
async def usersclass(user:User):
    user_dict = dict (user) #convertir de User a JSON
    del user_dict["id"] #eliminar id
    id = connection.Computacion.ModelosWEB.insert_one(user_dict).inserted_id
    new_user = user_schema(connection.Computacion.ModelosWEB.find_one({"_id":id}))
    return User(**new_user)

@app.put("/userdb/{username}", response_model=User)
async def usersclass(user: User, username:str):
    newusername = user.username
    full_name = user.full_name
    email = user.email
    phone = user.phone
    disabled = user.disabled

    filtro = {"username":username}
    newvalues = {"$set":{"full_name":full_name,
                         "email":email,
                         "phone":phone,
                         "disabled":disabled,
                         "username":newusername}}

    try:
        connection.Computacion.ModelosWEB.update_one(filtro,newvalues)
        new_user = user_schema(connection.Computacion.ModelosWEB.find_one({"username":newusername}))
        return User(**new_user)
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)

@app.delete("/userdb/{username}")
async def usersclass(username:str):
    try:
        connection.Computacion.ModelosWEB.delete_one({"username":username})
        return {"Usuario eliminado"}
    except:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
"""
"id": "",
"username": "User1",
"full_name": "Username Uno",
"email": "user@example.com",
"phone": "222 222 2222",
"disabled": false
"""
