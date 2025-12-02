from fastapi import FastAPI, Depends, Query
from pydantic import BaseModel, validator, root_validator
from fastapi.exceptions import RequestValidationError
from datetime import datetime
from llama_cpp import Llama, CreateCompletionResponse
from typing_extensions import Optional, List, Literal, Any, Union, Iterator
from functools import lru_cache


CONTEXT_SIZE = 512



class LLMPrompt(BaseModel):
    message: str = Query("message")

    @validator('message')
    def check_token_count(cls, v: str) -> str:
        token_count = len(llm.tokenize(v.encode('utf-8')))
        if token_count > CONTEXT_SIZE:
            raise RequestValidationError(
            f'Token count exceeds the maximum allowed limit of {CONTEXT_SIZE}.'
            )
        return v

class Choice(BaseModel):
    text: str = "Beep boop"
    index: int = 0
    logprobs: Optional[str] = "null"
    finish_reason: str = "stop"



class Usage(BaseModel):
    prompt_tokens: int = 198
    completion_tokens: int = 10
    total_tokens: int = 208

class BaseLlamaResponse(BaseModel):
    id: str = "cmpl-7fc1be4c-8f5b-4b2f-805f-f8c5086a9fb4"
    object: str = "text_completion"
    created: int = 1708459650
    model: str = "tinyllama-1.1b-chat-v1.0.Q2_K.gguf"
    choices: List[Choice]
    usage: Usage

@lru_cache(maxsize=None)
def get_llm_response_refactored(llm, template, memory_buffer):
    return llm(template, temperature=0.0, max_tokens=128)


async def get_llm_response(message : LLMPrompt, llm : Llama) -> Union[CreateCompletionResponse, Iterator[CreateCompletionResponse]]:
    system_message = "You are a helpful assistant."
    prompt = message
    template = f"""<|system|>
    {system_message}</s>
    <|user|>
    {prompt}</s>
    <|assistant|>"""
    new_mem_buffer = ' ' * 512000
    return get_llm_response_refactored(llm, template, new_mem_buffer)



app = FastAPI()
llm = None
@app.on_event("startup")
async def load_model():
    global llm
    print("Loading tinyllama model...")
    llm = Llama(
        model_path="tinyllama-1.1b-chat-v1.0.Q2_K.gguf",
        n_ctx=CONTEXT_SIZE,
        n_batch=1
    )

@app.get('/api', response_model=BaseLlamaResponse)
async def send_llm_response(message: LLMPrompt = Depends(LLMPrompt)) -> Union[CreateCompletionResponse, Iterator[CreateCompletionResponse]]:
    model_output = await get_llm_response(message, llm)
    return model_output


@app.get('/healthcheck')
def healthcheck() -> Literal["OK"]:
    return "OK"

