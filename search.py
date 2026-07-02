import chromadb as cr
import ollama as ol
chroma_place= cr.PersistentClient(path='./loacal_chroma_db')
chroma_storage=chroma_place.get_or_create_collection(name ="pdf_space")
ques="3rd page in nexus.pdf"
query=chroma_storage.query(
    query_texts= [ques],
    n_results=2,
    
)


context='\n\n'.join(query['documents'][0])
prompt = f"""
You are a highly accurate data assistant. Answer the user's question using ONLY the provided context. 
If the answer is not contained in the context then say its not availabe and if asked for summarisation then summarise the text"

Context:
{context}

Question:
{ques}
"""
output = ol.chat(
    model='gemma4',
    messages=[{'role':'user','content':prompt}]
)
print(output['message']['content'])