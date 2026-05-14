# https://fastapi.tiangolo.com/tutorial/first-steps/
# https://medium.com/@marcnealer/a-practical-guide-to-using-pydantic-8aafa7feebf6

# n8n بتبعت Request فيه:
#   - المهمة (task)
#   - شكل الخرج (Output Format)

# FastAPI بترد بـ:
#   - النتيجة (result)

# 1. Method  → POST
# 2. Endpoint → /n8n_request  
# 3. Request Body →
#    - task: str
#    - output_format: str

# {
#   "task": "اعمل تقرير عن أسهم شركة X",
#   "output_format": "report"
# }

from pydantic import BaseModel
from fastapi import FastAPI
from .graph import workflow_app

class RequestBody(BaseModel):
    task: str
    output_format: str

app = FastAPI()
langgraph_app = workflow_app

@app.post("/n8n_request")
async def n8n_request(body: RequestBody):
    result = langgraph_app.invoke({
                "task": body.task,
                "output_format": body.output_format,
                "agent": "",
                "crew_result": ""
            
        })
    return {
        'status': 'received',
        'task': body.task,
        'output_format': body.output_format,
        'result': result['crew_result'].raw
            }

# لأن دول هيتملوا أثناء تنفيذ الـ Graph:
# "agent": ""       # router_node هيملاه
# "crew_result": "" # crewai_node هيملاه
