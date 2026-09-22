# Six weeks of Generative AI Engineering

Roughly 6–8 hours a week. The order follows the material's own dependencies: you cannot
reason about fine-tuning before transformers, or about RAG before embeddings. Do not skip
ahead.

Every week ends with the same loop:

```bash
./sim.py -k generative-ai practice -d <topic>   # learn
./sim.py review                                 # whatever the scheduler says is due
./sim.py stats                                  # check where you actually stand
```

And every day you study at all, start with:

```bash
./sim.py review    # due questions
./sim.py flash     # due flashcards
```

That is what makes week 1's work still be there in week 6.

---

## Week 0 — baseline (1 hour)

Take a cold timed assessment before reading anything. It is meant to be uncomfortable; it
tells you which topic areas you already have and which are genuinely new.

```bash
./sim.py -k generative-ai exam
```

Write down the per-topic numbers. You will compare against them in week 6.

---

## Week 1 — Foundations (23% of the track)

*Topic areas: Introduction to AI (14%), Generative AI Introduction (9%)*

**Know cold**
- The nesting: AI ⊃ machine learning ⊃ deep learning ⊃ generative AI. Inverting this is the
  single most common error in the introductory material.
- Supervised / unsupervised / reinforcement / self-supervised, identified by the *signal
  learned from*, not by the algorithm.
- Generative vs discriminative: producing samples from a distribution versus drawing a
  boundary between classes.
- The four generative architectures and how each actually generates — GAN (generator vs
  discriminator), VAE (distribution over latents), diffusion (reverse a noising process),
  transformer (attention over sequences).
- The watsonx split: **.ai** builds and deploys, **.data** stores and queries,
  **.governance** documents risk.

**The trap**: accuracy on imbalanced data. At 97% negatives, a model that always predicts
"negative" scores 97%. Ask for precision, recall or the confusion matrix.

```bash
./sim.py -k generative-ai practice -d intro-ai
./sim.py -k generative-ai practice -d genai-intro
```

---

## Week 2 — Prompting and data preparation (18%)

*Topic areas: Prompt Engineering Basics (11%), LLM Architecture and Data Preparation (7%)*

**Read**
- Hugging Face [tokenizer summary](https://huggingface.co/docs/transformers/tokenizer_summary)
  — BPE, WordPiece, SentencePiece
- [PyTorch data loading](https://pytorch.org/docs/stable/data.html) — Dataset, DataLoader,
  `collate_fn`

**Build** — the highest-yield exercise of the week. Tokenise the same paragraph with
`BertTokenizer` and `XLNetTokenizer` and diff the output. Then write a `collate_fn` that pads
a batch of variable-length sequences and produces the attention mask. You will never again
be confused about why the two must travel together.

**Know cold**
- Zero-shot, few-shot, chain-of-thought, self-consistency, interview pattern, persona — and
  which problem each addresses.
- Prefer positive checkable instructions ("at most three sentences") over prohibitions.
- Subword tokenisation handles unseen words and keeps the vocabulary small. One token per
  word is precisely the assumption it abandons.
- A tokenizer belongs to its model. Other vocabularies produce ids that mean something else.
- Context window covers prompt *and* output, in tokens, not words.

```bash
./sim.py -k generative-ai practice -d prompt-engineering
./sim.py -k generative-ai practice -d llm-architecture
```

---

## Week 3 — Representations and transformers (21%)

*Topic areas: NLP Foundations (11%), Language Modeling with Transformers (10%)*

This is the conceptual centre of the track. Give it the most time.

**Read** — abstracts and methods only
- [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- [BERT](https://arxiv.org/abs/1810.04805)
- [word2vec](https://arxiv.org/abs/1301.3781)

**Build** — implement scaled dot-product attention in about fifteen lines of PyTorch, by
hand, without copying. Then print the attention matrix for a short sentence and look at it.
The quadratic cost stops being abstract the moment you see the N×N matrix.

**Know cold**
- Why positional encoding exists: attention is permutation-invariant.
- Query, key, value — relevance weights applied to contributions.
- Why divide by √d_k: keep softmax out of saturation.
- Encoder (bidirectional, classification) vs decoder (causal, generation). BERT vs GPT is
  masking, not "one uses attention".
- MLM and NSP, and what `[CLS]` and `[SEP]` are for.
- Static embeddings give one vector per word type and cannot separate the senses of "bank".

```bash
./sim.py -k generative-ai practice -d nlp-foundations
./sim.py -k generative-ai practice -d transformers
```

---

## Week 4 — Fine-tuning and alignment (19%)

*Topic areas: Engineering and Fine-Tuning Transformers (9%), Advanced Fine-Tuning (10%)*

**Read**
- [LoRA](https://arxiv.org/abs/2106.09685) · [DPO](https://arxiv.org/abs/2305.18290)
- [TRL docs](https://huggingface.co/docs/trl/index) — one trainer per alignment stage

**Know cold** — the intervention ladder, in order of cost:

| Problem | Fix |
|---|---|
| Wrong tone or vocabulary | Fine-tune (LoRA / SFT) |
| Missing or stale facts | Retrieval |
| Wrong output format | Constrained decoding |
| Cannot write the right answer but can judge better-vs-worse | Preference methods (DPO / RLHF) |

- LoRA freezes the base and learns two thin matrices. Rank *r* sets capacity.
- RLHF's three stages in order: SFT → reward model on pairwise preferences → PPO with a KL
  leash against a **frozen** reference.
- Why pairwise beats absolute scoring: humans are consistent about "which is better" and
  inconsistent about "how good".
- Reward hacking: high score, useless output. Hedging and padding are the classic symptoms.
- DPO removes the reward model and the RL loop by reparameterising the objective; the
  partition function cancels in the chosen-vs-rejected ratio.

```bash
./sim.py -k generative-ai practice -d finetuning
./sim.py -k generative-ai practice -d advanced-finetuning
```

---

## Week 5 — RAG, agents and the project (19%)

*Topic areas: AI Agents with RAG and LangChain (10%), Project (9%)*

**Read**
- [LangChain concepts](https://python.langchain.com/docs/concepts/) — the component vocabulary
- [DPR](https://arxiv.org/abs/2004.04906) · [RAG](https://arxiv.org/abs/2005.11401)

**Build** — a RAG pipeline over ~50 of your own documents, then break it deliberately: chunk
at 128 tokens with no overlap and watch procedures get severed. Fix it with structure-aware
chunking and overlap. That failure, felt once, is worth more than any explanation.

**Know cold**
- What happens offline (load, split, embed, index) and what happens per request (embed the
  query, retrieve, generate).
- Changing the embedding model invalidates the whole index — vectors live in *its* space.
- Topically right chunks that never contain the answer = chunking. Good retrieval with poor
  answers = generation.
- Similarity search always returns its nearest neighbours however far away. Out-of-scope
  questions need a relevance threshold.
- Deleting a source document does nothing until its chunks leave the index.
- Retrieved text is **data**, never instructions.

```bash
./sim.py -k generative-ai practice -d rag-langchain
./sim.py -k generative-ai practice -d capstone
./sim.py -k generative-ai exam        # compare against week 0
```

---

## Week 6 — Consolidation

Stop reading new material. Two or three full timed assessments, review between them, and
read the cheat sheet for anything still under 80%.

```bash
./sim.py -k generative-ai exam
./sim.py review
./sim.py flash -d transformer         # attention mechanics are pure recall
./sim.py stats
./sim.py cheat -d <weakest area>
```

You are done when `./sim.py stats` shows weighted accuracy above 85% with every topic area
attempted and no concept below target in an 11–14% area.

---

## If you are also taking the IBM certificate

This track covers the ten generative-AI courses (1–3 and 10–16), 91 of the certificate's
168 hours. Two things it deliberately does not do:

- **Courses 4–9** — Python, Flask, Pandas, scikit-learn, Keras — are out of scope. They teach
  library work that multiple choice tests poorly. The course labs are the right practice.
- **Course 16 is a build project.** The questions here cover the decisions it forces —
  chunking, embedding consistency, retrieval failure modes, index maintenance — but they are
  not a substitute for building it. Build it.

Coursera quizzes are retakeable and typically pass at 70–80%. This track targets 80% because
a retakeable quiz measures less than an unseen question. The questions here are harder and
more applied than the course quizzes; that is deliberate, but do not read a low score here as
a prediction of failing there.
