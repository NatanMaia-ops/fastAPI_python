from http import HTTPStatus

from fastapi import FastAPI, HTTPException

from fast_zero.schemas import Message, UserDB, UserList, UserPublic, UserSchema

app = FastAPI(title="Minha API BALA")

database = []


@app.get("/", response_model=Message, status_code=HTTPStatus.OK)
def read_root():
    return {"message": "Olá Mundo!"}


@app.get("/users/", response_model=UserList, status_code=HTTPStatus.OK)
def read_users():
    return {"users": database}


@app.post("/users/", status_code=HTTPStatus.CREATED, response_model=UserPublic)
def create_user(user: UserSchema):
    user_with_id = UserDB(
        username=user.username,
        email=user.email,
        password=user.password,
        id=len(database) + 1,
    )
    # aqui precisamos criar um novo modelo que represente o banco
    # precisamos de um identificador para esse registro

    database.append(user_with_id)

    return user_with_id


@app.put(
    "/users/{user_id}", response_model=UserPublic, status_code=HTTPStatus.OK
)
def update_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )

    user_with_id = UserDB(**user.model_dump(), id=user_id)
    database[user_id - 1] = user_with_id

    return user_with_id


@app.delete(
    "/users/{user_id}", response_model=UserPublic, status_code=HTTPStatus.OK
)
def delete_user(user_id: int, user: UserSchema):
    if user_id > len(database) or user_id < 1:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND, detail="User not found"
        )

    return database.pop(user_id - 1)
