# Free study material for the IBM Gen AI Engineering certificate

The certificate itself is paid (Coursera subscription, ~$49/month). Everything below is
free to read or run and covers the same ground. Tagged by the course it supports:

`1` Intro to AI · `2` Gen AI intro · `3` Prompt engineering · `10` LLM architecture
`11` NLP foundations · `12` Transformers · `13` Fine-tuning · `14` Advanced fine-tuning
`15` RAG & LangChain · `16` Capstone

---

## Auditing the courses

Every course on Coursera can be **audited free**, which gives you the videos and readings
but not the graded quizzes or the certificate. If you only want the knowledge, audit is
enough — this repo's question bank replaces the quizzes.

<https://www.coursera.org/professional-certificates/ibm-generative-ai-engineering>

## IBM's own free material

| Resource | Courses |
|---|---|
| [IBM Technology topic pages](https://www.ibm.com/topics) — concise explainers on AI, ML, transformers, RAG, fine-tuning | all |
| [What is generative AI?](https://www.ibm.com/topics/generative-ai) | 2 |
| [What is a transformer model?](https://www.ibm.com/topics/transformer-model) | 12 |
| [What is RAG?](https://www.ibm.com/topics/retrieval-augmented-generation) | 15, 16 |
| [What is fine-tuning?](https://www.ibm.com/topics/fine-tuning) | 13, 14 |
| [What are AI agents?](https://www.ibm.com/topics/ai-agents) | 15 |
| [AI ethics](https://www.ibm.com/topics/ai-ethics) · [Explainable AI](https://www.ibm.com/topics/explainable-ai) | 1 |
| [watsonx.ai](https://www.ibm.com/products/watsonx-ai) · [watsonx.data](https://www.ibm.com/products/watsonx-data) · [watsonx.governance](https://www.ibm.com/products/watsonx-governance) | 1 |

## Framework documentation — the practical half

| Resource | Courses |
|---|---|
| [Hugging Face Transformers docs](https://huggingface.co/docs/transformers/index) — pipelines, AutoClasses, Trainer | 13 |
| [Tokenizer summary](https://huggingface.co/docs/transformers/tokenizer_summary) — BPE, WordPiece, SentencePiece | 10 |
| [Hugging Face glossary](https://huggingface.co/docs/transformers/glossary) — attention mask, special tokens | 10, 12 |
| [Single-GPU training performance](https://huggingface.co/docs/transformers/perf_train_gpu_one) — OOM, accumulation, mixed precision | 13 |
| [PEFT / LoRA conceptual guide](https://huggingface.co/docs/peft/conceptual_guides/lora) | 13, 14 |
| [TRL docs](https://huggingface.co/docs/trl/index) — SFT, reward modelling, PPO, DPO trainers | 14 |
| [PyTorch data loading](https://pytorch.org/docs/stable/data.html) — Dataset, DataLoader, collate_fn | 10 |
| [nn.EmbeddingBag](https://pytorch.org/docs/stable/generated/torch.nn.EmbeddingBag.html) | 11 |
| [nn.TransformerEncoder](https://pytorch.org/docs/stable/generated/torch.nn.TransformerEncoder.html) | 12 |
| [LangChain concepts](https://python.langchain.com/docs/concepts/) — the component vocabulary | 15, 16 |
| [LangChain RAG tutorial](https://python.langchain.com/docs/tutorials/rag/) | 16 |
| [FAISS](https://github.com/facebookresearch/faiss) | 15 |
| [Gradio](https://www.gradio.app/) | 16 |

## Free courses elsewhere

- **Hugging Face LLM Course** — <https://huggingface.co/learn/llm-course> · the closest free
  equivalent to courses 10–13, with runnable notebooks.
- **Hugging Face Agents Course** — <https://huggingface.co/learn/agents-course> · covers
  course 15's ground with a free certificate.
- **DeepLearning.AI short courses** — <https://www.deeplearning.ai/courses/> · *Building and
  Evaluating Advanced RAG*, *Finetuning Large Language Models*, *Building Agentic RAG with
  LlamaIndex*.
- **Google ML Crash Course** — <https://developers.google.com/machine-learning/crash-course>
  · fills course 1's foundations.

## Papers behind the material

- Attention Is All You Need (transformer) — <https://arxiv.org/abs/1706.03762>
- BERT — <https://arxiv.org/abs/1810.04805>
- word2vec — <https://arxiv.org/abs/1301.3781>
- Dense Passage Retrieval — <https://arxiv.org/abs/2004.04906>
- RAG — <https://arxiv.org/abs/2005.11401>
- LoRA — <https://arxiv.org/abs/2106.09685>
- QLoRA — <https://arxiv.org/abs/2305.14314>
- InstructGPT / RLHF — <https://arxiv.org/abs/2203.02155>
- PPO — <https://arxiv.org/abs/1707.06347>
- DPO — <https://arxiv.org/abs/2305.18290>
- Chain-of-Thought — <https://arxiv.org/abs/2201.11903>
- Self-Consistency — <https://arxiv.org/abs/2203.11171>

## What this bank does not cover

Courses 4–9 — Python for Data Science, Flask, Data Analysis with Python, Machine Learning
with Python, and Deep Learning with Keras — are excluded by design. They teach library work
that multiple choice tests poorly. If you need them, the official course labs are the right
practice, not a question bank.

Course 16 is a **build project**. The questions here cover the decisions it forces —
chunking, embedding consistency, retrieval failure modes, index maintenance — but they are
not a substitute for building it.
