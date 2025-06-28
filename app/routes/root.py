from fastapi import APIRouter
from fastapi.responses import HTMLResponse

root_router = APIRouter()

@root_router.get("/", response_class=HTMLResponse)
async def read_root():
    html_content = """
    <!DOCTYPE html>
    <html>
        <head>
            <title>Welcome to Voice Transcriber Service</title>
            <style>
                /* Full viewport body */
                body {
                    margin: 0;
                    width: 100vw;
                    height: 100vh;
                    font-family: Arial, sans-serif;
                    background: #f5f5f5;
                    display: flex;
                    justify-content: center;
                    align-items: flex-start;
                    padding: 2rem 0;
                }

                /* Centered wrapper */
                .wrapper {
                    width: 90%;
                    background: white;
                    border-radius: 8px;
                    box-shadow: 0 8px 16px rgba(0,0,0,0.1);
                    padding: 2rem;
                    box-sizing: border-box;
                }

                h1 {
                    color: #2c3e50;
                    margin-top: 0;
                }

                .preview {
                    margin-top: 20px;
                }

                img, video {
                    max-width: 100%;
                    border-radius: 8px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                }

                video {
                    margin-top: 20px;
                }

                .button-container {
                    margin-top: 12px;
                    margin-bottom: 30px;
                    text-align: center;
                    width: 100%;
                }

                button {
                    background-color: #2c3e50;
                    color: white;
                    border: none;
                    padding: 12px 24px;
                    font-size: 16px;
                    border-radius: 6px;
                    cursor: pointer;
                    transition: background-color 0.3s ease;
                    width: 100%;
                }

                button:hover {
                    background-color: #1a2733;
                }

                .response-example {
                    background-color: #272822;
                    color: #f8f8f2;
                    padding: 1rem;
                    border-radius: 8px;
                    margin-top: 30px;
                    max-width: 600px;
                    overflow-x: auto;
                    font-family: 'Courier New', Courier, monospace;
                    font-size: 14px;
                    line-height: 1.5;
                    width: 100%;
                }

                .response-example h2 {
                    color: #66d9ef;
                    margin-top: 0;
                    margin-bottom: 10px;
                    font-weight: 600;
                    width: 100%;
                }

            </style>
        </head>
        <body>
            <div class="wrapper">
                <h1>Welcome to Voice Transcriber Service</h1>
                <p>Here is a preview of the project:</p>

                <div class="preview">
                    <img src="/static/previews/documentation.png" alt="Documentation Screenshot" title="Project Documentation Preview" />
                </div>

                <div class="button-container">
                    <button onclick="window.location.href='/docs'">Go to API Docs</button>
                </div>

                <div class="preview">
                    <img src="/static/previews/messages.png" alt="Messages Screenshot" title="Messages Preview" />
                </div>
                <div class="preview">
                    <h2>API Response Structure Example</h2>
                    <pre>
                        {
                            "status": 200,
                            "success": true,
                            "message": "Transcriber pipeline succeeded.",
                            "data": {
                                "messages": [
                                  {
                                    "sender": "robot",
                                    "duration": 5.0,
                                    "text": "Hello."
                                  },
                                  {
                                    "sender": "user",
                                    "duration": 5.0,
                                    "text": "How are you?"
                                 }
                               ],
                               "performance": {
                                  "duration_ms": 1234,
                                  "message_count": 2,
                                  "total_text_length": 23,
                                  "input_url_size_bytes": 56789
                                }
                            }
                        }
                    </pre>
                </div>
                <div class="preview">
                    <video controls title="Project Process Video">
                        <source src="/static/previews/process.webm" type="video/mp4" />
                        Your browser does not support the video tag.
                    </video>
                </div>
            </div>
        </body>
    </html>
    """
    return HTMLResponse(content=html_content)
