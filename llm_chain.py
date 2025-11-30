

from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM
from dotenv import load_dotenv
import os

load_dotenv()

def get_llm(provider="local"):
    if provider == "local":
        return OllamaLLM(model="llama3.2:1b")
    else:
        raise ValueError("Unsupported provider: choose 'local'.")

def run_llm(prompt: str, provider="local"):
    template = PromptTemplate.from_template("Answer the following:\n{question}")
    llm = get_llm(provider)
    chain = template | llm
    return chain.invoke({"question": prompt})

def stream_llm(prompt: str, provider="local"):
    template = PromptTemplate.from_template("Answer the following:\n{question}")
    llm = get_llm(provider)
    chain = template | llm
    for chunk in chain.stream({"question": prompt}):
        yield chunk