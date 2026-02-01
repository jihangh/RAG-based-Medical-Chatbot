from app.routes.rag_routes import router as rag_router
from fastapi import FastAPI
import gradio as gr
from app.gradio_ui.gradio_app import demo

app = FastAPI(title="RAG Assistant API")

app.include_router(rag_router)

#Define routes
@app.get("/")
def root():
    return {"status": "API is running"}

# Mount Gradio app
app = gr.mount_gradio_app(app, demo, path="/ui")

