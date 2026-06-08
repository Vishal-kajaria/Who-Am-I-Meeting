import os
from who_am_I_meeting.ui import app

if __name__ == "__main__":
    
    server_name = os.getenv("SERVER_NAME", "127.0.0.1") 
    server_port = int(os.getenv("SERVER_PORT", "7860"))
    
    app.launch(
        server_name=server_name,
        server_port=server_port
    )