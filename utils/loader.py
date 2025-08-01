from langchain_community.document_loaders import UnstructuredMarkdownLoader
from langchain_core.documents import Document
import os

def load_markdown_documents(markdown_dir: str) -> list[Document]:
    documents = []

    if not os.path.isdir(markdown_dir):
        raise NotADirectoryError(f"{markdown_dir} is not a valid directory")

    for file in os.listdir(markdown_dir):
        full_path = os.path.join(markdown_dir, file)

        if os.path.isdir(full_path):
            continue

        if " " in file:
            new_filename = file.replace(" ", "_")
            new_path = os.path.join(markdown_dir, new_filename)
            os.rename(full_path, new_path)
            print(f"Renamed: {file} -> {new_filename}")
            full_path = new_path
        else:
            print(f"No rename needed: {file}")

        # Load the markdown file
        loader = UnstructuredMarkdownLoader(full_path)
        data = loader.load()
        documents.extend(data)

    return documents
