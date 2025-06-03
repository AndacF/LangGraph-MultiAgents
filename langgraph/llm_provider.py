from langchain_openai import ChatOpenAI

def get_llm():
    return ChatOpenAI(
        base_url="http://127.0.0.1:1234/v1",
        api_key="lm-studio", 
        temperature=0.7,
        model="gemma-3-4b-it-qat"  
    )