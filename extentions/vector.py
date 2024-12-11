import os,dashscope,chromadb,warnings
warnings.filterwarnings("ignore")
from langchain_community.document_loaders import TextLoader,PyPDFium2Loader,CSVLoader,SeleniumURLLoader,UnstructuredWordDocumentLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import DashScopeEmbeddings
from langchain_core.documents import Document
from langchain_chroma import Chroma
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
def save_to_chromaDB_high_Quantity(file_path,vector_store):
    '''
    :param file_path: 文件路径
    :param vector_store: ChromaDB对象
    '''
    split_docs=load_file_split(file_path=file_path)
    document_ids=vector_store.add_documents(split_docs)
    print(document_ids)
    ###加入到mongodb数据库 待写

def updata_embedding_data_row(vector_store,ids,text):
    '''
    :param vector_store: ChromaDB对象
    :param ids: 文档id
    :param text: 更新文本
    '''
    updated_document = Document(page_content=text)
    vector_store.update_document(document_id=ids, document=updated_document)

    ###加入到mongodb数据库 待写

def delete_embedding_data_row(vector_store,ids):
    '''
    :param vector_store: ChromaDB对象
    :param ids: 单个文档id或文档id列表
    '''
    if isinstance(ids,str):
        vector_store.delete_document(document_id=ids)
        ###同步到mongodb数据库 待写
    elif isinstance(ids,list):
        for id in ids:
            vector_store.delete_document(document_id=id)
            ###同步到mongodb数据库 待写

def delete_embedding_collection(vector_store):
    '''
    :param vector_store: ChromaDB对象
    '''
    vector_store.delete_collection()
    ###同步到mongodb数据库 待写


vector_store = Chroma(
    collection_name="testCollection",
    embedding_function=embedding_model_list["qianwen_embedding_v1"],
    persist_directory = "/chromaData",
)


