# Evaluation Plan

This project includes a simple evaluation plan for a RAG chatbot.

## Metrics

| Metric | What it measures | Example target |
|---|---|---|
| Retrieval Precision@K | How many retrieved chunks are useful | 80%+ |
| Answer Faithfulness | Whether the answer is supported by retrieved text | 90%+ |
| Answer Relevance | Whether the answer directly answers the question | 85%+ |
| Latency | Average response time | Under 3 seconds locally |
| Source Coverage | Whether answers include useful source previews | 100% |

## Manual evaluation process

1. Create 10 to 20 questions from uploaded documents.
2. For each question, check whether the correct text appears in the retrieved sources.
3. Check whether the final answer is grounded in the retrieved text.
4. Record pass/fail for retrieval and answer quality.
5. Improve chunk size, overlap, prompt, or top-k if results are weak.

## Example evaluation table

| Question | Retrieved correct chunk? | Answer grounded? | Notes |
|---|---:|---:|---|
| What is RAG? | Yes | Yes | Correct answer from sample notes |
| What database is used? | Yes | Yes | Mentions ChromaDB or Pinecone |
| What is not in the document? | Yes | Yes | Model says it does not know |
