from datetime import timedelta
from flask import Flask, abort, request
from tempfile import NamedTemporaryFile
import whisper
import torch

# Checking if NVIDIA GPU is available
torch.cuda.is_available()
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load the Whisper model:
model = whisper.load_model("base", device=DEVICE)

app = Flask(__name__)


@app.route("/")
def hello():
    return "Whisper Hello World!"


@app.route("/whisper", methods=["POST"])
def handler():
    if not request.files:

        abort(400)

    results = []
    timestamp = []

    for filename, handle in request.files.items():

        temp = NamedTemporaryFile()

        handle.save(temp)

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
                "filename": filename,
                "transcript": result["text"],
                "segments": segments,
                "timestamp": timestamp,
            }
        )
        print(results)

    return {"results": results}
