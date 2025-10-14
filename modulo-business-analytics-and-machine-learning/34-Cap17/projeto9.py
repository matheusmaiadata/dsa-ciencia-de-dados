# Projeto 9 - Chatbot Personalizado com Sistema de Recomendação Para Suporte ao Cliente Usando LLMs

# Imports
import docx2txt  # Biblioteca para extrair texto de arquivos .docx
import streamlit as st  # Biblioteca para criar aplicações web interativas
#from langchain_huggingface import HuggingFaceEmbeddings  
from llama_index.embeddings.huggingface import HuggingFaceEmbedding # Importa modelo de embeddings do Hugging Face
from llama_index.llms.ollama import Ollama  # Importa o Ollama
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader, Settings  # Importa componentes do Llama Index para construir o banco de dados vetorial

# Evita problema de compatibilidade entre Streamlit e PyTorch
import torch
torch.classes.__path__ = []

# Configurando o título da página e outras configurações (favicon)
st.set_page_config(page_title="DSA Projeto 9", page_icon=":100:", layout="centered")

# Cria um menu lateral com informações do projeto e botão do mantenedor
st.sidebar.title("DSA - Projeto 9")
st.sidebar.markdown("### Business Analytics e Machine Learning Para Projetos de Data Science")
st.sidebar.markdown("[Data Science Academy](https://www.datascienceacademy.com.br)")
st.sidebar.button("AI Chatbot Versão 1.0")

# Define o título da aplicação
st.title("Chatbot Personalizado com Sistema de Recomendação Para Suporte ao Cliente Usando LLMs")

# Inicializa a sessão de mensagens se não existir
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Digite sua pergunta"}]

# Define o LLM (Large Language Model)
llm = Ollama(model="gemma3:270m", timeout = 300)

# Define o modelo de embeddings
embed_model = HuggingFaceEmbedding(model_name="sentence-transformers/all-MiniLM-L6-v2")

# Módulo de Criação do Banco de Dados Externo
@st.cache_resource()
def dsa_cria_database_externo():
    with st.spinner(text="Carregando e indexando os documentos. Isso deve levar alguns segundos."):
        reader = SimpleDirectoryReader(input_dir="./suporte", recursive=True)
        docs = reader.load_data()
        Settings.llm = llm
        Settings.embed_model = embed_model
        index = VectorStoreIndex.from_documents(docs)
        return index

# Carrega o índice de dados
banco_vetorial = dsa_cria_database_externo()

# Construindo o Motor de Execução da App 
if "chat_engine" not in st.session_state:
    st.session_state.chat_engine = banco_vetorial.as_chat_engine(chat_mode="condense_question", verbose=True)

# Verifica se há uma entrada de chat do usuário
if prompt := st.chat_input("Sua pergunta"):
    st.session_state.messages.append({"role": "user", "content": prompt})

# Exibe as mensagens na interface de chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Se a última mensagem não for do assistente, gera uma resposta
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Pensando..."):
            user_message = st.session_state.messages[-1]["content"]
            contextual_prompt = f"Você é um atendente de suporte especializado. O usuário fez a seguinte pergunta: '{user_message}'. Considere todos os documentos com perguntas e respostas disponíveis e forneça uma resposta detalhada e precisa, fazendo recomendações quando isso for pertinente. Seja pró-ativo."
            response = st.session_state.chat_engine.chat(contextual_prompt)
            st.write(response.response)
            st.session_state.messages.append({"role": "assistant", "content": response.response})




# Exemplos para testar o Chatbot:

# Desejo comprar um produto. A empresa oferece frete grátis?
# Como posso entrar em contato com o atendimento ao cliente?
# A empresa oferece programa de fidelidade? Como faço para me cadastrar?
# Posso reservar um produto online e retirar na loja?
# Muito obrigado. Você é um Chatbot muito inteligente e a Data Science Academy sempre surpreende com cursos e projetos incríveis.


