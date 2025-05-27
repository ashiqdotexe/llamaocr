import uvicorn
from fastapi import FastAPI
from routers.ocr import router as get_ocr_router
from database.ocr_database import engine
from models import ocr_model as model

model.Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(get_ocr_router)

if __name__ == "__main__":
    uvicorn.run(app, host="127.1.1.0", port=8000)
