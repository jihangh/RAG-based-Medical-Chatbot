import requests
from typing import List, Tuple
import gradio as gr


# API base URL - adjust based on your setup
API_BASE_URL = "http://localhost:8000"


def chat_with_rag(message: str, history= None) -> str:
    """
    Send message to RAG API and get response.
    
    Args:
        message: User message
        history: Chat history
       
        
    Returns:
        string of (response)
    """
    try:
        response = requests.post(
            f"{API_BASE_URL}/rag/chat",
            json={
                "message": message
                
            },
            timeout=30
        )
        response.raise_for_status()
        data = response.json()
        return data.get("answer", "No response")
    except requests.exceptions.Timeout:
        return "Request timed out. Please try again."
    except requests.exceptions.ConnectionError:
        return "Cannot connect to API. Please ensure the server is running."
    except requests.exceptions.HTTPError as e:
        error_detail = "Unknown error"
        try:
            error_detail = response.json().get("detail", str(e))
        except:
            pass
        return f"Error: {error_detail}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
    


#gradio chat interface

demo = gr.ChatInterface(
    fn=chat_with_rag,  
    title="Medical Chatbot with RAG",
    description="Ask your medical questions")