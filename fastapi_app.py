from datetime import timedelta
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, RedirectResponse
from tempfile import NamedTemporaryFile
import whisper
import torch
from typing import List

# Checking if NVIDIA GPU is available
torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"


model = whisper.load_model("base", device=DEVICE)

app = FastAPI()


@app.post("/whisper/")
async def handler(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files were provided")

    results = []
    timestamp = []

    for file in files:
        with NamedTemporaryFile(delete=True) as temp:
            with open(temp.name, "wb") as temp_file:
                temp_file.write(file.file.read())

            result = model.transcribe(temp.name)

        segments = result["segments"]

        for segment in segments:
            startTime = str(0) + str(timedelta(seconds=int(segment["start"]))) + ",000"
            endTime = str(0) + str(timedelta(seconds=int(segment["end"]))) + ",000"
            text = segment["text"]
            segmentId = segment["id"] + 1
            segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] is ' ' else text}\n\n"
            timestamp.append(
                {
                    "startTime": startTime,
                    "endTime": endTime,
                    "text": text,
                    "segmentId": segmentId,
                    "segment": segment,
                }
            )

        results.append(
            {
                "filename": file.filename,
                "transcript": result["text"],
                "segments": segments,
                "timestamp": timestamp,
            }
        )
        print(results)

    return JSONResponse(content={"results": results})


@app.get("/", response_class=RedirectResponse)
async def redirect_to_docs():
    return "/docs"
