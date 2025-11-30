from langchain_text_splitters import RecursiveCharacterTextSplitter

def chunk_text(text, max_length=430, overlap=30, filetype=None):
    """
    Splits text into chunks of a specified maximum length with overlap.
    """
    separators = ["\n\n", "\n", " ", ""]
    
    # Adjust separators for Excel if needed, but default is usually fine
    if filetype == "excel":
        separators = ["\n", " ", ""]

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=max_length,
        chunk_overlap=overlap,
        separators=separators
    )
    return splitter.split_text(text)
