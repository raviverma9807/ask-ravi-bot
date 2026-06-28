from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType, VectorizedQuery
import streamlit as st

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
        st.error("1")

        try:
            vector_query = VectorizedQuery(
                vector=embedding,
                k_nearest_neighbors=10,
                fields="text_vector"
            )

            st.error("2")

            results = self.search_client.search(
                search_text=query,
                vector_queries=[vector_query],
                query_type=QueryType.SEMANTIC,
                semantic_configuration_name="default",
                top=10
            )

            st.error("3")

            context_parts = []
            sources = []
            seen_chunks = set()

            st.error("4")

            for result in results:

                st.write("Processing:", result.get("title", "Unknown"))

                try:
                    reranker_score = result.get("@search.rerankerScore", 0)
                    st.write("✓ reranker")

                    title = result.get("title", "Unknown Document")
                    st.write("✓ title")

                    caption = ""
                    captions = result.get("@search.captions")
                    st.write("✓ captions")

                    if captions and len(captions) > 0:
                        caption = captions[0].text
                    st.write("✓ caption processed")

                    chunk = result.get("chunk", "")
                    st.write("✓ chunk")

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

                    sources.append(title)

                    st.success(f"Finished {title}")

                except Exception as ex:
                    import traceback
                    st.error(f"Error in document {title}: {ex}")
                    st.code(traceback.format_exc())
                    break