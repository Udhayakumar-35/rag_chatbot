import os
from azure.identity import DefaultAzureCredential
from azure.search.documents import SearchClient

def debug_retrieval():
    try:
        credential = DefaultAzureCredential()
        endpoint = 'https://gptkb-ktpwhuisap3mm.search.windows.net'
        index_name = 'gptkbindex'
        client = SearchClient(endpoint, index_name, credential)
        
        # We want to see if the search is finding the documents we expect
        query = 'What is included in my Northwind Health Plus plan that is not in standard?'
        print(f"DEBUGGING QUERY: {query}")
        
        # Test keyword search
        print("\n--- KEYWORD SEARCH RESULTS (Top 10) ---")
        results = client.search(search_text=query, top=10, select=["sourcepage", "content"])
        found_pages = {}
        for r in results:
            page = r['sourcepage']
            found_pages[page] = found_pages.get(page, 0) + 1
            print(f"Source: {page}")
        
        print("\nPage Distribution:")
        for page, count in found_pages.items():
            print(f"- {page}: {count} chunks")
            
        # Specific check for the two detail files
        print("\nChecking for specific detail files...")
        results = client.search(search_text="Northwind Health Plus Standard Comparison", top=5, select=["sourcepage", "content"])
        for r in results:
            if "Health_Plus" in r['sourcepage'] or "Standard" in r['sourcepage']:
                print(f"Found relevant file: {r['sourcepage']}")
                print(f"Content preview: {r['content'][:200]}...")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_retrieval()
