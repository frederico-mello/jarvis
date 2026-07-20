from src.retrieval.search import search_by_embedding, search_by_text, ChunkResult
from src.retrieval.traversal import GraphContext
from src.graph.driver import get_driver
from src.common.logging import get_logger

logger = get_logger(__name__)


class HybridResult:
    def __init__(self, chunks: list[ChunkResult], graph_context: GraphContext | None = None):
        self.chunks = chunks
        self.graph_context = graph_context


def hybrid_search(embedding: list[float], text_query: str | None = None,
                  top_k: int = 10, graph_depth: int = 2) -> HybridResult:
    vector_results = search_by_embedding(embedding, top_k=top_k)

    text_results: list[ChunkResult] = []
    if text_query:
        text_results = search_by_text(text_query, top_k=top_k)

    seen_ids: set[str] = set()
    merged: list[ChunkResult] = []

    for r in vector_results + text_results:
        if r.chunk_id not in seen_ids:
            seen_ids.add(r.chunk_id)
            merged.append(r)

    merged.sort(key=lambda x: x.score, reverse=True)
    merged = merged[:top_k]

    return HybridResult(chunks=merged)


def hybrid_search_with_graph(embedding: list[float], text_query: str | None = None,
                              sector_id: str | None = None, top_k: int = 10) -> HybridResult:
    result = hybrid_search(embedding, text_query, top_k=top_k)

    graph_context = None
    if sector_id:
        driver = get_driver()
        with driver.session() as session:
            from src.retrieval.traversal import traverse_sector_services, traverse_sector_hierarchy
            services = session.execute_read(traverse_sector_services, sector_id)
            hierarchy = session.execute_read(traverse_sector_hierarchy, sector_id)
            all_entities = services.entities + hierarchy.entities
            all_relations = services.relations + hierarchy.relations
            graph_context = GraphContext(entities=all_entities, relations=all_relations)
        driver.close()

    return HybridResult(chunks=result.chunks, graph_context=graph_context)
