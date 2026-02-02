from app.routes.rag_routes import router as rag_router
from fastapi import FastAPI
import gradio as gr
from app.gradio_ui.gradio_app import demo
from app.database import engine, Base

app = FastAPI(title="RAG Assistant API")

app.include_router(rag_router)

# create database tables
Base.metadata.create_all(bind=engine)  

#Define routes
@app.get("/")
def root():
    return {"status": "API is running"}

# Mount Gradio app
app = gr.mount_gradio_app(app, demo, path="/ui")

