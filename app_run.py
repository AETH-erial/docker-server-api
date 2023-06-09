from dotenv import load_dotenv
import uvicorn


load_dotenv()
if __name__ == '__main__':
    uvicorn.run('docker_server_api:web_app', reload=True,
                host='0.0.0.0', port=8080)
