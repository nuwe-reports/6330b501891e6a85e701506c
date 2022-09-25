"""user routes"""
import uuid
from fastapi import APIRouter, Depends, status, Body, HTTPException
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from database import SessionLocal

import schemas
import models


def get_session():
    """get seesion function"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_user(user: schemas.UserRegister, session: Session = Depends(get_session)):
    """Creates user

    :param user: user values
    :type user: schemas.UserRegister
    :param session: sessions, defaults to Depends(get_session)
    :type session: Session, optional
    :raises HTTPException: error if user already exists
    :return: user
    :rtype: model.User
    """
    get_user = (
        session.query(models.User)
        .filter(
            (models.User.email == user.email) | (models.User.username == user.username)
        )
        .first()
    )
    if get_user:
        msg = "Email already registered"
        if get_user.username == user.username:
            msg = "Username already registered"
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=msg)

    db_user = models.User(
        id=str(uuid.uuid4()),
        username=user.username,
        email=user.email,
        password=pwd_context.hash(user.password),
        subscribed=True,
    )

    # db_user.save()
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


router = APIRouter()


@router.get("/list")
def get_items(session: Session = Depends(get_session), status_code=status.HTTP_200_OK):
    """Lists all registered users

    :param session: session, defaults to Depends(get_session)
    :type session: Session, optional
    :param status_code: defaults to status.HTTP_200_OK
    :type status_code: fastapi.status, optional
    :return: response
    :rtype: dict
    """
    items = session.query(models.User).all()
    return {"status code": status_code, "message": "OK", "body": items}


@router.post(
    "/register",
    tags=["users"],
    status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(get_session)],
    summary="Create a new user",
)
def register_user(
    user: schemas.UserRegister = Body(...),
    session: Session = Depends(get_session),
):
    """Registers a new user

    :param user: user, defaults to Body(...)
    :type user: schemas.UserRegister, optional
    :param session: session, defaults to Depends(get_session)
    :type session: Session, optional
    :return: message response
    :rtype: str
    """
    create_user(user, session)
    return "User registered"


@router.get(
    "/subscribe/{email}",
    tags=["users"],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_session)],
    summary="Subscribe user",
)
def subscribe_user(
    email: str, session: Session = Depends(get_session), status_code=status.HTTP_200_OK
):
    """Subscribes email user

    :param email: user email
    :type email: str
    :param session: _description_, defaults to Depends(get_session)
    :type session: Session, optional
    :param status_code: default status code
    :type status_code: fastapi.status , optional
    :return: _description_
    :rtype: dict
    """
    item_object = session.query(models.User).get(email)
    item_object.username = item_object.username
    item_object.email = item_object.email
    item_object.password = item_object.password
    item_object.id = item_object.id
    item_object.subscribed = True
    session.commit()

    return {
        "status code": status_code,
        "message": f"User {item_object.email} is subscribed",
    }


@router.get(
    "/unsubscribe/{email}",
    tags=["users"],
    status_code=status.HTTP_200_OK,
    dependencies=[Depends(get_session)],
    summary="Subscribe user",
)
def unsubscribe_user(
    email: str, session: Session = Depends(get_session), status_code=status.HTTP_200_OK
):
    """Unsubscribes email user

    :param email: user email
    :type email: str
    :param session: _description_, defaults to Depends(get_session)
    :type session: Session, optional
    :param status_code: default status code
    :type status_code: fastapi.status , optional
    :return: _description_
    :rtype: dict
    """
    item_object = session.query(models.User).get(email)
    item_object.username = item_object.username
    item_object.email = item_object.email
    item_object.password = item_object.password
    item_object.id = item_object.id
    item_object.subscribed = False
    session.commit()

    return {
        "status code": status_code,
        "message": f"User {item_object.email} is unsubscribed",
    }


@router.delete("/delete/{email}")
def delete_item(
    email: str, session: Session = Depends(get_session), status_code=status.HTTP_200_OK
):
    """Removes user from DB

    :param email: user email
    :type email: str
    :param session: _description_, defaults to Depends(get_session)
    :type session: Session, optional
    :param status_code: default status code
    :type status_code: fastapi.status , optional
    :return: _description_
    :rtype: dict
    """
    item_object = session.query(models.User).get(email)

    if item_object:
        session.delete(item_object)
        session.commit()
        session.close()
    else:
        raise HTTPException(
            status_code=404, detail=f"User with email {email} not found"
        )

    return {
        "status code": status_code,
        "message": f"User {email} deleted...",
        "body": item_object,
    }
