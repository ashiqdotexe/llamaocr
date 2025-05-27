from fastapi.responses import JSONResponse
from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm import Session
from database.ocr_database import get_db
from models.ocr_model import User, ChatHistory
from schemas.ocr_schemas import UserCreate, ChatHistoryCreate
from datetime import datetime
from core.config import TOGETHER_API_KEY
from dotenv import load_dotenv
from together import Together
import os

load_dotenv()

router = APIRouter()

os.environ["TOGETHER_API_KEY"] = TOGETHER_API_KEY

model = "meta-llama/Llama-Vision-Free"

client = Together()

getDescriptionPrompt = """
You are an expert in extracting information from passport images. Given an image of a passport, extract the following details:
- Full Name
- Date of Birth
- Gender
- Nationality
- Passport Number
- Issue Date
- Expiry Date

Please provide the extracted information in a JSON response format.
"""


@router.post("/process-passport/", tags=["Response"])
async def process_passport(request: UserCreate, db: Session = Depends(get_db)):
    try:
        # Check if the user already exists
        user = db.query(User).filter(User.user_id == request.user_id).first()
        if not user:
            # Create a new user if not exists
            user_data = User(
                user_id=request.user_id, url=str(request.url), service=request.service
            )
            db.add(user_data)
            db.commit()
            db.refresh(user_data)
        else:
            user_data = user

        # Mock LLAMAOCR processing logic (replace with real implementation)
        stream = client.chat.completions.create(
            model="meta-llama/Llama-3.2-11B-Vision-Instruct-Turbo",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": getDescriptionPrompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": str(request.url),
                            },
                        },
                    ],
                }
            ],
            stream=True,
        )

        extracted_content = ""

        for chunk in stream:
            if hasattr(chunk, "choices") and chunk.choices:
                if hasattr(chunk.choices[0], "delta"):
                    if hasattr(chunk.choices[0].delta, "content"):
                        content = chunk.choices[0].delta.content
                        if content is not None:
                            extracted_content += content

        # Log the chat history
        chat_history = ChatHistory(
            user_id=user_data.id,
            search_history=extracted_content,
            last_updated=datetime.now(),
        )
        db.add(chat_history)
        db.commit()

        cleaned_content = (
            extracted_content.replace("\n", " ")
            .replace("\t", "")
            .replace("*", "")
            .replace("+", "")
            .strip()
        )
        formatted_response = cleaned_content.replace("  ", "\n")
        return JSONResponse(content={"Response": formatted_response})

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
