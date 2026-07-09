DOCUMENT_INDEX_MAPPING = {
    "mappings": {
        "properties": {
            "id": {"type": "integer"},
            "text": {"type": "text", "analyzer": "russian"},
        }
    }
}
