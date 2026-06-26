from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType


class SearchService:
    def __init__(self, endpoint, api_key, index_name):
        self.search_client = SearchClient(
            endpoint=endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(api_key)
        )

    def search_documents(self, query, top=5):
        """
        Searches Azure AI Search and returns:
        - context (string)
        - sources (list of filenames)
        """

        try:
            results = self.search_client.search(
                search_text=query,
                query_type=QueryType.SEMANTIC,
                semantic_configuration_name="default",
                query_caption="extractive",
                top=top
            )

            chunks = []
            sources = []

            for result in results:

                if "chunk" in result:
                    chunks.append(result["chunk"])

                if "title" in result:
                    sources.append(result["title"])

            context = "\n\n".join(chunks)

            return context, list(set(sources))

        except Exception as ex:
            print(ex)
            return "", []