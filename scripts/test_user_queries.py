import os
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient

def test_queries():
    try:
        credential = DefaultAzureCredential()
        endpoint = 'https://gptkb-ktpwhuisap3mm.search.windows.net'
        index_name = 'gptkbindex'
        client = SearchClient(endpoint, index_name, credential)
        
        queries = [
            'What is included in my Northwind Health Plus plan that is not in standard?',
            'What happens in a performance review?'
        ]
        
        for q in queries:
            print(f"\nQUERY: {q}")
            results = client.search(search_text=q, top=2, select=["sourcepage", "content"])
            found = False
            for r in results:
                found = True
                print(f"--- MATCH found in {r['sourcepage']} ---")
                print(f"Content (first 200 chars): {r['content'][:200]}...")
            if not found:
                print("--- NO MATCHES FOUND ---")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_queries()
