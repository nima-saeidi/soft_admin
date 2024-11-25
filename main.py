from fastapi import Form, FastAPI, Depends, HTTPException, status,UploadFile, File
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from jose import JWTError, jwt
import models
import schemas
import auth_utils
from database import engine, SessionLocal
from pathlib import Path
import shutil

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# JWT Token dependency
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="admin/login")


# JWT Decoding
def get_current_admin(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, auth_utils.SECRET_KEY, algorithms=[auth_utils.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    admin = db.query(models.Admin).filter(models.Admin.username == username).first()
    if admin is None:
        raise credentials_exception
    return admin


# Register Admin
@app.post("/admin/register/", status_code=201)
def register_admin(admin: schemas.AdminCreate, db: Session = Depends(get_db)):
    existing_admin = db.query(models.Admin).filter(models.Admin.username == admin.username).first()
    if existing_admin:
        raise HTTPException(status_code=400, detail="Username already registered")
    hashed_password = auth_utils.hash_password(admin.password)
    new_admin = models.Admin(username=admin.username, hashed_password=hashed_password)
    db.add(new_admin)
    db.commit()
    db.refresh(new_admin)
    return {"message": "Admin registered successfully"}


# Admin Login
@app.post("/admin/login/", response_model=schemas.Token)
def login_admin(login_data: schemas.AdminLogin, db: Session = Depends(get_db)):
    admin = db.query(models.Admin).filter(models.Admin.username == login_data.username).first()
    if not admin or not auth_utils.verify_password(login_data.password, admin.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")
    access_token = auth_utils.create_access_token(data={"sub": admin.username})
    return {"access_token": access_token, "token_type": "bearer"}

# Protected Create Item
@app.post("/admin/create-item/", status_code=201)
async def create_item(
        title: str = Form(...),  # Expect `title` from form-data
        description: str = Form(...),  # Expect `description` from form-data
        image: UploadFile = File(...),  # Expect `image` as a file
        db: Session = Depends(get_db),
        current_admin: models.Admin = Depends(get_current_admin)
):
    # Save the uploaded file
    uploads_path = Path("uploads")
    uploads_path.mkdir(parents=True, exist_ok=True)  # Ensure the uploads directory exists
    image_path = uploads_path / image.filename

    with image_path.open("wb") as buffer:
        shutil.copyfileobj(image.file, buffer)

    # Create a new item in the database
    new_item = models.Item(
        title=title,
        description=description,
        image_path=str(image_path)
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)

    return {"id": new_item.id, "title": new_item.title, "image_path": new_item.image_path}

# List Items (Protected)
@app.get("/admin/items/", status_code=200)
def get_items(db: Session = Depends(get_db), current_admin: models.Admin = Depends(get_current_admin)):
    items = db.query(models.Item).all()
    return items
