from fastapi import APIRouter,status,Depends,HTTPException,Response
from sqlmodel import Session, select
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import database , schemes,utils,auth2
from .. import models
router = APIRouter(tags=['authentication'])
@router.post("/login",response_model=schemes.Token)
def login(user_credentials: OAuth2PasswordRequestForm=Depends(),session:Session=Depends(database.get_session)):
    logged_user =  session.exec(select(models.Users).where(models.Users.email == user_credentials.username)).first()
    if not logged_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'no user with specific email was found')
    
    if not utils.verify(user_credentials.password,logged_user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail='wrong credentials')
    access_token = auth2.create_access_token(data={"user_id": logged_user.id})
    return schemes.Token(access_token=access_token)