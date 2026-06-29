from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType, VectorizedQuery

import logging

class SearchService:
    def __init__(self, endpoint, api_key, index_name, logger=None):
        self.search_client = SearchClient(
            endpoint=endpoint,
            index_name=index_name,
            credential=AzureKeyCredential(api_key),
            logger=logger or logging.getLogger(__name__)
        )

    def search_documents(self, query, embedding, top=10):
        """
        Searches Azure AI Search and returns:
        - context (formatted string)
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
                semantic_configuration_name="rag-1782364824827-semantic-configuration",
                top=top
            )


            context_parts = []
            seen_chunks = set()


            for result in results:

                try:

                    reranker_score = result.get("@search.rerankerScore") or 0

                    title = result.get("title", "Unknown Document")

                    caption = ""
                    captions = result.get("@search.captions")

                    if captions and len(captions) > 0:
                        caption = captions[0].text


                    chunk = result.get("chunk", "")

                    content = chunk

                    if caption:
                        content = f"{caption}\n\n{chunk}"

                    if not content:
                        continue

                    content = content.strip()

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

                    
                except Exception as ex:
                    logger.exception(
                        f"Error processing document: {result.get('title', 'Unknown')}"
                    )
                    continue


            context = "\n".join(context_parts)

            return context

        except Exception as ex:
            logger.exception("Azure AI Search failed.")
            return ""