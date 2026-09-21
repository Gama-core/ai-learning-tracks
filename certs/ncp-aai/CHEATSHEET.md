# NCP-AAI cheat sheets

Condensed reference for the NVIDIA-Certified Professional: Agentic AI LLMs exam.
Generated from `cheatsheet.json` by `build_md.py` — edit the JSON, not this file.
Also available in the web simulator under **Cheat sheets**, and in the terminal via
`./sim.py cheat`.

## Contents

1. [Exam mechanics and tactics](#exam-mechanics-and-tactics) — *Read this the morning of the exam*
2. [Exam day logistics](#exam-day-logistics) — *Certiverse rules that fail people before a question is answered*
3. [NVIDIA product map](#nvidia-product-map) — *7% of the exam, highest density of memorizable fact. Learn the boundaries.*
4. [Agent architecture and design](#agent-architecture-and-design) — *15% of the exam*
5. [Agent development](#agent-development) — *15% of the exam*
6. [Cognition, planning and memory](#cognition-planning-and-memory) — *10% of the exam*
7. [Knowledge integration and data handling](#knowledge-integration-and-data-handling) — *10% of the exam*
8. [Evaluation and tuning](#evaluation-and-tuning) — *13% of the exam*
9. [Deployment and scaling](#deployment-and-scaling) — *13% of the exam*
10. [Run, monitor and maintain](#run-monitor-and-maintain) — *5% of the exam*
11. [Safety, ethics and compliance](#safety-ethics-and-compliance) — *5% of the exam*
12. [Human-AI interaction and oversight](#human-ai-interaction-and-oversight) — *5% of the exam*
13. [Acronyms](#acronyms) — *If you blank on one of these, you lose the question*

---

## Exam mechanics and tactics

*Read this the morning of the exam*

- 120 minutes, 60-70 questions. Budget 1:45 per question. Past 3 minutes, flag and move.
- Read the last sentence of the stem first. The actual ask lives in the final clause: 'most directly', 'root cause', 'least risk', 'first step'.
- Two answers will be defensible. Pick the one that fixes the cause, not the symptom; the structural control, not the prompt-level one.
- 'Select TWO' means exactly two. Partial credit is not typical.
- Scenario stems carry a constraint (latency, cost, residency, irreversibility). The constraint is usually what eliminates the runner-up.

| Distractor pattern | Why it is wrong |
|---|---|
| Add it to the system prompt | Instructions are not enforcement. Anything the model can talk past is not a control. |
| Use a bigger or better model | Capability is not a fix for a design, authorization, or data problem. |
| Increase the limit / timeout / context window | Extends the failure instead of removing it. |
| Log it and review later | Detection after an irreversible side effect. Authorize before execution. |
| Ask the model to check itself | The untrusted component becomes the security control. |
| Answers containing always, never, only, all | Agentic engineering is trade-offs; absolutes are rarely the key. |

> NVIDIA does not publish a cut score. Community reports cluster at 70-75%. Train to 80%+ so the real thing has margin.

---

## Exam day logistics

*Certiverse rules that fail people before a question is answered*

| Policy | Detail |
|---|---|
| Delivery | Online, remotely proctored via Certiverse. You create a Certiverse account to register. |
| Scoring | Pass / fail only. NVIDIA does not return a score, so you get no diagnostic feedback from a failure. |
| Retake wait | 14 days between attempts. |
| Attempt cap | At most 5 attempts per 12 months, counted from the date you first purchased the exam. |
| On passing | Digital badge plus an optional certificate. |
| Validity | 2 years from issuance. Recertify by retaking the exam. |
| Invalidation | NVIDIA may review your record and invalidate results for scoring inaccuracy, misconduct, or anomalous response patterns. |

> Pass/fail with no score is why this simulator scores you per domain. A real failure tells you nothing about where you lost it — your last mock here is the only diagnostic you will have.

| Check before booking | Requirement |
|---|---|
| ID | One unexpired government-issued photo ID. Digital IDs are not accepted. |
| Name match | The names on your Certiverse account must match your ID exactly — all given names, middle names and surnames included. |
| System test | Run the Certiverse system compatibility and network test well in advance; requirements can change between appointments, so re-check before each one. |
| Browser | Scheduled live proctored exams run under a locked-down exam browser (SEB). Admin rights on the machine help. |

| On the day | Requirement |
|---|---|
| Room scan | The proctor will have you pan the camera across the whole room, your desk surface, and the area underneath it. |
| Alone | You must be alone for the full duration, in a quiet, well-lit room. |
| Desk | Clear. No notes, no second screen, no phone, no smart watch. |
| Interruptions | Anyone entering the room can void the session. Lock the door and silence everything. |

- Check the name on your Certiverse account against your passport the day you register, not the day you sit. A mismatch is the single most common cause of a forfeited appointment.
- Run the system check on the machine and network you will actually use — not your laptop on a different Wi-Fi.
- Budget the full 120 minutes. There is no credit for finishing early, and flagged questions are worth revisiting.
- A failure costs $200 and 14 days. One more week of drilling is cheaper than one more attempt.
- Policies change. Confirm against the NVIDIA certification FAQ and Certiverse testing rules before you book.

---

## NVIDIA product map

*7% of the exam, highest density of memorizable fact. Learn the boundaries.*

| You need to... | Component |
|---|---|
| Serve an optimized model behind an OpenAI-compatible API | NIM |
| Build and run the optimized inference engine | TensorRT-LLM |
| Serve many models across many frameworks, with ensembles | Triton Inference Server |
| Disaggregate prefill from decode, route by KV cache | Dynamo |
| Curate, filter, dedupe training corpora at scale | NeMo Curator |
| Generate synthetic training or eval data | NeMo Data Designer |
| Fine-tune (SFT / PEFT / LoRA) as a managed service | NeMo Customizer |
| RL post-training in interactive tool-using environments | NeMo Gym + NeMo RL |
| Run benchmarks and LLM-as-judge evaluations | NeMo Evaluator |
| Apply input / output / dialog / retrieval / execution rails | NeMo Guardrails |
| Extract, embed, rerank documents for RAG | NeMo Retriever (NV-Ingest for extraction) |
| Compose and profile agents across frameworks | NeMo Agent Toolkit |
| GPU-accelerate vector index build and search | cuVS / RAFT (CAGRA, IVF-PQ) |
| GPU-accelerate dataframes and ETL | RAPIDS (cuDF) |
| Run a sandboxed always-on local agent | NemoClaw + OpenShell |
| Get supported, patched, certified builds on-prem | NVIDIA AI Enterprise |
| Start from a working reference workflow | AI Blueprints |
| Try models with no GPU, then self-host the winner | build.nvidia.com |

| Confusable pair | The distinction |
|---|---|
| NIM vs Triton | NIM is a packaged, versioned microservice for one model with a standard API. Triton is a general multi-model, multi-backend server. A NIM may use Triton or TensorRT-LLM inside. |
| NIM vs TensorRT-LLM | TensorRT-LLM builds and runs the engine. NIM wraps an optimized engine plus runtime and API into a deployable container. |
| Curator vs Customizer vs Evaluator | Data in, weights changed, quality measured. Curate, then customize, then evaluate. |
| Retriever vs a vector database | Retriever provides extraction, embedding and reranking microservices. The index itself is Milvus, Elasticsearch, pgvector, etc. |
| Guardrails vs authorization | Guardrails filter natural language. Authorization decides whether a tool call may execute. Never substitute one for the other. |

| Nemotron 3 | Fact |
|---|---|
| Sizes | Nano, Super, Ultra — one family, so a model cascade shares prompting behavior and toolchain |
| Architecture | Hybrid Mamba-Transformer mixture-of-experts; Mamba layers scale linearly with length, attention layers keep precise recall |
| MoE economics | Roughly a tenth of parameters active per token: compute like a small model, memory capacity sized by total parameters |
| Context | Native 1M tokens |
| Techniques | NVFP4 4-bit float training, multi-token prediction (MTP) for decode throughput, RL post-training via NeMo Gym |
| License | NVIDIA Open Model License — open weights, commercial use under its terms, not a permissive OSI license |

| Hardware | What it buys |
|---|---|
| H100 (80GB) vs H200 (141GB) | Same Hopper compute; H200 adds HBM capacity and bandwidth = bigger KV cache, more concurrency, longer context per GPU |
| NVLink / NVSwitch | High-bandwidth GPU interconnect. Tensor parallelism all-reduces every layer, so TP stays inside an NVLink domain |
| MIG | Partitions ONE GPU into isolated instances. For co-hosting small models (embedder, reranker, guardrail) with QoS |
| Blackwell / GB200 | FP4 arithmetic; Grace-based superchips add tightly coupled CPU |

---

## Agent architecture and design

*15% of the exam*

> Workflow vs agent: in a workflow, code owns control flow. In an agent, the model chooses actions and when to stop. Model count, retrieval and hardware are irrelevant to the distinction.

| Pattern | Use when |
|---|---|
| Prompt chaining | Fixed sequence, each step's output feeds the next |
| Routing | Distinct input classes need different handling or different models |
| Parallelization (fan-out / map-reduce) | Independent subtasks; wall-clock becomes the slowest branch |
| Orchestrator-worker (supervisor) | A coordinator decides who works next and when the task is done |
| Evaluator-optimizer (reflection) | Clear, checkable criteria exist and a critique can drive revision |
| State machine / graph | The control flow is known in advance and must not be left to the model |
| ReAct loop | The path is genuinely unknown and must adapt to observations |

| Symptom | Architectural fix |
|---|---|
| Model skips a required step or repeats a side effect | Encode the order in a graph; make the side-effecting node terminal and idempotent |
| Agents ping-pong a task until the step limit | Disjoint responsibilities, explicit termination condition, escalation path |
| Tool-selection accuracy falls as tools are added | Partition tools behind sub-agents, or retrieve a candidate subset per turn |
| A flaky dependency aborts whole runs | Bounded retries, circuit breaker, documented degraded path |
| Inter-agent handoffs parse inconsistently | Typed message contract validated at each boundary |
| Cost dominated by easy traffic | Router / cascade: small model for simple intents, large for hard reasoning |
| Long job dies on pod restart | Durable checkpointing per step, keyed by thread id |
| Cross-department questions fail | Add decomposition and synthesis, not just routing |

| Protocol | Boundary it standardizes |
|---|---|
| MCP (Model Context Protocol) | Agent to tools, resources and prompts. Servers expose, clients discover and invoke. |
| A2A (Agent2Agent) | Agent to agent. Capability discovery via agent cards, task delegation between opaque peers. |

- Multi-agent is justified by genuinely different tools, context or permissions, or by real parallelism. Not by a long prompt and not by org structure.
- Privilege separation must be structural: a separate least-privilege service with its own credentials, reachable only from a validated step.
- Model-generated code runs in a sandbox with no credentials, no egress, minimal mounts, and hard CPU/memory/time limits.
- Hard real-time paths (sub-second) do not contain LLM loops. Fast tier decides; agentic tier investigates asynchronously.

---

## Agent development

*15% of the exam*

| Structured output, weakest to strongest | Guarantee |
|---|---|
| Prompt: respond only in JSON | None |
| Few-shot examples of the format | Better, still probabilistic |
| Post-hoc regex extraction or LLM repair | Reduces failures after the fact |
| Schema validation with a structured error returned to the model | Catches every violation, costs a turn |
| Constrained / guided decoding against a JSON schema or grammar | Malformed output becomes structurally impossible |

- Tools should be narrow, typed and intention-revealing: get_employee_pto_balance(employee_id, as_of_date), not run_sql(query) or hr_tool(action, params).
- Tool descriptions are prompt surface. State what it returns, when to use it, and when NOT to. Vague descriptions cause over-invocation.
- Enumerate allowed values in the schema rather than describing them in prose — guided decoding can then only emit valid ones.
- Tool errors are prompt input: name the invalid field, the constraint, and a valid example. Never return raw stack traces or silent empty results.
- Hallucinated tool name: return an error listing the valid tool names. Never fuzzy-match to the nearest one.
- Safe retry needs idempotency: a caller-supplied idempotency key, or an operation that is naturally idempotent (set-to-value, not increment-by).
- Destructive tools need a dry-run returning affected counts, an explicit confirmation parameter, and a server-side cap on blast radius.
- Tool output is prompt input: project responses down to needed fields, paginate explicitly, never dump 900-line documents into context.
- Aggregate questions over tabular data are computation, not retrieval. Expose filter/aggregate tools; embeddings cannot compute a sum.
- Global rate limits need shared state (distributed token bucket) or a queue with backpressure. Per-process counters multiply the limit by replica count.

| Test layer | What belongs there |
|---|---|
| Unit / CI (fast, hermetic, deterministic) | Stubbed model responses asserting exact tool calls and arguments; schema contract tests for every tool |
| Integration | Recorded/replayed tool fixtures; trajectory and state-transition assertions |
| Scheduled evaluation | LLM-as-judge quality, RAG metrics, benchmark suites, trend tracking |
| Production | Sampled automated proxies plus a human-reviewed slice |

> Temperature 0 is not reproducibility. Batch composition, kernels and model versions all shift results. Determinism comes from stubs and fixtures, not sampling settings.

---

## Cognition, planning and memory

*10% of the exam*

| Pattern | What it does |
|---|---|
| Chain-of-Thought | Intermediate reasoning steps before the answer |
| Self-consistency | Sample several chains at non-zero temperature, take the majority answer |
| ReAct | Interleave Thought, Action, Observation — reasoning conditions the next action |
| Reflexion | Verbal self-feedback on failure, stored in memory, conditioning the retry. No weight updates. |
| Tree of Thoughts | Search over partial solutions with state evaluation and backtracking |
| Least-to-Most | Explicitly decompose into ordered sub-problems, solve in dependency order |
| Plan-and-Execute | One planning call, then cheap execution. Fewer expensive calls than ReAct, less adaptive. |
| Plan-Act-Replan | Plan to the next decision point, execute, re-plan on new observations |

| Memory type | Holds | Example |
|---|---|---|
| Working / short-term | Current context, bounded by the window | The live conversation |
| Episodic | Specific past events and attempts | What was tried and what happened |
| Semantic | Facts and concepts | User preferences, domain facts |
| Procedural | How-to knowledge, reusable skills | Voyager-style skill library |
| Parametric | Knowledge in the weights | Fixed at training, uncitable, no update path |

- Good compaction is selective, not positional: summarize narrative history, keep verbatim the goal, open sub-tasks, exact identifiers and recent observations.
- Memory quality is decided at WRITE time. Store durable, future-relevant facts, not raw turns, with a supersession rule so new facts invalidate contradicting old ones.
- Retrieval scoring on relevance alone surfaces stale memories. Generative-agents scoring = relevance + recency + importance.
- Repeating a failed strategy means no accessible attempt log. That is an episodic-memory gap, not a context-size problem.
- Re-planning is event-driven: an invalidated assumption, a step failure, or new information. Not a fixed cadence.
- Reasoning-model thinking budgets have diminishing returns. Tune per task class; easy tasks gain nothing and pay latency.
- Self-written memory compounds errors: a wrong inference stored as fact is retrieved and reinforced. Tag confidence, keep provenance, allow expiry.
- CoT traces are not a faithful account of the model's computation. A fluent chain can rationalize a wrong answer — weak evidence for reviewers.

---

## Knowledge integration and data handling

*10% of the exam*

| Symptom | Layer at fault | Fix |
|---|---|---|
| Topically right chunks that truncate the answer | Chunking | Structure-aware splits, overlap, parent-document retrieval |
| Exact codes and SKUs not found | Dense-only retrieval | Add lexical BM25, fuse scores — hybrid search |
| Unrelated topics returned | Embedding or query | Query rewriting, HyDE, multi-query expansion |
| Right documents, wrong ordering | Ranking | Cross-encoder reranker over a shortlist |
| Multi-hop question fails | Flat top-k retrieval | GraphRAG: entities and relations, traversal |
| Answers from superseded documents | Governance | Effective-date metadata, query-time filters, tombstone old versions |
| Answer faithful but misses caveats | Context assembly / prompt | Stop truncating qualifications; ask for limitations explicitly |
| Top-k full of near-duplicates | Ingestion | Dedupe at ingest, diversity-aware selection (MMR) |

| Component | Role |
|---|---|
| Bi-encoder (embedding) | Encodes query and document independently; enables precomputed indexes and fast ANN search |
| Cross-encoder (reranker) | Attends over the pair jointly; far better relevance, far higher per-pair cost. Retrieve broad, rerank a shortlist. |
| HNSW index | High recall at low latency; large memory, costly updates |
| IVF-PQ index | Quantized codes, much smaller memory, some recall loss. Use when the set outgrows RAM. |
| Pre-filtering vs post-filtering | Pre-filter constrains the search itself. Post-filter retrieves then discards — a selective filter silently returns almost nothing. |

| RAG variant | Idea |
|---|---|
| Self-RAG | Decide whether to retrieve; critique and grade what comes back |
| Corrective RAG (CRAG) | Grade retrieved documents; rewrite or fall back when retrieval is poor |
| HyDE | Embed a hypothetical answer document instead of the raw question |
| RAPTOR | Recursive clustering and summarization into a tree; serve detail or synthesis by question scope |
| GraphRAG | Extract entities and relations so multi-hop links are traversable |

- Lost in the middle: models use content at the start and end of long context more reliably. Rank matters; put the best passages at the edges.
- Handle PII at ingestion — redact or tokenize before embedding. Output filtering is defense in depth, not the primary control.
- Multi-tenant retrieval: enforce tenant and per-user document permissions INSIDE the query, server-side, before anything enters the prompt.
- Changing the embedding model invalidates the whole index. Generators swap freely; embedders do not.
- Scanned PDFs and tables need layout-aware multimodal extraction (OCR, table structure, figure captions). Text-only extraction discards the answer.
- Time-series and telemetry are range and aggregate queries, not similarity. Use a time-series store behind query tools.
- GDPR erasure: index entries and sources delete deterministically; fine-tuned weights generally require retraining. Keep personal data out of training sets.

---

## Evaluation and tuning

*13% of the exam*

| Metric | Compares | Needs ground truth? |
|---|---|---|
| Faithfulness / groundedness | Answer vs retrieved context | No |
| Answer relevancy | Answer vs question | No |
| Context precision | Ranking of relevant chunks in what was retrieved | Usually yes |
| Context recall | Retrieved context vs the reference answer's claims | Yes |
| Context relevance | Retrieved context vs question | No |

> TruLens RAG triad = context relevance, groundedness, answer relevance. Failing one localizes the defect to retrieval, grounding, or response targeting.

| Failure | What it points at |
|---|---|
| Correct answer, 11 tool calls instead of 3 | Trajectory evaluation, not outcome evaluation |
| Right tool chosen, tool output insufficient | Tool or data capability gap, not reasoning |
| Malformed tool arguments | Schema and prompting |
| Retrieved context lacks the answer entirely | Retrieval — no amount of generator tuning fixes it |
| 84% overall, one task type at 50% | Aggregate hiding a segment. Always disaggregate. |
| 91% offline, 68% in production | Stale eval set plus overfitting to it |

| Problem | Intervention |
|---|---|
| Wrong terminology or style | Fine-tune (LoRA / SFT) |
| Missing, stale or company-specific facts | Retrieval |
| Wrong output format | Constrained decoding |
| Wrong tool chosen | Tool descriptions and schemas |
| Preference alignment | DPO (direct from preference pairs, no reward model, no RL rollouts) or RLHF |
| Agentic tool-use behavior | RL post-training in interactive environments (NeMo Gym) |

- LLM-as-judge: give an anchored rubric, require reasoning before the score, and validate against human labels before trusting it at scale. Do not reuse the generator model and prompt — self-preference bias.
- For open-ended comparison use pairwise preference with randomized position, not absolute 1-10 scores.
- A 4% lift on 60 examples is roughly two examples. Check run-to-run variance before believing it.
- Eval sets earn value from realism and difficulty: mine production failures and escalations, and keep an adversarial slice. Self-generated data inherits your blind spots.
- Report the adversarial slice and the high-consequence slice separately — they need different thresholds.
- pass@k high with pass@1 low means a selection problem: add self-consistency, verification or reranking, not a bigger model.
- Quantized models must be re-evaluated on the capabilities you depend on. Aggregate benchmarks hide damage to schema conformance.
- Catastrophic forgetting after narrow fine-tuning: mix in general instruction replay data, lower rank and learning rate.

| Benchmark | Measures |
|---|---|
| BFCL | Function-calling: selection, arguments, parallel calls, knowing when NOT to call |
| GAIA | General assistant tasks requiring tools and multi-step reasoning |
| SWE-bench | Real repository issue resolution |
| tau-bench | Tool-agent-user interaction with domain policies |
| WebArena / AgentBench | Web and multi-environment agent tasks |
| MTEB | Embedding and reranking quality |
| MMLU-Pro | Knowledge and reasoning |
| CLASSic (Aisera, NOT NVIDIA) | Cost, Latency, Accuracy, Stability, Security |

---

## Deployment and scaling

*13% of the exam*

| Metric | Means | Driven by |
|---|---|---|
| TTFT | Time to first token | Prefill — prompt length, queueing |
| TPOT / ITL | Inter-token latency per user | Decode — memory bandwidth, batch size |
| Throughput | Aggregate tokens/sec across users | Batching efficiency, GPU utilization |
| Goodput | Throughput that meets the latency SLO | The number that actually matters |

> Interactive agents: TTFT and TPOT are the SLOs. Aggregate throughput and GPU utilization can look excellent while every user waits.

| Technique | What it fixes |
|---|---|
| Continuous / in-flight batching | Static batching wastes cycles waiting for the longest sequence |
| PagedAttention | KV cache fragmentation and over-reservation; enables prefix sharing |
| Prefix KV-cache reuse | Repeated prefill of an identical system prompt and tool catalog |
| Chunked prefill + priority scheduling | One huge prefill blocking short requests (head-of-line blocking) |
| Speculative decoding / MTP | Decode latency — draft proposes, target verifies several tokens per pass |
| Quantization (INT8, INT4, FP8, NVFP4) | Weight memory and bandwidth; re-evaluate precision-critical behavior |
| Disaggregated serving (Dynamo) | Prefill is compute-bound, decode is bandwidth-bound; stop making them share |
| Multi-LoRA | N fine-tuned variants without N full deployments |

| Parallelism | Splits | Use |
|---|---|---|
| Tensor (TP) | Individual layers across GPUs | Fit a large model with low latency; keep inside NVLink |
| Pipeline (PP) | Layer groups across stages | Across nodes; adds bubble overhead |
| Expert (EP) | MoE experts across GPUs | MoE models only |
| Data (DP) | Replicas of the whole model | Throughput scaling, not fitting |

- KV cache is the memory term that scales with batch x sequence length x layers. At long context it exceeds the weights and causes the OOM.
- MoE sizing: compute like the active fraction, memory like the total. Every expert must be resident.
- Autoscale on queue depth, pending requests or GPU metrics. CPU utilization is blind to a GPU-bound server.
- Kubernetes: startup probes generous enough for weight loading, explicit GPU requests and node selectors, images and weights cached locally.
- Bursty traffic: warm baseline replicas + fast scale-out beats scale-to-zero with a 4-minute cold start.
- Session affinity or KV-aware routing keeps multi-turn conversations on the replica that holds their prefix cache.
- TensorRT-LLM engines are specific to model, precision and GPU architecture. New hardware means a rebuild.
- Load tests that stub the tools measure only the inference tier and overstate capacity.
- Self-hosting buys data residency and version control. It is not automatically cheaper — that depends on utilization.

---

## Run, monitor and maintain

*5% of the exam*

- Trace structure: a root span per task, child spans per LLM call, tool call and retrieval, each carrying model, token counts, latency and status. Flat logs lose the causal tree.
- OpenTelemetry GenAI semantic conventions standardize span names and attributes so traces are portable across vendors.
- Agent-specific telemetry a plain API does not have: per-step token consumption and cost per task; tool-call counts and error rates; step counts including runs that hit the limit.
- Leading indicators of degradation: rising step-limit terminations, rising tool-error and retry rates. Both precede user complaints.
- Slow quality decline with a frozen stack means drift — the traffic and the corpus moved, not the code.
- Version together: code, prompts, tool schemas, model version, index snapshot, guardrail config. Any one alone is insufficient to reproduce a decision.
- Pin model versions. A floating latest alias means behavior changes with no change on your side.
- Incident method: correlate the sharp time boundary against the change and dependency timeline, then diff traces either side of it. Do not roll back blindly.
- Strict parsing at tool boundaries: error on unexpected or missing fields rather than defaulting to null. Silent nulls make agents confidently wrong.
- Trace payloads contain prompts and tool arguments — that is a sensitive datastore. Redact at capture, restrict access, set retention.
- Canary: small percentage, same traffic mix, compare task success + tool-error rate + cost per task + latency against control, hold long enough to see real variety.

| SLI | Agentic version |
|---|---|
| Success rate | Task success against a defined acceptance criterion, not HTTP 200 |
| Latency | p95 end-to-end task completion across the whole trajectory |
| Cost | Cost per completed task, split prompt vs completion tokens |
| Efficiency | Steps and tool calls per task; rate of step-limit terminations |

---

## Safety, ethics and compliance

*5% of the exam*

| NeMo Guardrails rail | Intercepts |
|---|---|
| Input rails | User messages before the model sees them |
| Retrieval rails | Retrieved chunks before they enter the prompt — key defense against indirect injection |
| Dialog rails | Conversation flow and topic boundaries (Colang) |
| Execution rails | Custom actions and tool invocation |
| Output rails | Generated responses before the user sees them |

> Output filtering protects what the user sees, not what the system did. An agent that already sent the money has caused the harm. Consequential actions need PRE-execution authorization.

| Threat | Control |
|---|---|
| Direct prompt injection | Input rails, but assume bypass — bound consequences at the tool layer |
| Indirect injection (documents, web pages, image text) | Treat retrieved and extracted content as untrusted DATA: fence it, label it, never promote it into the system prompt |
| Tool poisoning / supply chain | Pin and review tool definitions, verify server provenance, alert on metadata changes |
| Knowledge-base poisoning | Moderate contributions, track provenance, filter at the retrieval rail |
| Excessive agency | Least-privilege credentials + orchestrator-enforced approval for irreversible actions |
| Confused deputy | Act with the requesting user's authority, not the agent's service credentials |
| Data exfiltration | Scope tools to allowlists, proxy egress, no ambient credentials |
| Jailbreak | Classifier + output checks + tool authorization. Detection alone always has false negatives. |

| Framework | Structure |
|---|---|
| NIST AI RMF | Govern, Map, Measure, Manage (NOT Identify/Protect/Detect/Respond — that is the Cybersecurity Framework) |
| EU AI Act | Risk tiers: prohibited, high-risk, limited (transparency), minimal. Employment and recruitment screening is HIGH-RISK. |
| EU AI Act transparency | People must be told they are interacting with an AI unless obvious — applies regardless of risk tier |
| GDPR | Purpose limitation, data minimization, storage limitation. Applies to trace stores too. |
| OWASP LLM Top 10 | Prompt injection, insecure output handling, supply chain, excessive agency, sensitive information disclosure |
| MITRE ATLAS | Adversarial ML threat matrix |

- Auditability needs the full trajectory: inputs, retrieved sources with versions, every tool call and result, model and prompt versions, guardrail decisions, human approvals.
- Bias detection requires disaggregated metrics by group plus counterfactual tests varying only group-correlated attributes. Aggregate accuracy hides disparate impact, and removing explicit demographic fields does not remove proxies.

---

## Human-AI interaction and oversight

*5% of the exam*

| Model | Human role |
|---|---|
| Human IN the loop | Approves before the system proceeds — blocking. For irreversible or high-consequence actions. |
| Human ON the loop | Monitors and can intervene while the system proceeds. For high-volume, reversible actions. |
| Human OUT of the loop | Fully autonomous. Requires measured reliability on that specific action and input distribution. |

> Autonomy is set by potential harm x irreversibility, weighed against measured reliability on that specific action. Not by frequency, duration, or whether the API is internal.

- Rubber-stamping is the default failure of oversight. 40 pending items at 4 seconds each is oversight theater — accountability without control.
- Reduce automation bias: show the evidence BEFORE the recommendation, make rejection as cheap as approval, capture the reason. Do not pre-select the agent's choice or lead with a confidence score.
- Reviewers need two things: the evidence with links to source versions, and a precise statement of what will happen if approved, including reversibility.
- Escalate on verifiable signals — no relevant evidence retrieved, tool failures or conflicts, disagreement across repeated samples, out-of-scope match. Model self-reported confidence is poorly calibrated.
- Recoverability limits harm better than logging: a defined compensating action per operation, the before-state captured at execution, and a window before finality.
- Handoff package: user goal, actions already taken, evidence gathered, what failed, and the specific reason for escalation. Raw transcripts force reconstruction.
- Clarifying questions name the ambiguity, list the options, and state what each answer will do.
- Reviewer decisions are noisy labeled data: analyze patterns and fix prompts, tools or retrieval, add cases to the regression suite, and only then consider preference tuning.
- User-facing transparency: disclose it is an AI, cite sources for factual claims, provide a route to a human. Not parameter counts or the system prompt.
- Handoff health metrics: time for the human to decide, and how often they must re-gather context the agent already had.

---

## Acronyms

*If you blank on one of these, you lose the question*

| Term | Expansion / meaning |
|---|---|
| A2A | Agent2Agent protocol — agent-to-agent delegation |
| BFCL | Berkeley Function-Calling Leaderboard |
| CAGRA | GPU graph-based ANN index in cuVS |
| CoT / ToT | Chain-of-Thought / Tree of Thoughts |
| CRAG | Corrective RAG |
| DPO | Direct Preference Optimization — policy from preference pairs, no reward model |
| HITL / HOTL | Human in / on the loop |
| HNSW | Hierarchical Navigable Small World — graph ANN index |
| HyDE | Hypothetical Document Embeddings |
| ITL / TPOT | Inter-token latency / time per output token |
| IVF-PQ | Inverted File with Product Quantization — compressed ANN index |
| KV cache | Cached attention keys and values; scales with batch x length x layers |
| LoRA / QLoRA / PEFT | Low-Rank Adaptation / quantized LoRA / parameter-efficient fine-tuning |
| MCP | Model Context Protocol — agent-to-tool standard |
| MIG | Multi-Instance GPU — partitions one GPU into isolated instances |
| MMR | Maximal Marginal Relevance — diversity-aware selection |
| MoE | Mixture of Experts |
| MTP | Multi-token prediction |
| NIM | NVIDIA Inference Microservice |
| NVFP4 | NVIDIA 4-bit floating-point format |
| PEFT | Parameter-efficient fine-tuning |
| RAG | Retrieval-Augmented Generation |
| ReAct | Reason + Act — Thought / Action / Observation loop |
| RLHF | Reinforcement Learning from Human Feedback |
| SFT | Supervised fine-tuning |
| SLO / SLI | Service level objective / indicator |
| TP / PP / EP / DP | Tensor / pipeline / expert / data parallelism |
| TTFT | Time to first token |
