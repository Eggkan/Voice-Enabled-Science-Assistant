import os
from langchain_community.document_loaders import TextLoader
from langchain_community.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.prompts import ChatPromptTemplate
from langchain_community.chat_models import ChatOpenAI

# Dosya yolunu kontrol etme
DOC_PATH = "data.txt"
if not os.path.exists(DOC_PATH):
    raise FileNotFoundError(f"{DOC_PATH} dosyası bulunamadı. Lütfen dosya yolunu kontrol edin.")

# Veriyi yükleme
loader = TextLoader(DOC_PATH)
pages = loader.load()

# Metni parçalara ayırma
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = text_splitter.split_documents(pages)

# Gömme modelini yükleme
embeddings = HuggingFaceEmbeddings(model_name="dbmdz/bert-base-turkish-cased")

# Chroma veritabanını oluşturma
CHROMA_PATH = "veritabanı"
db_chroma = Chroma.from_documents(chunks, embeddings, persist_directory=CHROMA_PATH)

# Alım mekanizmasını tanımlama
def retrieve_context(query):
    docs_chroma = db_chroma.similarity_search_with_score(query, k=5)
    context_text = "\n\n".join([doc.page_content for doc, _score in docs_chroma])
    return context_text

# Yanıt üretme
def generate_response(query):
    context_text = retrieve_context(query)

    PROMPT_TEMPLATE = """Aşağıdaki bağlama dayanarak soruyu yanıtlayın: {context} 
    Yukarıdaki bağlama dayanarak soruyu yanıtlayın: {question}. Detaylı bir yanıt verin."""

    prompt_template = ChatPromptTemplate.from_template(PROMPT_TEMPLATE)
    prompt = prompt_template.format(context=context_text, question=query)

    model = ChatOpenAI()  # Yerel bir model veya alternatif kullanabilirsiniz
    response_text = model.predict(prompt)
    return response_text

# Örnek bir sorgu
query = "Belgede hangi konular var?"
response = generate_response(query)
print(response)