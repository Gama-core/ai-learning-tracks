# Six weeks of Agentic AI

Roughly 6–8 hours a week. The order is deliberate: the heaviest topic areas first while you
have the most runway, NVIDIA product specifics late (they are memorisation and decay fast),
and full timed assessments only in the last two weeks so the score means something.

Every week ends with the same loop:

```bash
./sim.py -k agentic-ai practice -d <domain>   # learn
./sim.py review                 # whatever the scheduler says is due
./sim.py stats                  # check where you actually stand
```

`stats` ends with your weakest **concepts**, ranked by what each gap costs across the track, and
hands you the two commands that fix it: `practice -c <concept>` to drill it and
`cheat -d <section>` to read it. Work that list top-down rather than guessing.

And every day you study at all, start with:

```bash
./sim.py review    # due questions
./sim.py flash     # due flashcards
```

That is the part that makes week 1's work still be there in week 6. Five minutes of review
beats thirty minutes of rereading.

---

## Week 0 — baseline (1 hour)

Take a cold timed assessment before studying anything. It is meant to be unpleasant; it
tells you which topic areas you already have from work experience and which are genuinely
new.

```bash
./sim.py -k agentic-ai exam
```

Write down the per-domain numbers. You will compare against them in week 5.

---

## Week 1 — Agent architecture + development (30% of the track)

The two heaviest domains, and the ones most likely to reward what you already do.

**Read** ([RESOURCES.md](RESOURCES.md) §3)
- LangGraph concepts: low-level graph/state, persistence, multi-agent, human-in-the-loop
- Anthropic *Building effective agents* — the workflow/agent distinction and the named patterns
- MCP specification: architecture, server concepts (tools, resources, prompts)
- Skim A2A to know where its boundary sits versus MCP

**Build** — the single highest-yield exercise in this plan. Write one small agent twice:
once as a free-form ReAct loop, once as an explicit state graph with a checkpointer. Kill
the process mid-run and resume it. You will not forget what persistence buys you.

**Drill**
```bash
./sim.py -k agentic-ai practice -d agent-architecture
./sim.py -k agentic-ai practice -d agent-development
```

Target: 75%+ on both before moving on.

---

## Week 2 — Cognition/memory + knowledge/data (20%)

**Read** — abstracts and methods only ([RESOURCES.md](RESOURCES.md) §5)
- ReAct, Reflexion, Tree of Thoughts, Plan-and-Solve, self-consistency
- Generative Agents (memory stream: relevance + recency + importance), MemGPT, Voyager
- RAG, DPR, HyDE, Self-RAG, CRAG, GraphRAG, *Lost in the Middle*

**Know cold**: the four memory types (working / episodic / semantic / procedural) and which
agent feature maps to each; when hybrid search beats dense; what a cross-encoder reranker
does that a bi-encoder cannot.

**Build** — a RAG pipeline over ~50 of your own documents. Deliberately break it: chunk at
128 tokens with no overlap and watch procedures get severed. Then fix it with
structure-aware chunking and parent-document retrieval.

```bash
./sim.py -k agentic-ai practice -d cognition-planning-memory
./sim.py -k agentic-ai practice -d knowledge-data
```

---

## Week 3 — Evaluation and tuning (13%)

The domain most people underestimate, and the one where the questions are most diagnostic:
you are given a symptom and asked which layer is at fault.

**Read** ([RESOURCES.md](RESOURCES.md) §4)
- RAGAS metric definitions — specifically **which metrics need ground truth** (context
  recall does; faithfulness and answer relevancy do not)
- TruLens RAG triad
- LangSmith evaluation concepts — trajectory vs. final-response evaluation
- LoRA, QLoRA, DPO abstracts
- Benchmark names and what each measures: GAIA, SWE-bench, τ-bench, BFCL, MTEB, MMLU-Pro

**Know cold**: the decision table for *fine-tune vs. RAG vs. prompt vs. retrieval fix*.
Wrong terminology and style → tune. Missing or stale facts → retrieve. Wrong format →
constrain decoding. Wrong tool choice → fix tool descriptions.

**Build** — run RAGAS over last week's pipeline. Make faithfulness drop on purpose by
shrinking top-k, and confirm the metric catches it.

```bash
./sim.py -k agentic-ai practice -d evaluation-tuning
```

---

## Week 4 — Deployment/scaling + NVIDIA platform (20%)

**Read** ([RESOURCES.md](RESOURCES.md) §2)
- NIM for LLMs: what a NIM actually is, OpenAI-compatible endpoints, function calling,
  structured generation, multi-LoRA serving
- TensorRT-LLM: in-flight batching, paged KV cache, KV-cache reuse, quantization, parallelism
- Triton: multi-backend serving, ensembles, dynamic batching
- Dynamo: disaggregated prefill/decode, KV-aware routing
- NeMo component boundaries — **this is the most testable list in the track**

**Memorize the product map.** Most `NVIDIA Platform` questions are "which component for X":

| Need | Component |
|---|---|
| Serve an optimized model behind an OpenAI-compatible API | **NIM** |
| Build/run the optimized inference engine | **TensorRT-LLM** |
| Multi-framework, multi-model serving | **Triton** |
| Disaggregated prefill/decode, KV-aware routing | **Dynamo** |
| Curate/dedupe/filter training data at scale | **NeMo Curator** |
| Fine-tune (SFT/PEFT/LoRA) as a service | **NeMo Customizer** |
| Benchmarks + LLM-as-judge evaluation | **NeMo Evaluator** |
| Input/output/dialog/retrieval/execution rails | **NeMo Guardrails** |
| Extraction, embedding, reranking for RAG | **NeMo Retriever** |
| Framework-agnostic agent composition + profiling | **NeMo Agent Toolkit** |
| GPU-accelerated vector index build/search | **cuVS / RAFT** |
| Supported, patched enterprise builds | **NVIDIA AI Enterprise** |
| Reference end-to-end workflows | **AI Blueprints** |
| Hosted endpoints + free credits to try models | **build.nvidia.com** |

**Also know**: KV cache is the memory term that scales with concurrency × context; TP inside
an NVLink domain, PP across nodes; MIG partitions one GPU for small models; H200 over H100
is capacity and bandwidth, not compute.

**Build** — call a model on [build.nvidia.com](https://build.nvidia.com) with the `tools`
parameter and with a JSON schema. Free, and it makes the whole domain concrete.

```bash
./sim.py -k agentic-ai practice -d deployment-scaling
./sim.py -k agentic-ai practice -d nvidia-platform
```

---

## Week 5 — Operations, safety, oversight (15%) + first full assessment

Small weights, cheap points. These questions are mostly reasoning from first principles,
so a focused pass is enough.

**Read**
- OpenTelemetry GenAI semantic conventions
- OWASP Top 10 for LLM Applications — especially prompt injection, excessive agency,
  supply chain
- NIST AI RMF: **Govern, Map, Measure, Manage**
- EU AI Act risk tiers; know that employment/recruitment screening is high-risk
- NeMo Guardrails rail types and what each intercepts

**The recurring pattern across all three domains**: controls the model can talk its way
past are not controls. Least-privilege tool scopes, pre-execution authorization, retrieval
filters, and reversibility are. Anything enforced by a system prompt is the wrong answer.

```bash
./sim.py -k agentic-ai practice -d run-monitor-maintain
./sim.py -k agentic-ai practice -d safety-ethics-compliance
./sim.py -k agentic-ai practice -d human-ai-oversight
./sim.py -k agentic-ai exam        # full timed assessment — compare vs week 0
```

---

## Case studies

Work one whenever a domain starts to feel solid — they test whether you can hold a
situation across several questions, which standalone items do not.

```bash
./sim.py -k agentic-ai case      # pick from ten scenarios
```

## Week 6 — Consolidation

Stop reading new material. Two or three full timed assessments, drill between them, and read
the cram sheet for anything still under 75%.

```bash
./sim.py -k agentic-ai exam
./sim.py review
./sim.py -k agentic-ai flash -d nvidia-platform   # the product map is pure recall
./sim.py stats
./sim.py -k agentic-ai cheat -d <weakest domain>
```

Ship it when `./sim.py stats` shows blueprint-weighted accuracy above 80% with every domain
attempted **and** no concept below target in a 13-15% topic area. The margin over the 75% target absorbs the gap between a question bank you have
seen and one you have not.

---

## If you are also taking NCP-AAI

Everything above stands on its own — this section is only for the exam.

Book a date early: it is the only scheduling mechanism that reliably works. Then read
`./sim.py -k agentic-ai cheat -d logistics` before you book and again the night before. It
covers the Certiverse rules that fail people before they answer a question: exact name
matching, the room scan, the 14-day retake wait, and that NVIDIA returns **pass/fail with no
score** — so your last assessment here is the only diagnostic you will ever get. The
[official exam page](https://www.nvidia.com/en-us/learn/certification/agentic-ai-professional/)
has the current price and window.

Mechanics on the day:

- 120 minutes for 60–70 questions ≈ **1:45 per question**. Anything past three minutes gets
  flagged and left.
- Read the last sentence of the stem first. These questions are scenario-heavy and the
  actual ask is usually in the final clause ("...which change *most directly* addresses the
  root cause?").
- Two right answers, one *most* right: prefer the option that fixes the cause over the one
  that handles the symptom, and the structural control over the prompt-level one.
- "Select TWO" means exactly two. Partial credit is not typical.
- Distrust absolutes — *always*, *never*, *only* — in answer text. Distrust "buy the bigger
  model" as a fix for a design problem.
