from langgraph.graph import StateGraph, END
from langchain_core.messages import HumanMessage, AIMessage 
from functools import partial
import graph_nodes
import tools

db_agent_executor = tools.create_db_agent_executor()
workflow = StateGraph(graph_nodes.GraphState)
database_agent_node_with_tool = partial(graph_nodes.database_agent_node, agent_executor=db_agent_executor)
workflow.add_node("router", graph_nodes.router_node)
workflow.add_node("database_agent", database_agent_node_with_tool)
workflow.add_node("general_chatbot", graph_nodes.general_chatbot_node)
workflow.set_entry_point("router")
workflow.add_conditional_edges(
    "router",
    graph_nodes.decide_next_node,
    {
        "database": "database_agent",
        "general_health_chatbot": "general_chatbot",
    }
)
workflow.add_edge("database_agent", END)
workflow.add_edge("general_chatbot", END)
app = workflow.compile()

if __name__ == "__main__":
    try:
        mermaid_code = app.get_graph().draw_mermaid()
        print("\n✅ İşte LangGraph Mimarinin GüncelKodu:\n")
        print("```mermaid")
        print(mermaid_code)
        print("```")
    except Exception as e:
        print(f"\nUyarı: Mermaid diyagramı oluşturulamadı. Hata: {e}")

    print("\n✅ LangGraph Hafızalı Sağlık Asistanı Başlatıldı.")
    print("---")
    print("   Sorularınızı yazıp Enter'a basın.")
    print("   Çıkmak için 'exit', 'quit' veya 'çık' yazabilirsiniz.")

    # Konuşma geçmişini (hafızayı) tutacak olan liste
    conversation_history = []

    while True:
        try:
            user_input = input("\n> ")

            if user_input.strip().lower() in ["exit", "quit", "çık", "kapat"]:
                print("\nGörüşmek üzere!")
                break
            if not user_input.strip():
                continue

            # 1. Kullanıcı mesajını geçmişe ekle
            conversation_history.append(HumanMessage(content=user_input))

            print(" Düşünülüyor...")
            
            # 2. Grafiği tüm konuşma geçmişiyle
            inputs = {"messages": conversation_history}
            final_state = None
            for output in app.stream(inputs, stream_mode="values"):
                final_state = output
            
            print("\n✅ Sonuç:")
            if final_state and "messages" in final_state and final_state["messages"]:
                ai_response_message = final_state["messages"][-1]
                print(ai_response_message.content)
                conversation_history.append(ai_response_message)
            else:
                print("Bir sonuç üretilemedi.")
            print("-------------------------------------")

        except (KeyboardInterrupt, EOFError):
            print("\n\nÇıkış yapılıyor... Görüşmek üzere!")
            break