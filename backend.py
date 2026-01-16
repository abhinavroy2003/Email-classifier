from fastapi import FastAPI
from pydantic import BaseModel, Field, computed_field, EmailStr,AnyUrl
from fastapi.responses import JSONResponse
from typing import Literal,Annotated

import joblib
import pandas as pd

with open('email_classifier_model.pkl','rb') as f:
    model = joblib.load(f)

# Try to load vectorizer, if not available, create new one
try:
    with open('vectorizer.pkl','rb') as f:
        vectorizer = joblib.load(f)
except FileNotFoundError:
    from sklearn.feature_extraction.text import TfidfVectorizer
    vectorizer = TfidfVectorizer(stop_words='english', max_features=3000)

app = FastAPI()

class Parent(BaseModel):
    user_email:Annotated[str, Field(...,description ='Enter the email we want to classify into the spam or not spam')]


@app.get('/')
def welcome():
    return {
        'message' : "welcome to this pannel of Spam classifier"
    }


@app.post('/predict')
def predict(data : Parent):
    # Vectorize the email text using the pre-fitted vectorizer
    vectorized_email = vectorizer.transform([data.user_email])
    
    # Make prediction
    prediction = model.predict(vectorized_email)[0]
    
    # Convert numpy type to native Python type for JSON serialization
    prediction = int(prediction) if hasattr(prediction, 'item') else int(prediction)

    return JSONResponse(status_code=200, content={'predicted':prediction})
