import whisper
model = whisper.load_model("medium")
result = model.transcribe("310774525446848514.wav")
print(f' The text in video: \n {result["text"]}')