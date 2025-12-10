from fastapi import FastAPI, File, UploadFile
from transformers import pipeline
import tempfile
import shutil

app = FastAPI()


pipe = pipeline(
    task="automatic-speech-recognition",
    model="openai/whisper-tiny",
    return_timestamps=True,
    chunk_length_s=30,  # recommandé
)

@app.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    # Sauvegarder temporairement le fichier
    temp = tempfile.NamedTemporaryFile(delete=False, suffix=file.filename)
    with open(temp.name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    # Transcription avec timestamps
    result = pipe(temp.name)

    return {
        "text": result.get("text", ""),
        "chunks": result.get("chunks", []),  # timestamps + texte
    }

# # result = pipe("input.mp4")
# # print(result["chunks"])

# curl -X POST "https://torikhu-whisper.hf.space/transcribe/" -F "file=@input.mp4"


# curl -X POST "https://jimmy573-transcript-audio.hf.space/transcrire/" -F "file=@input.mp4"