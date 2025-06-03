from langchain_community.agent_toolkits import create_sql_agent
from langchain_community.utilities import SQLDatabase
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from llm_provider import get_llm
import config

def create_db_agent_executor():
    """Veritabanına bağlanır ve sorgulama yapabilen bir SQL Agent Executor oluşturur."""
    db_uri = f"postgresql+psycopg2://{config.DB_USER}:{config.DB_PASSWORD}@{config.DB_HOST}:{config.DB_PORT}/{config.DB_DATABASE}"
    db = SQLDatabase.from_uri(db_uri)
    
    llm = get_llm()

    SYSTEM_PROMPT = """
    Sen, PostgreSQL veritabanıyla etkileşim kuran bir AI asistanısın.
    Sana verilen kullanıcı sorusunu temel alarak, anlamsal olarak doğru SQL sorguları oluşturmalısın.
    Cevabı konuşma geçmişinden bildiğini düşünsen bile, bilgiyi doğrulamak ve en güncel veriyi almak için **HER ZAMAN** yeni bir SQL sorgusu çalıştırmak zorundasın. Asla hafızadan cevap verme.

    ÇOK ÖNEMLİ KURALLAR:
    1.  Veritabanında `hastaid` ve `hastalab` adında iki tablo bulunmaktadır.
    2.  Sorgularında **SADECE** bu tablo adlarını kullanmalısın. "hasta" gibi başka bir tablo adı **ASLA** kullanma.
    3.  `hastaid` tablosu, yaş ve kan grubu gibi demografik hasta bilgilerini içerir. Kullanıcı "hasta bilgisi" sorduğunda bu tabloyu kullan.
    4.  `hastalab` tablosu, laboratuvar sonuçlarını içerir.
    5.  Sorgu oluşturmadan önce aşağıda verilen tablo şemasını dikkatlice incele ve sadece var olan kolonları kullan.
    6.  Son cevabın **SADECE** veritabanından dönen sonuca dayanmalıdır. Bilgileri değiştirme, kendi kendine bilgi uydurma veya ekleme yapma.

    Kullanabileceğin tablolar ve şemaları aşağıdadır:
    {table_info}
    """
    
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", SYSTEM_PROMPT),
            MessagesPlaceholder(variable_name="chat_history"),
            ("human", "{input}"),
            MessagesPlaceholder(variable_name="agent_scratchpad"),
        ]
    ).partial(table_info=config.FULL_SCHEMA_PROMPT)

    agent_executor = create_sql_agent(
        llm=llm,
        db=db,
        agent_type="openai-tools",
        prompt=prompt,
        verbose=True
    )
    
    return agent_executor