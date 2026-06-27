from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType, VectorizedQuery


class SearchService:
    def __init__(self, endpoint, api_key, index_name):
        self.search_client = SearchClient(
            endpoint=endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(api_key)
        )

    def search_documents(self, query, embedding, top=10):
        """
        Searches Azure AI Search and returns:
        - context (formatted string)
        - sources (list of document names)
        """

        try:
            vector_query = VectorizedQuery(
                vector=embedding,
                k_nearest_neighbors=10,
                fields="text_vector"
            )

            results = self.search_client.search(
                search_text=query,
                vector_queries=[vector_query],
                query_type=QueryType.SEMANTIC,
                semantic_configuration_name="default",
                top=10
            )

            context_parts = []
            sources = []
            seen_chunks = set()

            for result in results:

                # Skip weak semantic matches
                reranker_score = result.get("@search.rerankerScore", 0)
                if reranker_score < 0.5:
                    continue

                title = result.get("title", "Unknown Document")

                # Prefer semantic caption if available
                caption = ""
                captions = result.get("@search.captions")

                if captions and len(captions) > 0:
                    caption = captions[0].text

                chunk = result.get("chunk", "")

                # Use caption + chunk for better context
                content = caption if caption else chunk

                if not content:
                    continue

                content = content.strip()

                # Remove duplicate chunks
                if content in seen_chunks:
                    continue

                seen_chunks.add(content)

                context_parts.append(
                    f"""
==================================================
Document: {title}

Relevant Information:
{content}
"""
                )

                sources.append(title)

            context = "\n".join(context_parts)

            return context, sorted(set(sources))

        except Exception as ex:
            print(f"Azure AI Search Error: {ex}")
            return "", []