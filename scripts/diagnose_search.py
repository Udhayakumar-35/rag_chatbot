import os
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient

def check_index():
    try:
        credential = DefaultAzureCredential()
        search_service_endpoint = 'https://gptkb-ktpwhuisap3mm.search.windows.net'
        index_name = 'gptkbindex'
        client = SearchClient(search_service_endpoint, index_name, credential)
        
        # Check count
        count = client.get_document_count()
        print(f"Total documents in index: {count}")
        
        # Check samples
        results = client.search(search_text="*", select=["sourcepage"], top=5)
        print("\nSample source files in index:")
        for r in results:
            print(f"- {r['sourcepage']}")
            
        # Try a relevant search
        test_query = "deductible"
        print(f"\nPerforming test search for: '{test_query}'")
        results = client.search(search_text=test_query, select=["sourcepage", "content"], top=1)
        found = False
        for r in results:
            found = True
            print(f"Match found in: {r['sourcepage']}")
            print(f"Content snippet: {r['content'][:100]}...")
        if not found:
            print("No matches found for test query.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check_index()
