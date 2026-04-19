# Patient Management API - Main Application
from fastapi import FastAPI, Path, HTTPException, Query
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field, computed_field
from typing import Annotated, Literal, Optional
from database import engine
from models import Base
Base.metadata.create_all(bind=engine)
from database import SessionLocal
from models import Patient as PatientModel

app = FastAPI()

class Patient(BaseModel):

    id: Annotated[str, Field(..., description='ID of the patient', examples=['P001'])]
    name: Annotated[str, Field(..., description='Name of the patient')]
    city: Annotated[str, Field(..., description='City where the patient is living')]
    age: Annotated[int, Field(..., gt=0, lt=120, description='Age of the patient')]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description='Gender of the patient')]
    height: Annotated[float, Field(..., gt=0, description='Height of the patient in mtrs')]
    weight: Annotated[float, Field(..., gt=0, description='weight of the patient in kgs')]

    @computed_field
    @property
    def bmi(self) -> float:
        bmi = round(self.weight/(self.height**2), 2)
        return bmi
    
    @computed_field
    @property
    def verdict(self) -> str:
        if self.bmi < 18.5:
            return 'underweight'
        elif self.bmi < 25:
            return 'normal'
        elif self.bmi < 30:
            return 'overweight'
        else:
            return 'obese'
        

class PatientUpdate(BaseModel):
    name: Annotated[Optional[str], Field(default=None)]
    city: Annotated[Optional[str], Field(default=None)]
    age: Annotated[Optional[int], Field(default=None, gt=0)]
    gender: Annotated[Optional[Literal['male', 'female', 'others']], Field(default=None)]
    height: Annotated[Optional[float], Field(default=None, gt=0)]
    weight: Annotated[Optional[float], Field(default=None, gt=0)]


@app.get('/')
def hello():
    return {'message':'Patient Management System API'}

@app.get('/about')
def about():
    return {'message':'A fully functional API to manage your patient records'} 

@app.get('/view')
def view():
    try:
        db = SessionLocal()
        patients = db.query(PatientModel).all()
        return patients
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')
    finally:
        db.close()

@app.get('/patient/{patient_id}')
def view_patient(patient_id: str = Path(..., description ='ID of the patient in the DB', examples = 'P001')):
    try:
        db = SessionLocal()
        patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()

        if not patient:
            raise HTTPException(status_code=404, detail='Patient not found')
        return patient
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')
    finally:
        db.close()
 
@app.get('/sort')
def sort_patients(sort_by: str = Query(..., description='sort on the basis of height, weight or bmi'), order: str = Query('asc', description='sort in asc or desc order')):
    
    valid_fields = ['height', 'weight', 'bmi']

    if sort_by not in valid_fields:
        raise HTTPException(status_code=400, detail=f'Invalid field, select from {valid_fields}')
    
    if order not in ['asc', 'desc']:
        raise HTTPException(status_code=400, detail='Invalid order select between asc or desc')
    
    try:
        db = SessionLocal()
        patients = db.query(PatientModel).all()
        sort_order = True if order == 'desc' else False
        sorted_data = sorted(patients, key=lambda X: getattr(X, sort_by, 0), reverse=sort_order)
        return sorted_data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')
    finally:
        db.close()


@app.post('/create')
def create_patient(patient: Patient):
    try:
        db = SessionLocal()
        patient_exists = db.query(PatientModel).filter(PatientModel.id == patient.id).first()
        if patient_exists:
            db.close()
            raise HTTPException(status_code=400, detail='Patient already exists')
        
        new_patient = PatientModel(
            id = patient.id,
            name = patient.name,
            city = patient.city,
            age = patient.age,
            gender = patient.gender,
            height = patient.height,
            weight = patient.weight
        )

        db.add(new_patient)
        db.commit()
        return JSONResponse(status_code=200, content={'message': 'patient created successfully'})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')
    finally:
        db.close()

@app.put('/edit/{patient_id}')
def update_patient(patient_id: str, patient_update: PatientUpdate):
    try:
        db = SessionLocal()
        patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
        if not patient:
            db.close()
            raise HTTPException(status_code=404, detail='Patient not found')   
        updated_data = patient_update.model_dump(exclude_unset=True)
        for key, value in updated_data.items():
            setattr(patient, key, value)
        db.commit()
        return JSONResponse(status_code=200, content={'message':'Patient updated'})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')
    finally:
        db.close()


@app.delete('/delete/{patient_id}')
def delete_patient(patient_id: str):
    try:
        db = SessionLocal()
        patient = db.query(PatientModel).filter(PatientModel.id == patient_id).first()
        if not patient:
            db.close()
            raise HTTPException(status_code=404, detail='Patient not found')
        db.delete(patient)
        db.commit()
        return JSONResponse(status_code=200, content={'message':'Patient record deleted'})
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')
    finally:
        db.close()

@app.get('/search')
def search_patients(name: str = Query(None), city: str = Query(None)):
    try:
        db = SessionLocal()
        patients = db.query(PatientModel)
        if name:
            patients = patients.filter(PatientModel.name.ilike(f'%{name}%'))
        if city:
            patients = patients.filter(PatientModel.city.ilike(f'%{city}%'))
        result = patients.all()
        if not result:
            raise HTTPException(status_code=404, detail='No patients found')
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Database error: {str(e)}')
    finally:
        db.close()

