from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
import hnswlib
from sentence_transformers import SentenceTransformer
import os

# Initialize FastAPI app
app = FastAPI(title="Dataverse NLP Search API", description="API for searching datasets based on text queries", version="1.0")

# Load Data
app_files = "./app"
fname = "dataverse"
dv_records = pd.read_pickle(os.path.join(app_files,fname + ".pkl"), compression={'method': 'gzip', 'compresslevel': 5, 'mtime': 1})

# Load Model
# model = SentenceTransformer('all-mpnet-base-v2')
# model.save("./all-mpnet-base-v2")

# load a local version
model = SentenceTransformer(os.path.join(app_files,"all-mpnet-base-v2"))
nemb = model[1].word_embedding_dimension

# Load Search Indexes
cols2embed = ['Description', 'Title', 'Meta']
space = 'cosine'

p0 = pd.read_pickle(os.path.join(app_files,f"{fname}-all-mpnet-base-v2-{cols2embed[0]}-{space}.pkl"), compression={'method': 'gzip', 'compresslevel': 5, 'mtime': 1})
p1 = pd.read_pickle(os.path.join(app_files,f"{fname}-all-mpnet-base-v2-{cols2embed[1]}-{space}.pkl"), compression={'method': 'gzip', 'compresslevel': 5, 'mtime': 1})
p2 = pd.read_pickle(os.path.join(app_files,f"{fname}-all-mpnet-base-v2-{cols2embed[2]}-{space}.pkl"), compression={'method': 'gzip', 'compresslevel': 5, 'mtime': 1})

K = 10
p0.set_ef(100)
p1.set_ef(100)
p2.set_ef(100)

# Define Request Model
class QueryRequest(BaseModel):
    query: str

# API Endpoint
@app.post("/search", summary="Search the Dataverse records", response_model=dict)
def search(request: QueryRequest):
    query = request.query
    qemb = model.encode(query)
    
    lab, dist = [], []
    for p in [p0, p1, p2]:
        l, d = p.knn_query(qemb, k=K)
        lab.extend(l[0].tolist())
        dist.extend(d[0].tolist())
    
    res = pd.DataFrame({
        'Title': dv_records.Title.iloc[lab],
        'Description': dv_records.Description.iloc[lab],
        'DOI': dv_records.doi.iloc[lab],
        'Authors': dv_records.Authors.iloc[lab],
        'Keywords': dv_records.Keywords.iloc[lab],
        'Subject': dv_records.Subject.iloc[lab],
        'Distance': dist
    })
    
    res = res.drop_duplicates("DOI", keep='first')
    res = res.sort_values(by=['Distance'], ascending=True)
    
    return {"results": res.to_dict(orient='records')}

# Run the API with: `uvicorn filename:app --reload`
