import uvicorn
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

APP_TITLE: str = "MY_APP"
APP_PORT: int = 8080
APP_HOST: str = '0.0.0.0'

def run_job_func():
    now_dt = datetime.now()
    print(f"job run at '{now_dt}'")

class AppRun:
    def __init__(self):
        self.fastapp=FastAPI(title=APP_TITLE)
        self.__scheduler=AsyncIOScheduler(timezone='Europe/Paris')
        self.__config_app()

    def __add_middlewares(self):
        self.fastapp.add_middleware(
                        CORSMiddleware,
                        allow_origins=["*"],
                        allow_credentials=True,
                        allow_methods=["*"],
                        allow_headers=["*"],
        )
    
    def __set_app_routes_events(self):
        # start scheduler befor starting application
        self.fastapp.add_event_handler('startup', lambda: self.__scheduler.start())

        # stop scheduler after stoping application
        self.fastapp.add_event_handler('shutdown', lambda: self.__scheduler.shutdown())

        @self.fastapp.get("/")
        async def index():
            html_content = """<html>
                                    <head><title>TEST APP</title></head>
                                    <body>
                                            <h1>HELLO APP</h1>
                                    </body>
                            
                            
            </html>"""
            return HTMLResponse(content=html_content, status_code=200)
        
        
    
        
    
    def __setup_scheduler(self):
        # run run_job_func() evry one minute
        self.__scheduler.add_job(
                                    func=run_job_func, 
                                    id="1", 
                                    name="RUN_JOB_CRON", 
                                    trigger="cron", 
                                    day="*",  
                                    minute="*/1"
        )

    
    def __config_app(self):
        self.__add_middlewares()
        self.__set_app_routes_events()
        self.__setup_scheduler()

if __name__ == "__main__":
    appRunInstance = AppRun()
    uvicorn.run(
                    appRunInstance.fastapp, 
                    port=APP_PORT, 
                    host=APP_HOST
    )
   
