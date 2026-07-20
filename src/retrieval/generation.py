from src.retrieval.hybrid import HybridResult
from src.common.logging import get_logger

logger = get_logger(__name__)


class GeneratedAnswer:
    def __init__(self, answer: str, sources: list[dict], has_sufficient_evidence: bool):
        self.answer = answer
        self.sources = sources
        self.has_sufficient_evidence = has_sufficient_evidence


def build_prompt(question: str, hybrid_result: HybridResult) -> str:
    context_parts: list[str] = []

    for chunk in hybrid_result.chunks:
        context_parts.append(f"[Fonte: {chunk.source_id or 'desconhecida'}]\n{chunk.text}")

    if hybrid_result.graph_context and hybrid_result.graph_context.entities:
        context_parts.append("\n--- Relações do grafo ---")
        for rel in hybrid_result.graph_context.relations:
            context_parts.append(f"- {rel.get('type', 'relacionado')}")

    context = "\n\n".join(context_parts)

    prompt = f"""Você é um assistente institucional do ICT-SJC (Instituto de Ciência e Tecnologia de São José dos Campos, UNESP).

Responda APENAS com base nas fontes fornecidas abaixo. Se as fontes não contiverem informação suficiente para responder, diga claramente que não encontrou informação suficiente.

Sempre cite as fontes utilizadas. Responda em português.

Contexto:
{context}

Pergunta: {question}

Resposta:"""
    return prompt


def generate_answer(question: str, hybrid_result: HybridResult, llm_client=None) -> GeneratedAnswer:
    if not hybrid_result.chunks:
        return GeneratedAnswer(
            answer="Não encontrei informações suficientes para responder a esta pergunta nas fontes disponíveis.",
            sources=[],
            has_sufficient_evidence=False,
        )

    prompt = build_prompt(question, hybrid_result)

    if llm_client:
        try:
            response = llm_client.complete(prompt)
            answer_text = response.text if hasattr(response, 'text') else str(response)
        except Exception as exc:
            logger.error("LLM call failed", error=str(exc))
            answer_text = "O serviço de geração de respostas está temporariamente indisponível."
    else:
        answer_text = _fallback_answer(question, hybrid_result)

    sources = [
        {"id": c.chunk_id, "source_id": c.source_id, "score": c.score}
        for c in hybrid_result.chunks[:5]
    ]

    return GeneratedAnswer(
        answer=answer_text,
        sources=sources,
        has_sufficient_evidence=True,
    )


def _fallback_answer(question: str, hybrid_result: HybridResult) -> str:
    top_chunks = hybrid_result.chunks[:3]
    if not top_chunks:
        return "Não encontrei informações suficientes para responder."
    excerpts = "\n".join(f"- {c.text[:200]}..." for c in top_chunks)
    return f"Encontrei as seguintes informações relacionadas à sua pergunta:\n\n{excerpts}\n\nNota: Esta é uma resposta automática sem processamento por modelo de linguagem."
