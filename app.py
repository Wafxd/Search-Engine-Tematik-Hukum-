from flask import Flask, request, render_template
import csv
import sys
from search_helper import get_best_documents, load_data, get_query, relevance_feedback
from constants import *
from QueryExpansion import get_new_query_strings, strip_query_to_free_text

app = Flask(__name__)

# Set the maximum field size for CSV
max_int = sys.maxsize
while True:
    try:
        csv.field_size_limit(max_int)
        break
    except OverflowError:
        max_int = int(max_int / 10)

# Function to read CSV and store document properties
def read_csv(file_path):
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return {row['id']: row for row in reader}

# Function to perform search
def perform_search(query):
    dictionary_file = 'dictionary.txt'
    postings_file = 'postings.txt'
    doc_properties_file = 'properties.txt'
    newdata = 'data/newdatafull.csv'

    dictionary = load_data(dictionary_file)
    doc_properties = load_data(doc_properties_file)
    documents = read_csv(newdata)

    with open(postings_file, 'rb') as p:
        result = get_results([query], p, dictionary, doc_properties)

    # Retrieve document information based on search result IDs
    document_info = get_document_info(result, documents)
    
    return document_info

def get_results(query_data, postings_handler, dictionary, doc_properties):
    original_query_string = query_data[0]
    queries = get_new_query_strings(original_query_string)
    result = []
    result_set = set(result)
    for query in queries:
        query, is_boolean = get_query(query)
        docs = get_best_documents(postings_handler, dictionary, doc_properties, query, is_boolean)
        docs = list(filter(lambda x: x not in result_set, docs))
        result_set = result_set.union(set(docs))
        result += docs
    return result

def get_document_info(document_ids, documents):
    info = []
    for doc_id in document_ids:
        if doc_id in documents:
            info.append(documents[doc_id])
    return info

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
    query = request.form.get('query') or request.args.get('query')
    per_page = int(request.form.get('per_page', request.args.get('per_page', 10)))
    page = int(request.args.get('page', 1))

    results = perform_search(query) if query else []

    total_pages = (len(results) + per_page - 1) // per_page  # Calculate total pages
    start = (page - 1) * per_page
    end = start + per_page
    paginated_results = results[start:end]

    return render_template('index.html', query=query, results=paginated_results, per_page=per_page, page=page, total_pages=total_pages)

@app.route('/detail/<document_id>', methods=['GET'])
def detail(document_id):
    documents = read_csv('data/newdatafull.csv')
    document = documents.get(document_id)
    return render_template('detail.html', document=document)

app.run(debug=True)
