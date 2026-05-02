import os
from langchain_community.vectorstores import FAISS
# PDF Loader (optimized import)
from langchain_community.document_loaders.pdf import PyPDFLoader

# Text Splitter
from langchain_text_splitters import RecursiveCharacterTextSplitter

# Embeddings
from langchain_community.embeddings import HuggingFaceEmbeddings

DATA_PATH = "data/"


# 🔹 Clean text
def clean_text(text):
    text = text.replace("- ", "")
    text = text.replace("\n", " ")
    return text


# 🔹 Load PDFs
def load_pdfs(data_path):
    documents = []

    for file in os.listdir(data_path):
        if file.endswith(".pdf"):
            print(f"📄 Loading: {file}")
            loader = PyPDFLoader(os.path.join(data_path, file))
            docs = loader.load()

            for doc in docs:
                doc.page_content = clean_text(doc.page_content)

            documents.extend(docs)

    return documents


# 🔹 Split text
def split_text(documents):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=30
    )
    return splitter.split_documents(documents)


# 🔹 Main
def main():
    print("📄 Loading PDFs...")
    documents = load_pdfs(DATA_PATH)

    print("✂️ Splitting text...")
    chunks = split_text(documents)

    print(f"📊 Total Chunks: {len(chunks)}")

    print("🔢 Creating embeddings...")
    embedding = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    print("💾 Storing in FAISS...")
    db = FAISS.from_documents(chunks, embedding)

    db.save_local("faiss_index")

    print("✅ Index created successfully!")


if __name__ == "__main__":
    main()
