# IBM Gen AI Engineering cheat sheets

Condensed reference for the NVIDIA-Certified Professional: Agentic AI LLMs exam.
Generated from `cheatsheet.json` by `build_md.py` — edit the JSON, not this file.
Also available in the web simulator under **Cheat sheets**, and in the terminal via
`./sim.py cheat`.

## Contents

1. [How to work this certificate](#how-to-work-this-certificate) — *Read before you start course 1*
2. [Foundations and terminology](#foundations-and-terminology) — *Courses 1-2 · 23% of the covered hours*
3. [Prompt engineering](#prompt-engineering) — *Course 3 · 11%*
4. [Tokenisation and data pipelines](#tokenisation-and-data-pipelines) — *Course 10 · 7%*
5. [Representations and sequence models](#representations-and-sequence-models) — *Course 11 · 11%*
6. [Transformer architecture](#transformer-architecture) — *Course 12 · 10%*
7. [Fine-tuning](#fine-tuning) — *Course 13 · 9%*
8. [Alignment: RLHF and DPO](#alignment:-rlhf-and-dpo) — *Course 14 · 10%*
9. [RAG, agents and LangChain](#rag-agents-and-langchain) — *Courses 15-16 · 19%*
10. [Acronyms](#acronyms) — *Blank on one of these and you lose the question*

---

## How to work this certificate

*Read before you start course 1*

- 168 hours across 16 courses, self-paced. This bank covers the 10 generative-AI courses (1-3, 10-16), 91 hours.
- There is no cumulative exam. Each course has module quizzes you can retake, plus a capstone build project.
- Because quizzes are retakeable, passing one proves less than answering an unseen question. That is what this bank is for.
- Courses 10-16 build strictly on each other: tokenisation, then embeddings, then attention, then fine-tuning, then alignment, then RAG. Do not skip ahead.
- The capstone cannot be simulated. Build it. Everything before it is preparation for that.

| Trap | Why it catches people |
|---|---|
| Confusing the AI / ML / DL / gen-AI nesting | Asked constantly in course 1, and the hierarchy is easy to invert under time pressure |
| Mixing up encoder and decoder roles | BERT and GPT differ by masking, not by 'one uses attention' |
| Treating a tokenizer as interchangeable | Token ids only mean something relative to the vocabulary that produced them |
| Assuming RAG and fine-tuning are alternatives for the same problem | They solve different problems: facts versus behaviour |
| Thinking prompt engineering changes the model | It changes nothing; weights are fixed at inference |

---

## Foundations and terminology

*Courses 1-2 · 23% of the covered hours*

| Term | Meaning |
|---|---|
| AI | Any technique making machines appear intelligent. The outermost set. |
| Machine learning | Subset of AI that learns patterns from data instead of hand-written rules |
| Deep learning | Subset of ML using multi-layer neural networks |
| Generative AI | Subset of deep learning that produces new content |
| Narrow AI | Performs one defined task. Everything in production today. |
| General AI | Human-breadth understanding across arbitrary domains. Does not exist. |
| Foundation model | Trained broadly at scale, then adapted to many downstream tasks |

| Learning type | Signal it learns from |
|---|---|
| Supervised | Labelled examples: input paired with the correct answer |
| Unsupervised | Structure in unlabelled data (clustering, dimensionality reduction) |
| Reinforcement | Rewards and penalties following actions in an environment |
| Self-supervised | Labels derived from the data itself, e.g. predict the masked or next token |

| Generative architecture | How it generates |
|---|---|
| GAN | Generator versus discriminator; the discriminator's judgement trains the generator |
| VAE | Encodes to a distribution over latent space, so sampling it decodes to new data |
| Diffusion | Learns to reverse a noising process; denoises from pure noise, iteratively |
| Transformer | Attention over sequences; the basis of nearly every modern LLM |

| watsonx component | Job |
|---|---|
| watsonx.ai | Studio to train, validate, tune and deploy models including foundation models |
| watsonx.data | Lakehouse for storing and querying the data models use |
| watsonx.governance | Model risk documentation, drift monitoring, compliance and audit |

> Accuracy on imbalanced data is a trap: at 97% negatives, a model that always predicts 'negative' scores 97%. Ask for precision, recall or the confusion matrix.

---

## Prompt engineering

*Course 3 · 11%*

| Technique | Use when |
|---|---|
| Zero-shot | The task is common and the instruction alone carries it |
| Few-shot | The format or style is easier to demonstrate than to describe |
| Chain-of-thought | The answer depends on multiple reasoning steps (arithmetic, logic) |
| Self-consistency | One correct answer exists; sample several chains and take the majority |
| Interview pattern | The model questions you to gather requirements before producing output |
| Persona | Tone, register and vocabulary need shaping. Confers no actual expertise. |

- A good prompt fixes: task, context, audience, format, length and tone. 'Make it good' instructs nothing.
- Prefer positive checkable instructions ('at most three sentences') over prohibitions ('do not be verbose').
- Delimit user-supplied and retrieved content. It marks the trust boundary as well as the subject.
- Temperature scales the sampling distribution: low for extraction and structure, higher for ideation.
- Few-shot examples teach everything they share, including properties you did not intend. Vary what should vary.
- In long inputs, restate hard constraints near the content they govern; attention to the middle degrades.
- Evaluate a prompt change on a fixed set of inputs, not on one output you happened to like.

> In-context learning: the model adapts to examples in the prompt without any weight change. It lasts only for that request, which is exactly why RAG works.

---

## Tokenisation and data pipelines

*Course 10 · 7%*

| Tool | What it is for |
|---|---|
| NLTK / spaCy | General linguistic tooling: sentence and word segmentation, stemming, stop words |
| BertTokenizer | WordPiece subword tokenisation matching BERT's vocabulary |
| XLNetTokenizer | SentencePiece tokenisation with XLNet's own vocabulary and special tokens |
| torch Dataset | Defines __len__ and __getitem__: how many items and how to fetch item i |
| torch DataLoader | Batching, shuffling and parallel loading over a Dataset |
| collate_fn | Decides how a list of samples becomes one batched tensor — pads variable lengths |

- Always pair a model with its own tokenizer. Other vocabularies produce ids that mean something else.
- Subword tokenisation handles unseen words by composing known fragments and keeps the vocabulary small. One token per word is exactly the assumption it abandons.
- Pad per batch, not across the dataset; padding to the global maximum wastes compute.
- An attention mask tells the model which positions are padding. Omit it and output depends on batch composition.
- Load lazily in __getitem__ so memory scales with batch size, not corpus size.
- Context window covers prompt and output together, measured in tokens, not words.

---

## Representations and sequence models

*Course 11 · 11%*

| Representation | Property |
|---|---|
| One-hot | Orthogonal: every word equidistant from every other. Length of the vocabulary. |
| Bag of words | Counts only; word order and syntax discarded |
| Static embeddings (word2vec, GloVe) | One dense vector per word type. Cannot separate senses of 'bank'. |
| Contextual embeddings (BERT) | A different vector per occurrence, computed from surrounding text |

| word2vec variant | Prediction direction |
|---|---|
| Skip-gram | Target word -> context words. More signal per occurrence; better on rare words. |
| CBOW | Context words -> target word. Faster to train. |

| Concept | Detail |
|---|---|
| N-gram model | Next word from the previous N-1. Cannot see beyond the window. |
| RNN limits | Vanishing/exploding gradients over long sequences; computation is inherently sequential |
| LSTM / GRU | Gating shortens the gradient path across time. Keeps the sequential bottleneck. |
| Seq2seq | Encoder builds a representation; decoder generates conditioned on it |
| Teacher forcing | Feed ground-truth previous token in training. Causes exposure bias at inference. |
| Autoregressive | Each token conditioned on those already produced. N tokens ≈ N forward passes. |
| Perplexity | Exponentiated average negative log-likelihood. Lower = less surprised by held-out text. |
| BLEU / ROUGE | N-gram overlap with references. Punish valid paraphrase; reward copied wording. |

---

## Transformer architecture

*Course 12 · 10%*

| Component | Purpose |
|---|---|
| Positional encoding | Attention is permutation-invariant; this injects word order |
| Query / Key / Value | Query·Key gives relevance weights; those weights average the Values |
| Scaling by sqrt(d_k) | Keeps dot-product variance stable so softmax does not saturate |
| Multi-head attention | Parallel heads in different subspaces capture different relationship types |
| Causal mask | Stops a position attending to later ones, so the decoder cannot read the answer |
| Cross-attention | Decoder queries against encoder keys and values (translation) |
| Residual connection | Direct gradient path around each sublayer; makes deep stacks trainable |
| Layer normalisation | Normalises within one example's features, independent of batch size |
| Position-wise FFN | Attention moves information between positions; this transforms within one |

| Model | Stack | Pretraining objective |
|---|---|---|
| BERT | Encoder | Masked language modelling (~15% masked) + next sentence prediction |
| GPT | Decoder | Causal next-token prediction |
| T5 / BART | Encoder-decoder | Span corruption / denoising |

| BERT special token | Role |
|---|---|
| [CLS] | First position; its output serves as the sequence-level representation |
| [SEP] | Separates segments and marks the end of a sequence |
| [MASK] | Marks tokens to be predicted during MLM |
| [PAD] | Fills to a common batch length; excluded by the attention mask |

> Self-attention costs scale with the square of sequence length: one score per pair of positions. That single fact drives the whole long-context research agenda.

---

## Fine-tuning

*Course 13 · 9%*

| Approach | What it updates | When |
|---|---|---|
| Prompting | Nothing | Always try first. Instant, free, reversible. |
| Feature extraction | A new head only; backbone frozen | Small datasets; fast; resists overfitting |
| Full fine-tuning | All weights | Enough data and compute; strongest adaptation |
| LoRA | Small low-rank matrices added to chosen weights | Most of the gain, a fraction of the memory |

- LoRA freezes the base and learns two thin matrices whose product is the weight update. Rank r sets capacity: higher r adapts more and overfits small data sooner.
- Because the base is untouched, many adapters share one loaded model at serving time. QLoRA adds 4-bit quantisation of the base.
- Fine-tuning learning rates are small (roughly 1e-5 to 5e-5). Rates suited to random initialisation destroy the pretrained representation.
- Replace the pretrained head: it predicts the pretraining objective's output space, not your labels.
- OOM during training: reduce per-device batch size, then restore the effective batch with gradient accumulation.
- Catastrophic forgetting after narrow tuning: mix general data back in, lower the learning rate, train fewer epochs.
- Training loss falling while validation loss rises means stop — that is overfitting, not progress.
- model.eval() switches dropout off and normalisation to running statistics. torch.no_grad() is separate.

---

## Alignment: RLHF and DPO

*Course 14 · 10%*

| Stage | What happens |
|---|---|
| 1. Supervised fine-tuning | Train on demonstrations so the model responds sensibly at all |
| 2. Reward modelling | Train a scorer on pairwise human preferences between responses |
| 3. Policy optimisation | PPO improves the policy against the reward model, with a KL leash |

| Term | Meaning |
|---|---|
| Policy | The model's conditional distribution over next tokens: state = context, action = token |
| Reward model | Scores a response to correlate with human preference. Never generates. |
| Pairwise preference | 'Which of these two is better' — far less noisy than absolute ratings |
| KL penalty | Keeps the policy near the frozen reference, preventing reward hacking |
| Proximal (in PPO) | Clipped objective stops any single update moving the policy far |
| Reward hacking | High reward-model score, useless output. Hedging and padding are classic symptoms. |
| DPO | Reparameterises the objective so preferences update the policy directly |
| Partition function | The intractable normaliser; cancels in DPO's chosen-vs-rejected ratio |

> PPO needs policy, frozen reference and reward model resident at once. That memory cost is much of why DPO became popular — it needs neither the reward model nor the RL loop.

- TRL provides SFTTrainer, RewardTrainer, PPOTrainer and DPOTrainer, one per stage.
- The reference model is frozen so the KL term has a fixed anchor; if it moved, drift would be unbounded.
- Hold out preference data the optimiser never sees, or rising reward is indistinguishable from memorisation.
- Climb the ladder in order: prompt, then SFT on demonstrations, then preference methods only when you can judge better-versus-worse but cannot write the right answer.

---

## RAG, agents and LangChain

*Courses 15-16 · 19%*

| Stage | Happens when |
|---|---|
| Load documents | Offline. Loaders normalise PDF/HTML/CSV into Documents with metadata. |
| Split into chunks | Offline. Size and overlap decide whether a passage holds a whole answer. |
| Embed and index | Offline. Vectors live in the embedding model's space. |
| Embed the query | Per request, with the same embedding model |
| Retrieve top-k | Per request. Trades recall against noise and prompt cost. |
| Generate | Per request, conditioned on the retrieved passages |

| LangChain component | Role |
|---|---|
| Document loader | Reads a source format into Documents with metadata |
| Text splitter | Chunks documents; chunk_size and chunk_overlap are the levers |
| Prompt template | Parameterised prompt with named variables |
| Example selector | Chooses which few-shot examples to include for this input |
| Output parser | Turns model text into structured data; supplies format instructions |
| Retriever | Interface: query in, documents out. Backend can be anything. |
| Chain | Composition where each step's output feeds the next |
| Agent | Chooses actions via tools, observes results, decides what to do next |

| Retrieval concept | Detail |
|---|---|
| DPR | Separate question and context encoders, aligned so questions land near answering passages |
| FAISS | Efficient nearest-neighbour search over dense vectors. Stores and searches only. |
| Top-k | Too few: answer absent. Too many: signal diluted, prompt cost up. |
| Chunk overlap | Ensures content across a boundary appears whole in at least one chunk |

> Changing the embedding model invalidates the whole index — old and new vectors live in incomparable spaces. The corpus must be re-embedded. Generators swap freely; embedders do not.

- Topically right chunks that never contain the answer = a chunking problem, not a model problem.
- Good retrieval with poor answers = a generation problem: context assembly, instructions or generator choice.
- Similarity search always returns its nearest neighbours however far away. Out-of-scope questions need a relevance threshold or a grading step.
- Instruct the model to answer only from context and to say when the context does not contain the answer.
- Deleting a source document does nothing until its chunks are removed from the index.
- Treat retrieved and user-supplied text as data, never as instructions. Fence it and keep it out of the privileged section.
- RAG over fine-tuning when facts change or answers must cite sources; fine-tuning for stable behaviour and style.

---

## Acronyms

*Blank on one of these and you lose the question*

| Term | Expansion / meaning |
|---|---|
| BERT | Bidirectional Encoder Representations from Transformers |
| BLEU | N-gram precision against reference translations, with a brevity penalty |
| BPE | Byte-pair encoding — subword tokenisation by merging frequent pairs |
| CBOW | Continuous bag of words — word2vec variant predicting target from context |
| CoT | Chain-of-thought prompting |
| DPO | Direct Preference Optimization — policy from preferences, no reward model |
| DPR | Dense Passage Retrieval — dual encoder retrieval |
| FAISS | Facebook AI Similarity Search — dense vector index |
| GAN | Generative Adversarial Network |
| GPT | Generative Pre-trained Transformer — decoder stack, causal LM |
| GRU | Gated Recurrent Unit |
| KL | Kullback-Leibler divergence — the leash on policy drift in PPO |
| LoRA | Low-Rank Adaptation |
| LSTM | Long Short-Term Memory |
| MLM | Masked Language Modelling — BERT's pretraining objective |
| NSP | Next Sentence Prediction — BERT's second pretraining objective |
| PEFT | Parameter-Efficient Fine-Tuning |
| PPO | Proximal Policy Optimization |
| QLoRA | LoRA over a 4-bit quantised base model |
| RAG | Retrieval-Augmented Generation |
| RLHF | Reinforcement Learning from Human Feedback |
| RNN | Recurrent Neural Network |
| ROUGE | Recall-oriented n-gram overlap, used for summarisation |
| SFT | Supervised Fine-Tuning |
| TRL | Transformer Reinforcement Learning — Hugging Face alignment trainers |
| VAE | Variational Autoencoder |
