# backend/app.py
from docarray import DocumentArray, Document
import numpy as np
import json

from flask import Flask, request, jsonify
from jina import Document, Flow
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# Load indexed data from pickle file
# with open('indexed_data.pickle', 'rb') as handle:
#     indexed_data = pickle.load(handle)
da = DocumentArray()

with open('icecat-products-w_price-19k-20201127.json') as f:
    jdocs = json.load(f)
for doc in jdocs:
    d = Document(text=" ".join([doc[item] for item in doc if item.startswith("title") 
    or item.startswith("attr_t")
    or item.startswith("short_description") 
    or item.startswith("name")
    or item.startswith("supplier")]), tags=doc)
    da.append(d)


# Create Flow for querying
f = Flow().add(name='encoder', uses='jinahub://TransformerTorchEncoder/latest', install_requirements=True)\
         .add(uses='jinahub://AnnLiteIndexer/latest', install_requirements=True,
              uses_with={'columns': [('supplier', 'str'), ('price', 'float'),
                                     ('attr_t_product_type', 'str'), ('attr_t_product_colour', 'str')],
                         'n_dim': 768})

da = da[1:1000]

with f:
  da = f.index(da)
  print(da[0])
  print(type(da))

@app.route('/')
def index():
    return "GN Vector Search Engine Backend is running!"

@app.route('/search', methods=['POST'])
def search():
    query_text = request.json['query']
    query = Document(text=query_text)

    # Search for similar documents
    with f:
        results = f.search(query)

    # Extract and return the tags of the most similar document
    tags = results[0].matches[0].tags
    return jsonify(tags)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)

