from bson import ObjectId
import motor.motor_asyncio

from dotenv import load_dotenv
import os

load_dotenv()


sample_patient = {
    "_id": ObjectId("605c72ef1532071e9f9372f1"),
    "name": "Rishav",
    "last_visit_date": "03-Oct-24",
    "last_visit_type": "op",
    "doctor": "Dr. P N GUPTA",
    "medical_history": {
        "key_findings": [],
        "clinical_representation": [
        "Urea aur creatinine ka level bahut high hai (Urea: 117.0, Creatinine: 6.4), jo kidney ko properly kaam karne mein problem bata raha hai.",
        "Alkaline Phosphatase aur GGTP ka level bhi kafi high hai (Alkaline Phosphatase: 437.0, GGTP: 416.0), jo liver issues bhi indicate kar sakta hai.",
        "Ferritin thoda jyada hai (Ferritin: 699.0), jo inflammation ya iron overload ka sign ho sakta hai.",
        "RDW bahut high hai (RDW: 19.4), jo different size ki red blood cells ko indicate karta hai, anemia ke potential issues ko batata hai."
        ],
        "procedures_done": [],
        "medications": []
    },
    "care_plan": {
        "primary_goal": {
        "consultations": [
            {
            "department": "Nephrology",
            "is_booked": False
            },
            {
            "department": "Hepatology",
            "is_booked": False
            }
        ],
        "lab_screenings": [
            {
            "evidence": "To monitor and assess the progression of kidney damage.",
            "name": "Kidney Function Test"
            },
            {
            "evidence": "To evaluate the extent of liver damage and monitor therapy effectiveness.",
            "name": "Liver Function Test"
            }
        ],
        "next_visit_date": "2024-12-19T05:46:18.834000"
        }
    },
    "cohort": "Nephrology"
}

mongo_client = motor.motor_asyncio.AsyncIOMotorClient(os.getenv("MONGO_URI"))
mongo_db = mongo_client[os.getenv("DB_NAME")]
patient_collection = mongo_db[os.getenv("PATIENT_COLLECTION")]
chat_collection = mongo_db[os.getenv("CHAT_COLLECTION")]

async def init_db():
    await patient_collection.update_one(
        filter={"_id": sample_patient["_id"]},
        update={"$set": sample_patient},
        upsert=True
    )

def close_db():
    mongo_client.close()