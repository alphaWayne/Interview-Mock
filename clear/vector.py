import os,dashscope,chromadb,warnings,uuid
warnings.filterwarnings("ignore")
from langchain_community.document_loaders import TextLoader,PyPDFium2Loader,CSVLoader,SeleniumURLLoader,UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_community.vectorstores import Chroma
from dotenv import load_dotenv,find_dotenv
_=load_dotenv(find_dotenv())
dashscope.api_key = os.getenv("DASHSCOPE_API_KEY")

embedding_model_list={
    "qianwen_embedding_v1":DashScopeEmbeddings(model="text-embedding-v1", dashscope_api_key="sk-610f5dd948db4848a52e5e4a2bd58b98"),
    "qianwen_embedding_v2":DashScopeEmbeddings(model="text-embedding-v2", dashscope_api_key="sk-610f5dd948db4848a52e5e4a2bd58b98"),
    "qianwen_embedding_v3":DashScopeEmbeddings(model="text-embedding-v3", dashscope_api_key="sk-610f5dd948db4848a52e5e4a2bd58b98"),
}

#加载文件并分割文档
def load_file_split(file_path):
    '''
    :param file_path: 文件路径
    '''
    if file_path.endswith(".pdf"):
        loader=PyPDFium2Loader(file_path=file_path)
    elif file_path.endswith(".csv"):
        loader=CSVLoader(file_path=file_path)
    elif file_path.endswith(".docx"):
        loader=UnstructuredWordDocumentLoader(file_path=file_path)
    elif file_path.startswith("http"):
        loader=SeleniumURLLoader(url=file_path)
    elif file_path.endswith(".txt"):
        loader=TextLoader(file_path=file_path)
    else:
        print("文件格式不支持")
    data=loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=32)
    split_docs = text_splitter.split_documents(data)
    return split_docs


#使用高质量的方法将文档保存到ChromaDB
def save_to_chromaDB_high_Quantity(file_path,):
    '''
    :param file_path: 文件路径
    :param embedding_func: embedding模型
    :param collection_name: collection名称
    :param persist_directory: chromadb保存路径
    '''
    split_docs=load_file_split(file_path=file_path)
    save_collection = chromadb.PersistentClient(path=persist_directory).get_or_create_collection(name=collection_name)
    for item in split_docs:
        embeddings_Result = embedding_func.embed_query(item.page_content)
        save_collection.add(
        documents=item.page_content,  # 分割后的文档对象列表
        embeddings=embeddings_Result,  # 嵌入向量列表
        ids=str(uuid.uuid4()),  # 每个文档的唯一ID
        metadatas=item.metadata # 每个文档的元数据
        )

file_path=os.path.join(os.getcwd(),"storage/user/巩金玮简历.pdf")

# vector_store = Chroma(
#     collection_name="testCollection",
#     embedding_function=embeddings,
#     persist_directory = "/chromaData",
# )
# print(vector_store.similarity_search(query="巩金玮的科研经历", k=3))

