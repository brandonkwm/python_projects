# main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React dev server origin
    allow_methods=["*"],                       # allow all HTTP methods
    allow_headers=["*"],                       # allow all headers
)
 
workflows = {}

class WorkflowNode(BaseModel):
    id: str
    type: str  # 'start', 'task', 'decision', 'end'
    params: Dict[str, Any]
    next_nodes: List[str]

class Workflow(BaseModel):
    id: str
    name: str
    nodes: List[WorkflowNode]

@app.post('/workflow')
def save_workflow(workflow: Workflow):
    workflows[workflow.id] = workflow
    return {'message': 'Workflow saved', 'workflow_id': workflow.id}

@app.get('/workflow/{workflow_id}')
def get_workflow(workflow_id: str):
    if workflow_id not in workflows:
        raise HTTPException(status_code=404, detail='Workflow not found')
    return workflows[workflow_id]

def evaluate_rule(node: WorkflowNode, context: Dict[str, Any]) -> bool:
    if node.type != 'decision':
        return True
    cond = node.params.get('condition')
    if cond:
        return context.get(cond, False)
    return True

def utility_based_next(node: WorkflowNode, context: Dict[str, Any], workflow) -> List:
    candidates = []
    max_utility = float('-inf')
    for next_id in node.next_nodes:
        next_node = next(n for n in workflow.nodes if n.id == next_id)
        utility = next_node.params.get('utility', 0)  
        if utility > max_utility:
            max_utility = utility
            candidates = [next_node]
        elif utility == max_utility:
            candidates.append(next_node)
    return candidates

@app.post('/execute/{workflow_id}')
def execute_workflow(workflow_id: str, context: Dict[str, Any]):
    if workflow_id not in workflows:
        raise HTTPException(status_code=404, detail='Workflow not found')

    workflow = workflows[workflow_id]
    current_nodes = [node for node in workflow.nodes if node.type == 'start']
    results = []

    while current_nodes:
        next_nodes = []
        for node in current_nodes:
            if node.type == 'end':
                results.append({'node': node.id, 'status': 'completed'})
                continue
            if node.type == 'decision':
                if evaluate_rule(node, context):
                    next_nodes.extend(utility_based_next(node, context, workflow))
            else:
                next_nodes.extend([n for n in workflow.nodes if n.id in node.next_nodes])
            results.append({'node': node.id, 'status': 'executed'})
        current_nodes = next_nodes

    return {'workflow_id': workflow_id, 'execution_result': results}
