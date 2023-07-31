import DatabaseRequests
data = DatabaseRequests.requestTable('table_AVTX_2023-06-27')

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

@app.get("/table/{tableName}", response_class=HTMLResponse)
async def table(tableName: str, request: Request):
    data = DatabaseRequests.requestTable(tableName)
    context = {'request': request, 'data': data}
    return templates.TemplateResponse("tableData.html", context)