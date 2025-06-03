from typing import List
from typing_extensions import TypedDict
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
from llm_provider import get_llm
import config

class GraphState(TypedDict):
    messages: List[BaseMessage]
    next_node: str

def router_node(state: GraphState) -> dict:
    """
    Gelen mesaja göre karar verir. Bu versiyon, LLM'in yapısal çıktı (structured output)
    ile ilgili sorunlarını aşmak için basit metin çıktısı kullanır.
    """
    llm = get_llm()
    
    prompt = f"""
    Sen bir metin sınıflandırma uzmanısın. Kullanıcının sorusunu analiz et ve aşağıdaki iki kategoriden hangisine ait olduğuna karar ver.
    Cevabın SADECE ve SADECE 'database' veya 'general_health_chatbot' kelimelerinden biri olmalıdır. Başka hiçbir şey yazma.

    Kategoriler:
    - 'database': Eğer soru, hasta kayıtları, laboratuvar sonuçları gibi veritabanında bulunabilecek spesifik bilgiler içeriyorsa.
    - 'general_health_chatbot': Eğer soru, genel sağlık bilgisi, hastalık tanımları, "merhaba", "nasılsın" gibi genel sohbet konuları içeriyorsa.

    Kullanıcı sorusu: '{state["messages"][-1].content}'
    """
    
    response = llm.invoke(prompt)
    decision = response.content.strip().lower().replace("'", "").replace('"', '')
    
    print(f"--- Yönlendirici Kararı: {decision} ---")

    if "database" in decision:
        return {"next_node": "database"}
    else:
        return {"next_node": "general_health_chatbot"}


def decide_next_node(state: GraphState) -> str:
    return state["next_node"]


def database_agent_node(state: GraphState, agent_executor) -> dict:
    print("--- Veritabanı Ajanı Çalışıyor (Hafızalı) ---")
    query = state["messages"][-1].content
    history = state["messages"][:-1]
    
    response = agent_executor.invoke({"input": query, "chat_history": history})
    
    return {"messages": [AIMessage(content=response["output"])]}


def general_chatbot_node(state: GraphState) -> dict:
    print("--- Genel Sağlık Chatbot'u Çalışıyor (Hafızalı) ---")
    llm = get_llm()
    
    messages_for_llm = [
        SystemMessage(content="Sen, AKAI isimli yardımsever bir sağlık asistanısın. Kullanıcının sorularını, önceki konuşmayı da dikkate alarak samimi bir dille cevapla.")
    ]
    messages_for_llm.extend(state["messages"])
    
    response = llm.invoke(messages_for_llm)
    
    return {"messages": [AIMessage(content=response.content)]}