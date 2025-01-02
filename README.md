# Docscribe demo app

## Overview

This is a demo backend which will get a patient's medical history stored in the Database and enable patients to get information regarding their medications, medical procedures done and answers from recent consulation from a doctor.

---

## Setup

Before running the app, ensure that you have the following dependencies installed:

### Mongo DB
- Make sure you have a valid connection string for mongo db. You can locally install and setup mongo db or use the free cloud version from mongo atlas.
- It is highly recommended to download mongo compass easily manage the created collections.

### .env
- In the root folder create a file named .env with the following to be used as environmental variables

   ```.env
   MONGO_URI=<mongo connection string>
   DB_NAME=<your database name in mongodb>
   PATIENT_COLLECTION=<your collection name for patients>
   CHAT_COLLECTION=<your collection name for chat data>
   OPENAI_KEY=<openai api-key>
   OPENAI_CHAT_MODEL=<openai model name to use> # gpt-4o-mini recommended
   ```


### uv
- If you have python already installed. Run the following command to install uv

   ```bash
   pip install uv
   ```
- If you don't have python refer the link to install uv: https://docs.astral.sh/uv/getting-started/installation/

---

## Running the app

Once all the setup is done, run the following command.

   ```bash
   uv run uvicorn main:app
   ```

Once you run this command, it will
- download and install the needed python version if not already present locally.
- create a virtual environment
- download and install all the dependencies needed to run the app.
- Bring up a web server at localhost:8000

From the second run onwards use this command
   ```bash
   uvicorn main:app
   ```

## API Usage

### GET localhost:8000/chat/patient/{patient_id}
- Check if the medical history of patient exists. If it exists gives back the last unfinished chat details else gives instructions to upload medical history.

- case 1:
If medical history is not present for the patient:
   ```json
   {
      "type": "message",
      "content": [
         {
            "role": "assistant",
            "content": "We don't have your medical history. Please reach out to abcd@efg.com for uploading your medical history."
         }
      ]
   }
   ```

- case 2:
If medical history upload has already been initiated :
   ```json
   {
      "type": "message",
      "content": [
         {
            "role": "assistant",
            "content": "Your medical history upload is being processed. Please try after some time or reach out to abcd@efg.com for updates."
         }
      ]
   }
   ```

- case 3:
If medical history exists:
   ```json
   {
      "type": "chat_history",
      "content": {
         "chat_id": "67758d8988ea3d1c85f6e3b0",
         "chat_history": [
               {
                  "role": "system",
                  "content": "You are a helpful chat bot ..."
               }
         ]
      }
   }
   ```

### POST localhost:8000/chat?patient_id={patient_id}
- Create a new chat session for the patient.
- sample response
   ```json
   {
      "chat_id": "67758d8988ea3d1c85f6e3b0",
      "chat_history": [
         {
               "role": "system",
               "content": "You are a helpful chat bot ..."
         }
      ]
   }
   ```

### PUT localhost:8000/chat
- Continue with an already created chat session.
- sample request data
   ```json
   {
      "chat_id": "67758d8988ea3d1c85f6e3b0",
      "chat_history": [
         {
               "role": "system",
               "content": "You are a helpful chat bot ..."
         },
         {
               "role": "user",
               "content": "How is my liver ?"
         },
         {
               "role": "assistant",
               "content": "Based on your medical history, your liver function may be a concern as your Alkaline Phosphatase and GGTP levels are quite high (Alkaline Phosphatase: 437.0, GGTP: 416.0). These elevated levels can indicate potential liver issues. It's important to discuss these findings with your healthcare provider for a thorough evaluation and appropriate management.\n\nIf you have any other specific questions about your medical history, feel free to ask!"
         }
      ],
      "question": "What is Alkaline Phosphatase and what is the optimal limit ?"
   }
   ```
- sample response
   ```json
   {
      "chat_id": "67758d8988ea3d1c85f6e3b0",
      "chat_history": [
         {
               "role": "system",
               "content": "You are a helpful chat bot ..."
         },
         {
               "role": "user",
               "content": "How is my liver ?"
         },
         {
               "role": "assistant",
               "content": "Based on your medical history, your liver function may be a concern as your Alkaline Phosphatase and GGTP levels are quite high (Alkaline Phosphatase: 437.0, GGTP: 416.0). These elevated levels can indicate potential liver issues. It's important to discuss these findings with your healthcare provider for a thorough evaluation and appropriate management.\n\nIf you have any other specific questions about your medical history, feel free to ask!"
         },
        {
            "role": "user",
            "content": "What is Alkaline Phosphatase and what is the optimal limit ?"
        },
        {
            "role": "assistant",
            "content": "Alkaline Phosphatase (ALP) is an enzyme found in various tissues throughout the body, with the highest concentrations in the liver, bones, kidneys, and bile ducts. It plays a role in breaking down proteins and is often measured to assess liver and bone health.\n\nThe optimal limit for Alkaline Phosphatase can vary based on the laboratory and the individual's age and sex, but generally, normal ranges are approximately:\n- For adults: 44 to 147 IU/L (international units per liter)\n\nSince your level is significantly higher at 437.0 IU/L, it suggests that there may be an underlying issue that needs further investigation.\n\nIf you have more questions related to your medical history, feel free to ask!"
        }
      ],
      "question": "What is Alkaline Phosphatase and what is the optimal limit ?"
   }
   ```
