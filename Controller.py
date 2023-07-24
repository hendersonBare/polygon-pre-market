import DatabaseRequests
from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates


app = FastAPI()

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def main(request: Request):
    context = {'request': request}
    return templates.TemplateResponse("main.html", context)

@app.get("/date/{datevalue}", response_class=HTMLResponse)
async def date(datevalue: str, request: Request):
    data = DatabaseRequests.requestDate(datevalue)
    context = {'request': request, 'data': data, "dateValue": datevalue} 
    return templates.TemplateResponse("date.html", context)
    