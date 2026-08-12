from datetime import datetime, timezone
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
from prometheus_client import Counter, Histogram, generate_latest, CONTENT_TYPE_LATEST
from starlette.responses import Response

MONGO_URL=os.getenv('MONGO_URL','mongodb://127.0.0.1:27017')
DB_NAME=os.getenv('MONGO_DB','error_analyzer')
client=MongoClient(MONGO_URL,serverSelectionTimeoutMS=3000)
db=client[DB_NAME]
collection=db['analysis_history']
app=FastAPI(title='Intelligent Error Analyzer API',version='1.0.0')
app.add_middleware(CORSMiddleware,allow_origins=['http://localhost:5173','http://127.0.0.1:5173'],allow_credentials=True,allow_methods=['*'],allow_headers=['*'])
REQ=Counter('error_analyzer_requests_total','API requests',['endpoint','method','status'])
AN=Counter('error_analyzer_analyses_total','Analyses',['result'])
LAT=Histogram('error_analyzer_analysis_latency_seconds','Analysis latency')
class CodeRequest(BaseModel): code:str
@app.get('/')
def home(): return {'message':'Intelligent Error Analyzer API is Running'}
@app.get('/health')
def health():
    try: client.admin.command('ping'); return {'status':'UP','mongodb':'UP'}
    except Exception as e: raise HTTPException(503,detail=str(e))
@app.get('/ready')
def ready():
    try: client.admin.command('ping'); return {'ready':True}
    except Exception: raise HTTPException(503,detail='MongoDB unavailable')
@app.post('/analyze')
def analyze(req:CodeRequest):
    with LAT.time():
        try:
            compile(req.code,'<string>','exec')
            result={'error':'No Syntax Error','suggestion':'Your Python code is syntactically correct.','line':None,'received_code':req.code,'timestamp':datetime.now(timezone.utc)}
            AN.labels('success').inc()
        except SyntaxError as e:
            suggestions={"'(' was never closed":"You forgot to close a parenthesis ')'.","'[' was never closed":"You forgot to close a square bracket ']'.","'{' was never closed":"You forgot to close a curly bracket '}'.","expected ':'":"A colon (:) is missing after a statement like if, for, while, or def.","invalid syntax":"Check the syntax near the highlighted line.","unexpected EOF while parsing":"Your code ended unexpectedly. Check for missing brackets or quotes.","unterminated string literal":"Check that all strings have matching quotes."}
            result={'error':f'SyntaxError: {e.msg}','suggestion':suggestions.get(e.msg,'Please review the syntax on the indicated line.'),'line':e.lineno,'received_code':req.code,'timestamp':datetime.now(timezone.utc)}
            AN.labels('syntax_error').inc()
        except Exception as e:
            result={'error':str(e),'suggestion':'Unexpected error occurred.','line':None,'received_code':req.code,'timestamp':datetime.now(timezone.utc)}
            AN.labels('runtime_error').inc()
        try: collection.insert_one(result.copy())
        except Exception as e: raise HTTPException(503,detail=f'MongoDB write failed: {e}')
        REQ.labels('/analyze','POST','200').inc(); result['timestamp']=result['timestamp'].isoformat(); return result
@app.get('/history')
def history():
    try:
        records=list(collection.find({},{'_id':0}).sort('timestamp',-1).limit(100))
        for r in records:
            if isinstance(r.get('timestamp'),datetime): r['timestamp']=r['timestamp'].isoformat()
        return records
    except Exception as e: raise HTTPException(503,detail=f'MongoDB read failed: {e}')
@app.get('/metrics')
def metrics(): return Response(generate_latest(),media_type=CONTENT_TYPE_LATEST)
