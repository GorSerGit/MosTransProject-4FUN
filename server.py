from fastapi import FastAPI, Request, Form, File, UploadFile, Query
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pathlib import Path
from fastapi.responses import FileResponse, PlainTextResponse,JSONResponse
from fastapi import encoders



import libs.maplib as mp
app = FastAPI()
#app.mount("/static", StaticFiles(directory=Path(__file__).parent.absolute() / "templates/static"), name="static")
templates = Jinja2Templates(directory = 'templates')



@app.get("/")
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/analyse", response_class=JSONResponse)
def analyse(requesr: Request, 
          latitude: str = "",
          longtitude: str = "",
          livable: str = "",
          workable: str = "",
          percent_25: str = "",
          percent_45: str = ""):
    print(100500)
    print((latitude, longtitude, percent_25, percent_45, livable, workable))
    data = mp.analyse(float(latitude), float(longtitude), float(percent_25), float(percent_45), float(livable), float(workable))
    json_compatible_stations = encoders.jsonable_encoder(data)
    print(json_compatible_stations)
    return data

if __name__ == '__main__':
    import uvicorn
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default = 'localhost')
    parser.add_argument('--port', default = 8000)
    opt = parser.parse_args()
        
    app_str = f'{Path(__file__).stem}:app' #make the app string equal to whatever the name of this file is
    uvicorn.run(app_str, host= opt.host, port=opt.port, reload=True)
