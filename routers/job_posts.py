"""job posts routes"""
from typing import Optional
from fastapi import Depends, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
import schemas
import models

from database import SessionLocal


def get_session():
    """_summary_"""
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


router = APIRouter()


@router.get("/search")
def search_items(
    session: Session = Depends(get_session),
    status_code=status.HTTP_200_OK,
    name: Optional[str] = None,
    company_name: Optional[str] = None,
    job_description: Optional[str] = None,
    skills: Optional[str] = None,
    job_type: Optional[str] = None,
    locations: Optional[str] = None,
    comments: Optional[str] = None,
):
    """_summary_

    :param session: session, defaults to Depends(get_session)
    :type session: Session, optional
    :param status_code: status code, defaults to status.HTTP_200_OK
    :type status_code: fastapi.status, optional
    :param name: name, defaults to None
    :type name: Optional[str], optional
    :param company_name: company name, defaults to None
    :type company_name: Optional[str], optional
    :param job_description: job description, defaults to None
    :type job_description: Optional[str], optional
    :param skills: skills, defaults to None
    :type skills: Optional[str], optional
    :param job_type: job type, defaults to None
    :type job_type: Optional[str], optional
    :param locations: locations, defaults to None
    :type locations: Optional[str], optional
    :param comments: commnents, defaults to None
    :type comments: Optional[str], optional
    :return: response data
    :rtype: dict
    """
    items = session.query(models.JobPost)
    if name:
        items = items.filter(models.JobPost.name.contains(name))
    if company_name:
        items = items.filter(models.JobPost.company_name.contains(company_name))
    if job_description:
        items = items.filter(models.JobPost.job_description.contains(job_description))
    if skills:
        items = items.filter(models.JobPost.skills.contains(skills))
    if job_type:
        items = items.filter(models.JobPost.job_type.contains(job_type))
    if locations:
        items = items.filter(models.JobPost.locations.contains(locations))
    if comments:
        items = items.filter(models.JobPost.comments.contains(comments))

    items = items.all()
    return {
        "status code": status_code,
        "message": f"{len(items)} jobs posts found.",
        "body": items,
    }


@router.get("/list")
def get_items(session: Session = Depends(get_session), status_code=status.HTTP_200_OK):
    """_summary_

    :param session: session, defaults to Depends(get_session)
    :type session: Session, optional
    :param status_code: status code, defaults to status.HTTP_200_OK
    :type status_code: fastapi.status_code, optional
    :return: response data
    :rtype: dict
    """
    items = session.query(models.JobPost).all()
    return {"status code": status_code, "message": "OK", "body": items}


@router.get("/{id}")
def get_item(id: int, session: Session = Depends(get_session)):
    """_summary_

    :param id: job post id
    :type id: int
    :param session: session, defaults to Depends(get_session)
    :type session: Session, optional
    :return: response data
    :rtype: dict
    """
    item = session.query(models.JobPost).get(id)
    return item


@router.post("/create", status_code=status.HTTP_201_CREATED)
def add_item(
    item: schemas.JobPost,
    session: Session = Depends(get_session),
    status_code=status.HTTP_201_CREATED,
):
    """_summary_

    :param item: _description_
    :type item: schemas.JobPost
    :param session: session, defaults to Depends(get_session)
    :type session: Session, optional
    :param status_code: status code, defaults to status.HTTP_201_CREATED
    :type status_code: fastapi.status, optional
    :return: response data
    :rtype: dict
    """
    item = models.JobPost(
        name=item.name,
        company_name=item.company_name,
        job_description=item.job_description,
        skills=item.skills,
        job_type=item.job_type,
        locations=item.locations,
        comments=item.comments,
    )
    session.add(item)
    session.commit()
    session.refresh(item)

    return {
        "status code": status_code,
        "message": f"Job post with id '{item.id}' and name '{item.name}' created",
        "body": item,
    }


@router.put("/update/{id}", status_code=status.HTTP_201_CREATED)
def update_item(
    id: int,
    item: schemas.JobPostUpdate,
    session: Session = Depends(get_session),
    status_code=status.HTTP_201_CREATED,
):
    """_summary_

    :param id: job post id
    :type id: int
    :param item: job post
    :type item: schemas.JobPostUpdate
    :param session: session, defaults to Depends(get_session)
    :type session: Session, optional
    :param status_code: status code, defaults to status.HTTP_201_CREATED
    :type status_code: fastapi.status, optional
    :return: response data
    :rtype: dict
    """
    item_object = session.query(models.JobPost).get(id)
    item_object.name = item.name if item.name is not None else item_object.name
    item_object.company_name = (
        item.company_name if item.company_name is not None else item_object.company_name
    )
    item_object.job_description = (
        item.job_description
        if item.job_description is not None
        else item_object.job_description
    )
    item_object.skills = item.skills if item.skills is not None else item_object.skills
    item_object.job_type = (
        item.job_type if item.job_type is not None else item_object.job_type
    )
    item_object.locations = (
        item.locations if item.locations is not None else item_object.locations
    )
    item_object.comments = (
        item.comments if item.comments is not None else item_object.comments
    )

    session.commit()
    return {
        "status code": status_code,
        "message": f"Job post with id '{id}' modified",
        "body": item,
    }


@router.delete("/delete/{id}")
def delete_item(
    id: int, session: Session = Depends(get_session), status_code=status.HTTP_200_OK
):
    """_summary_

    :param id: job post id
    :type id: int
    :param session: session, defaults to Depends(get_session)
    :type session: Session, optional
    :param status_code: status code, defaults to status.HTTP_200_OK
    :type status_code: fastapi.status, optional
    :raises HTTPException: error if id doesn't exist
    :return: response data
    :rtype: dict
    """
    item_object = session.query(models.JobPost).get(id)

    if item_object:
        session.delete(item_object)
        session.commit()
        session.close()
    else:
        raise HTTPException(status_code=404, detail=f"Job post with id {id} not found")

    return {
        "status code": status_code,
        "message": f"Item {id} deleted...",
        "body": item_object,
    }
