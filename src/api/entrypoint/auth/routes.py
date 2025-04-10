from fastapi import APIRouter,Request,Depends
from src.api.entrypoint.auth import models
from src.modules.auth.handlers import check_duplicate_user,persist_user_to_db,get_user
from src.core.extensions import db_dependency
from src.core.security import hash_password,verify_password,create_access_token
from fastapi.security import  OAuth2PasswordRequestForm


router = APIRouter(prefix="/auth",tags=["Auth"])


@router.post("/SignUp")
def register_user(request: Request, model: models.UserRegisterModel,db:db_dependency):
    check_duplicate_user(db,model.username)
    # breakpoint()
    model.password = str(hash_password(model.password))
    user = persist_user_to_db(db,model)
    return user
    


@router.post("/Signin")
def login_user(request: Request,db:db_dependency, form_data: OAuth2PasswordRequestForm=Depends()):
    user=get_user(db,form_data.username)
    verify_password(form_data.password,user.password)
    access_token=create_access_token({'sub':user.username})
    return models.Token(access_token=access_token,token_type='bearer')

