# Free Study Material for NCP-AAI

Everything here is free to read/run. Paid items are listed only in the last section, so you
know what you are *not* missing. Each entry is tagged with the blueprint domains it covers:

`AA` architecture · `AD` development · `ET` evaluation · `DS` deployment · `CP` cognition/memory
`KD` knowledge/data · `NP` NVIDIA platform · `RM` run/monitor · `SE` safety · `HO` human oversight

---

## 1. Official NVIDIA — free courses (DLI)

Register free at learn.nvidia.com with an NVIDIA Developer account. Free courses issue a
certificate of competency (not the NCP credential).

| Course | Domains | Why it matters |
|---|---|---|
| [Agentic AI Explained](https://learn.nvidia.com/courses/course-detail?course_id=course-v1%3ADLI+S-FX-39+V1) (free, ~1h, no code) | AA CP HO | NVIDIA's own vocabulary for perceive→reason→act→learn. The exam uses this framing. |
| [Generative AI Explained](https://learn.nvidia.com/courses/course-detail?course_id=course-v1%3ADLI+S-FX-07+V1) (free, ~2h) | KD SE | Baseline LLM concepts, hallucination framing. |
| [Building LLM Applications With Prompt Engineering](https://learn.nvidia.com/courses/course-detail?course_id=course-v1%3ADLI+S-FX-16+V1) (free, ~8h) | AD CP | Prompt patterns that become agent system prompts. |
| [Introduction to NIM Microservices](https://www.nvidia.com/en-us/training/) (free, ~1h) | NP DS | NIM is the single most-tested NVIDIA product name. |
| [Sizing LLM Inference Systems](https://www.nvidia.com/en-us/training/) (free) | DS NP | Throughput vs. latency, batching, memory math. |
| [Introduction to Transformer-Based NLP](https://www.nvidia.com/en-us/training/) (free) | KD | Embeddings and attention background. |

Browse the live free list: **<https://www.nvidia.com/en-us/training/find-training/?Free+Courses=Free>**
(the free set rotates — check before paying for anything).

## 2. Official NVIDIA — free docs that mirror exam objectives

These are the highest-yield reading for the `NP`, `DS`, `SE` domains. The exam asks
"which NVIDIA component do you use for X", so learn the *boundaries* between products.

| Resource | Domains |
|---|---|
| [NeMo Agent Toolkit docs](https://docs.nvidia.com/nemo/agent-toolkit/latest/) + [GitHub](https://github.com/NVIDIA/NeMo-Agent-Toolkit) | AA AD RM ET |
| [NeMo Agent Toolkit examples](https://github.com/NVIDIA/NeMo-Agent-Toolkit/tree/develop/examples) (runnable) | AD AA |
| [NeMo Agent Toolkit community examples](https://github.com/NVIDIA/NeMo-Agent-Toolkit-Examples) | AD |
| [NeMo Guardrails docs](https://docs.nvidia.com/nemo/guardrails/latest/) + [GitHub](https://github.com/NVIDIA/NeMo-Guardrails) | SE HO |
| [NIM for LLMs docs](https://docs.nvidia.com/nim/large-language-models/latest/) | NP DS |
| [NeMo Retriever / NIM retrieval docs](https://docs.nvidia.com/nim/#retrieval) | KD NP |
| [NeMo Framework user guide](https://docs.nvidia.com/nemo-framework/user-guide/latest/) (Curator, Customizer, Evaluator) | ET KD NP |
| [TensorRT-LLM docs](https://nvidia.github.io/TensorRT-LLM/) | DS NP |
| [Triton Inference Server docs](https://docs.nvidia.com/deeplearning/triton-inference-server/user-guide/docs/) | DS NP |
| [NVIDIA Dynamo](https://github.com/ai-dynamo/dynamo) (disaggregated serving, KV-aware routing) | DS |
| [NVIDIA AI Blueprints](https://build.nvidia.com/blueprints) — reference agentic architectures | AA NP |
| [Generative AI Examples](https://github.com/NVIDIA/GenerativeAIExamples) — end-to-end RAG/agent stacks | AD KD DS |
| [build.nvidia.com](https://build.nvidia.com) — free API credits to call NIM endpoints | NP AD |
| [Nemotron models hub](https://developer.nvidia.com/nemotron) — open-weight agentic model family | NP DS |
| [Inside Nemotron 3](https://developer.nvidia.com/blog/inside-nvidia-nemotron-3-techniques-tools-and-data-that-make-it-efficient-and-accurate/) — hybrid Mamba-Transformer MoE, 1M context, NVFP4, MTP | NP DS CP |
| [NemoClaw docs](https://docs.nvidia.com/nemoclaw/user-guide/openclaw/home) + [blog](https://developer.nvidia.com/blog/build-a-secure-always-on-local-ai-agent-with-nvidia-nemoclaw-and-openclaw/) — local agents, OpenShell sandboxing | AA SE NP |
| [NeMo microservices](https://docs.nvidia.com/nemo/microservices/latest/) — Customizer, Evaluator, Guardrails, Retriever as services | ET NP |
| [cuVS GPU vector search](https://docs.rapids.ai/api/cuvs/stable/) — CAGRA, IVF-PQ, index build acceleration | KD NP |
| [MIG user guide](https://docs.nvidia.com/datacenter/tesla/mig-user-guide/) | DS NP |
| [NVIDIA Technical Blog: agentic AI tag](https://developer.nvidia.com/blog/category/generative-ai/) | all |
| [NVIDIA On-Demand: GTC agentic AI sessions](https://www.nvidia.com/en-us/on-demand/) (free video) | all |

## 3. Framework docs (free) — the `AD` and `AA` backbone

The exam is vendor-aware but concept-first. You need to recognize orchestration patterns
regardless of library.

- **LangGraph** — [docs](https://langchain-ai.github.io/langgraph/) · graph/state-machine agents,
  checkpointers, interrupts, human-in-the-loop. Read: persistence, `interrupt_before`, subgraphs.
- **LlamaIndex** — [docs](https://docs.llamaindex.ai/) · ingestion, node parsers, query engines,
  `AgentWorkflow`, routers. Read: chunking + retrieval composition.
- **CrewAI** — [docs](https://docs.crewai.com/) · role-based multi-agent, sequential vs. hierarchical.
- **Microsoft AutoGen / AG2** — [docs](https://microsoft.github.io/autogen/) · conversational
  multi-agent, group chat topologies.
- **Model Context Protocol (MCP)** — [spec](https://modelcontextprotocol.io/) · tools/resources/prompts,
  transports, why it exists. Increasingly tested as the tool-integration standard.
- **OpenTelemetry GenAI semantic conventions** — [spec](https://opentelemetry.io/docs/specs/semconv/gen-ai/)
  · span names/attributes for LLM and agent calls. Core `RM` material.

## 4. Evaluation (free) — the `ET` domain

- **RAGAS** — [docs](https://docs.ragas.io/) · faithfulness, answer relevancy, context precision/recall.
  Memorize which metric needs ground truth and which does not.
- **TruLens** — [docs](https://www.trulens.org/) · RAG triad (context relevance, groundedness, answer relevance).
- **DeepEval** — [docs](https://deepeval.com/) · G-Eval, agent/tool-correctness metrics.
- **LangSmith evaluation concepts** — [docs](https://docs.smith.langchain.com/evaluation/concepts)
  · trajectory vs. final-response evaluation, pairwise judges.
- **HELM / lm-evaluation-harness** — [EleutherAI harness](https://github.com/EleutherAI/lm-evaluation-harness)
- Agent benchmarks worth knowing by name: **GAIA**, **SWE-bench**, **WebArena**, **AgentBench**, **τ-bench (tau-bench)**, **BFCL** (Berkeley Function-Calling Leaderboard), **MMLU-Pro**, **MTEB** (embeddings/reranking).

## 5. Papers (free) — the concepts behind the question stems

Read the abstract + method of each; that is enough for exam-level recall.

**Reasoning & planning (`CP`)**
- Chain-of-Thought — <https://arxiv.org/abs/2201.11903>
- Self-Consistency — <https://arxiv.org/abs/2203.11171>
- ReAct — <https://arxiv.org/abs/2210.03629>
- Reflexion — <https://arxiv.org/abs/2303.11366>
- Tree of Thoughts — <https://arxiv.org/abs/2305.10601>
- Least-to-Most prompting — <https://arxiv.org/abs/2205.10625>
- Plan-and-Solve — <https://arxiv.org/abs/2305.04091>
- Toolformer — <https://arxiv.org/abs/2302.04761>
- MRKL systems — <https://arxiv.org/abs/2205.00445>
- Voyager (skill library / procedural memory) — <https://arxiv.org/abs/2305.16291>
- Generative Agents (memory stream, reflection) — <https://arxiv.org/abs/2304.03442>
- MemGPT (virtual context management) — <https://arxiv.org/abs/2310.08560>

**Retrieval & knowledge (`KD`)**
- RAG (Lewis et al.) — <https://arxiv.org/abs/2005.11401>
- Dense Passage Retrieval — <https://arxiv.org/abs/2004.04906>
- ColBERT (late interaction) — <https://arxiv.org/abs/2004.12832>
- HyDE (hypothetical document embeddings) — <https://arxiv.org/abs/2212.10496>
- Self-RAG — <https://arxiv.org/abs/2310.11511>
- Corrective RAG (CRAG) — <https://arxiv.org/abs/2401.15884>
- GraphRAG — <https://arxiv.org/abs/2404.16130>
- Lost in the Middle (context position effects) — <https://arxiv.org/abs/2307.03172>
- RAPTOR (hierarchical summary trees) — <https://arxiv.org/abs/2401.18059>

**Multi-agent (`AA`)**
- AutoGen — <https://arxiv.org/abs/2308.08155>
- MetaGPT (SOP-driven roles) — <https://arxiv.org/abs/2308.00352>
- CAMEL (role-playing) — <https://arxiv.org/abs/2303.17760>
- Society of Mind / debate — <https://arxiv.org/abs/2305.14325>
- Survey: LLM-based autonomous agents — <https://arxiv.org/abs/2308.11432>
- Survey: LLM multi-agent systems — <https://arxiv.org/abs/2402.01680>

**Tuning & efficiency (`ET`, `DS`)**
- LoRA — <https://arxiv.org/abs/2106.09685>
- QLoRA — <https://arxiv.org/abs/2305.14314>
- P-Tuning v2 / prompt tuning — <https://arxiv.org/abs/2110.07602>
- DPO — <https://arxiv.org/abs/2305.18290>
- InstructGPT / RLHF — <https://arxiv.org/abs/2203.02155>
- PagedAttention / vLLM — <https://arxiv.org/abs/2309.06180>
- FlashAttention — <https://arxiv.org/abs/2205.14135>
- Speculative decoding — <https://arxiv.org/abs/2211.17192>
- Medusa (multi-head decoding) — <https://arxiv.org/abs/2401.10774>
- Megatron-LM (tensor parallelism) — <https://arxiv.org/abs/1909.08053>
- Mixture-of-Experts / Switch Transformers — <https://arxiv.org/abs/2101.03961>

**Safety (`SE`, `HO`)**
- Constitutional AI — <https://arxiv.org/abs/2212.08073>
- Universal & transferable adversarial attacks (GCG) — <https://arxiv.org/abs/2307.15043>
- Indirect prompt injection — <https://arxiv.org/abs/2302.12173>
- NeMo Guardrails paper — <https://arxiv.org/abs/2310.10501>
- OWASP Top 10 for LLM Applications — <https://genai.owasp.org/llm-top-10/>
- NIST AI Risk Management Framework — <https://www.nist.gov/itl/ai-risk-management-framework>
- EU AI Act (risk tiers, GPAI obligations) — <https://artificialintelligenceact.eu/>
- MITRE ATLAS (adversarial ML threat matrix) — <https://atlas.mitre.org/>

## 6. Free courses elsewhere (concept coverage, no NVIDIA specifics)

- **DeepLearning.AI short courses** (free) — *Functions, Tools and Agents with LangChain*,
  *AI Agents in LangGraph*, *Multi AI Agent Systems with crewAI*, *Building and Evaluating
  Advanced RAG*, *Building Agentic RAG with LlamaIndex*, *Evaluating and Debugging Generative AI*.
  <https://www.deeplearning.ai/courses/>
- **Hugging Face Agents Course** (free, with certificate) — <https://huggingface.co/learn/agents-course>
- **Hugging Face LLM Course** — <https://huggingface.co/learn/llm-course>
- **Anthropic / OpenAI agent-building guides** (free PDFs, good on tool design and guardrails)
  — <https://www.anthropic.com/engineering> · <https://cdn.openai.com/business-guides-and-resources/a-practical-guide-to-building-agents.pdf>
- **Google ADK / Agent Development Kit docs** (free) — <https://google.github.io/adk-docs/>

## 7. What is paid (for reference)

NVIDIA's *recommended* prep is paid DLI training. You do not need it to pass, but if you buy
one thing, buy the first:

| Course | Price | Hours |
|---|---|---|
| Building Agentic AI Applications With LLMs | $90 | 8 |
| Building RAG Agents With LLMs | $90 | 8 |
| Introduction to Deploying RAG Pipelines for Production at Scale | $90 | 8 |
| Evaluating RAG and Semantic Search Systems | $30 | 3 |
| Adding New Knowledge to LLMs (instructor-led) | $500 | 8 |

Exam itself: **$200**, booked through Certiverse via the
[certification page](https://www.nvidia.com/en-us/learn/certification/agentic-ai-professional/).

> NVIDIA periodically runs free-DLI promotions (GTC, developer-day events). Check
> <https://www.nvidia.com/en-us/training/find-training/?Free+Courses=Free> before purchasing —
> the $90 agentic courses have been free during past GTC windows.

## 8. Third-party exam guides — read for coverage, not for answers

These are free, and useful for one purpose: they list which topics, products and terms
they believe are tested, which is a cross-check on your own coverage. Treat their technical
claims as unverified — one of them attributes the **CLASSic** evaluation framework
(Cost, Latency, Accuracy, Stability, Security) to NVIDIA when it is Aisera's.

- [Preporato NCP-AAI complete guide](https://preporato.com/blog/nvidia-ncp-aai-certification-complete-guide-2025)
- [Whizlabs NCP-AAI guide](https://www.whizlabs.com/blog/ncp-aai-guide/)
- [FlashGenius NCP-AAI guide](https://flashgenius.net/blog-article/your-comprehensive-guide-to-the-nvidia-agentic-ai-llm-professional-certification-ncp-aai)

Their *practice questions* are a different matter — see below.

## 9. Other people's practice exams

A second opinion is worth having: different authors probe different corners of the
blueprint, and a question you have never seen is a better test than one you wrote.
Linked, never copied — every question in this repo's simulator is original.

| Source | Cost | What you get |
|---|---|---|
| [CertificationPractice](https://certificationpractice.com/practice-exams/nvidia-certified-professional-agentic-ai) | free | Six practice exams, around 420 questions — the most substantial free set found. |
| [Preporato free questions](https://preporato.com/free/agentic-ai-professional/questions) | free tier | 29 questions with explanations, no signup; full set is paid. |
| [OpenExamPrep](https://open-exam-prep.com/practice/ncp-aai) | free | ReAct, multi-agent, NIM, NeMo Retriever, Guardrails, evals, observability. |
| [ExamHeist](https://www.examheist.com/practice/nvidia/ncp-aai/) | free | 182 questions with written explanations. |

These are also linked from the **Practice elsewhere** panel in the web simulator.

> CertificationPractice rate-limits automated requests, so its link could not be
> machine-checked with the others — it works in a browser.

## 10. Deliberately excluded

The line is not "third party" but what the site claims to be selling. Practice exams written
by their authors are listed above. Sites advertising **actual**, **real**, or **verified**
exam questions — validexamdumps, itexams, certshero, exams4sure, passitexams, Quizlet dump
decks — are selling content reconstructed from live exams. That breaches the NVIDIA
candidate agreement, is grounds for revoking a credential, and is frequently wrong. They are
not linked here.
