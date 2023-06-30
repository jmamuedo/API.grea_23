from typing import Optional,List
from datetime import *

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from .database import SessionLocal
import os

from . import models

db = any

# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

fake_users_db = {
    "ericstein": {
        "username": "ericstein",
        "full_name": "Eric Stein",
        "email": "Eric.Stein@fmc.com",
        "hashed_password": "$2b$12$jfX0M.C/UaCkwpL0/EzSW.AXi79mA9e//XCVT1Kjvnzw0lrAWfr1a",
        "disabled": False,
    },
    "jmamuedo": {
        "username": "jmamuedo",
        "full_name": "Jose Maria Amuedo",
        "email": "josemaria.amuedo@ec2ce.com",
        "hashed_password": "$2b$12$65R3jg1xLq5tUQjhDq1Meu1MlfTTZwlzbxICXO.PPU.aaefEdlxZe",
        "disabled": False,
    },
    "fmcprecisionag": {
        "username": "fmcprecisionag",
        "full_name": "FMC",
        "email": "fmcprecisionag@fmc.com",
        "hashed_password": "$2b$12$VuLDHXIpzIkWnYvghQ2t7e7/zndXskc3H11QwDCI9W1nAVIuuL4T2",
        "disabled": False,
    },
}


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: Optional[str] = None


class User(BaseModel):
    username: str
    email: Optional[str] = None
    full_name: Optional[str] = None
    disabled: Optional[bool] = None


class UserInDB(User):
    hashed_password: str


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

description = """
API-ec2ce helps you get our AI data. 🚀

## Real_Data

You can **get all real data**.

## Pred_Data

You can **get all pred data** filter by pred_time (2021-09-12).

## Spatial_Data

You can **get all spatial data** filter by country id (IT, ES, GR).

"""

app = FastAPI(title='API-ec2ce',
            version='Bactrocera oleae v0.2',
            description=description,
            redoc_url=None)


try:
    db=SessionLocal()
except:
    db.rollback()

# class Pred(BaseModel):
# 	id: int
# 	id_trap: str
# 	pred_time: date
# 	type: int
# 	h1: Optional[float] = Field(..., nullable=True)
# 	h2: Optional[float] = Field(..., nullable=True)
# 	h3: Optional[float] = Field(..., nullable=True)
# 	h4: Optional[float] = Field(..., nullable=True)
# 	ph1: Optional[float] = Field(..., nullable=True)

# 	class Config:
# 		orm_mode = True
                
class Municipios(BaseModel):
    id_dera: int
    cod_mun: str
    nombre: str
    provincia: str

    class Config:
        orm_mode = True

class PEM(BaseModel):
    id: int
    cod_mun: str
    estado: str
    fecha_h: Optional[date] = Field(..., nullable=True)
    fecha_r1: Optional[date] = Field(..., nullable=True)
    fecha_r2: Optional[date] = Field(..., nullable=True)
    h_r: Optional[str] = Field(..., nullable=True)
    programa: Optional[str] = Field(..., nullable=True)

    class Config:
        orm_mode = True

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@app.post("/token/", response_model=Token, tags=["token"])
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get('/municipio',response_model=List[Municipios],status_code=status.HTTP_200_OK)
def get_all_pred(id_dera:str,current_user: User = Depends(get_current_active_user)):

     if id_dera == '0':
        pred=db.query(models.Municipios).all()
     else:    
        pred=db.query(models.Municipios).filter(models.Municipios.id_dera==id_dera).all()
     return pred

@app.get('/pem',response_model=List[PEM],status_code=status.HTTP_200_OK)
def get_all_pred(cod_mun:str,current_user: User = Depends(get_current_active_user)):
    
    pred=db.query(models.PEM).filter(models.PEM.cod_mun==cod_mun).all()

    return pred


# @app.get('/real_data',
# response_model=List[Real],status_code=status.HTTP_200_OK)
# def get_filter_real_dates(id_trap:str,start_date:date,end_date:date,
#                 current_user: User = Depends(get_current_active_user)):
#     real_filter_dates=db.query(models.Real).filter(models.Real.id_trap==id_trap,
#                   models.Real.date>=start_date,models.Real.date<=end_date).all()
#     return real_filter_dates

# @app.get('/pred_data',response_model=List[Pred],status_code=status.HTTP_200_OK)
# def get_all_pred(pred_time:date,current_user: User = Depends(get_current_active_user)):

#     pred=db.query(models.Pred).filter(models.Pred.pred_time==pred_time).all()
#     return pred

# @app.get('/spatial_data',response_model=List[Spatial])
# def get_country_spatial(country:str,current_user: User = Depends(get_current_active_user)):
#     country_spatial=db.query(models.Spatial).filter(models.Spatial.country==country).all()
#     return country_spatial

#@app.get('/spatial_data/country={country}&region={region}',response_model=List[Spatial])
#def get_counreg_spatial(country:str,region:str,current_user: User = Depends(get_current_active_user)):
#    counreg_spatial=db.query(models.Spatial).filter(models.Spatial.country==country,
#    models.Spatial.region==region).all()
#    return counreg_spatial
