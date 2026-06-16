from agent.state import AgentState, StateUpdate, IntentResult  # new code
from prompts import load_prompt  # new code
from utils.llm_client import LLMClient  # new code
from utils.logger import get_logger  # new code

logger = get_logger(__name__)  # new code

INTENT_PROMPT = load_prompt("intent_recognition")  # new code
client = LLMClient(task="intent")  # new code

def recognize_intent(state: AgentState) -> StateUpdate:  # new codeW
    result = client.structured(
        INTENT_PROMPT,
        { "question" : state["question"] },
        IntentResult
    )
    logger.info("LMM ask for intent recognition sent")

    return {"intent": result}

async def arecognize_intent(state: AgentState) -> StateUpdate:  # new code
    """Async variant of recognize_intent."""  # new code
    result = await client.astructured(INTENT_PROMPT, {"question": state["question"]}, IntentResult)  # new code
    logger.info(f"Intent='{result.intent}' reason='{result.reason}'")  # new code
    return {"intent": result}  # new code


