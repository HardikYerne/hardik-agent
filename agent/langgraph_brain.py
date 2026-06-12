from langgraph.graph import StateGraph, END
from typing import TypedDict, Annotated
import operator
from agent.langchain_brain import process_command as lc_process

# define state
class AgentState(TypedDict):
    user_input: str
    plan: str
    result: str
    steps: Annotated[list, operator.add]
    is_complete: bool

# define nodes
def understand_node(state: AgentState) -> AgentState:
    print(f'Understanding: {state["user_input"]}')
    state['plan'] = state['user_input']
    state['steps'] = [f'Received: {state["user_input"]}']
    return state

def execute_node(state: AgentState) -> AgentState:
    print(f'Executing: {state["plan"]}')
    result = lc_process(state['plan'])
    state['result'] = result
    state['steps'] = [f'Executed: {result}']
    state['is_complete'] = True
    return state

def respond_node(state: AgentState) -> AgentState:
    print(f'Response: {state["result"]}')
    state['steps'] = [f'Done: {state["result"]}']
    return state

def should_continue(state: AgentState) -> str:
    if state.get('is_complete', False):
        return 'respond'
    return 'execute'

# build graph
workflow = StateGraph(AgentState)

workflow.add_node('understand', understand_node)
workflow.add_node('execute', execute_node)
workflow.add_node('respond', respond_node)

workflow.set_entry_point('understand')

workflow.add_conditional_edges(
    'understand',
    should_continue,
    {
        'execute': 'execute',
        'respond': 'respond'
    }
)

workflow.add_edge('execute', 'respond')
workflow.add_edge('respond', END)

graph = workflow.compile()

def process_command(user_input: str) -> str:
    try:
        initial_state = AgentState(
            user_input=user_input,
            plan='',
            result='',
            steps=[],
            is_complete=False
        )
        final_state = graph.invoke(initial_state)
        return final_state.get('result', 'Task completed.')
    except Exception as e:
        print(f'Graph error: {e}')
        from agent.langchain_brain import process_command as fallback
        return fallback(user_input)

