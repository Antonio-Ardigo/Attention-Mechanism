# Q, K, V — How Attention Learns to Specialize

A training plan for explaining the attention mechanism to people who are smart but not mathematical.

---

## At a glance

| | |
|---|---|
| **Audience** | Product managers, analysts, designers, executives, engineers new to ML |
| **Prerequisites** | None. Curiosity about how language models work. No math, no code. |
| **Format** | 4 sessions × 60 min, or one 4-hour workshop with two breaks |
| **Group size** | 6–20 (activities need pairs and small groups) |
| **Materials** | Slides, sticky notes, printed sentence handouts, one laptop for the live demo |

### What learners can do afterwards

By the end, a participant can:

1. Explain in plain language why a word's meaning depends on the words around it, and why that is hard.
2. Describe what Query, Key, and Value each represent, using an analogy of their own.
3. Explain that the model learns **how to look**, not **what to look at** — and say why that distinction matters.
4. Describe the training loop that produces attention behaviour, without any formula.
5. Explain why different attention heads end up doing different jobs, when nobody assigned those jobs.
6. Read an attention map and say something true about it — and name one thing it does *not* prove.

### The one sentence the whole course is built around

> **Nobody teaches attention what to pay attention to. It is a side effect of being repeatedly graded on one thing: predicting the next word.**

If a participant leaves with only that sentence and can defend it, the training worked.

---

## Session 1 — The problem attention solves (60 min)

**Goal:** create the itch before showing the cure. Attention makes no sense until the problem is felt.

### Key idea

Words don't have fixed meanings. They have meanings *in context*. Any system that gives each word one permanent definition will get language wrong.

### Talk track (15 min)

Put three sentences on screen, one at a time:

- *"I sat on the **bank** of the river."*
- *"I withdrew cash from the **bank**."*
- *"The plane began to **bank** to the left."*

Same five letters. Three unrelated meanings. Ask: what told you which one? The answer is always *another word in the sentence* — river, cash, plane. The meaning came from somewhere else in the sentence.

Then the harder case:

- *"The trophy didn't fit in the suitcase because **it** was too big."*
- *"The trophy didn't fit in the suitcase because **it** was too small."*

One word changed, and *"it"* switched which object it refers to. Nothing about the word *"it"* changed. The whole difference lives in the relationship between words.

**Land the point:** a model needs a mechanism that lets each word go and fetch what it needs from the other words. Attention is that mechanism. That's all it is — a principled way for words to look at each other.

### Activity — Human context resolution (20 min)

Hand each pair a slip with an ambiguous sentence. Ask them to write down:

1. Which word was ambiguous?
2. Which *other* word resolved it?
3. How far away was it — 1 word, 5 words, 30 words?

Collect answers on a whiteboard as arrows between words. You have just drawn, by hand, the thing the model computes. Keep this board photo — you'll refer back to it in Sessions 2 and 4.

### Check for understanding (10 min)

Ask the room: *"Why can't we just give every word a really, really good dictionary definition and be done?"*

Looking for: because the definition would have to change depending on the neighbours, and there are infinitely many possible neighbourhoods.

### Facilitator notes

- Resist explaining Q, K, V here even if someone asks. Say "that's exactly session two" and let the tension sit.
- If the group is technical, add: this is also why word-level embeddings alone were not enough, and what made contextual models a step change.

---

## Session 2 — Meet Q, K, and V (75 min)

**Goal:** the three roles, made concrete and memorable. This is the session people quote back to you.

### Key idea

Every word produces three different things, for three different purposes:

| | Name | What it is | Plain-language version |
|---|---|---|---|
| **Q** | Query | What this word is looking for | *"I'm a verb — where's my subject?"* |
| **K** | Key | What this word advertises about itself | *"I'm a plural noun, and I'm a subject."* |
| **V** | Value | What this word actually contributes | *"Here's my meaning, take it."* |

The mechanism in four steps:

1. Each word broadcasts its **Query** — the thing it needs.
2. Every word displays its **Key** — the thing it offers.
3. Queries and Keys are compared. Good match → high score. Poor match → low score.
4. Scores become percentages, and each word receives a blend of everyone's **Values**, weighted by those percentages.

That's it. Ask, advertise, match, blend.

### The analogy — a conference room (15 min)

You're at a conference. You need to know something specific.

- Your **Query** is the question you shout across the room: *"who here knows about supply chains?"*
- Everyone's **Key** is their name badge: *"Maria — logistics"*, *"Tom — legal"*, *"Priya — supply chain"*.
- You listen mostly to Priya, a bit to Maria, and essentially not at all to Tom.
- What Priya then *tells you* is her **Value**.

Two details that make this analogy earn its keep:

**Why are Key and Value separate?** Because how you find someone is not the same as what they tell you. The badge is short and searchable. The answer is long and detailed. In the model, the same split applies: a word's Key is optimised for *being findable*, its Value for *being useful once found*. Tying them together would force one representation to do two conflicting jobs.

**You don't pick one person — you get a blend.** Attention is never a hard choice of one word. It's always a weighted mixture: 70% Priya, 25% Maria, 5% everyone else. The percentages always add to 100%.

### Activity — Be the sentence (25 min)

Give each participant a word from *"The keys to the cabinet were on the table"* on a card, worn as a badge.

- Round 1: whoever holds **"were"** stands and says their Query out loud: *"I need my subject — who is plural and comes before me?"*
- Everyone else reads their Key: *"I'm 'keys' — plural noun"*, *"I'm 'cabinet' — singular noun"*, *"I'm 'the' — a determiner"*.
- The room votes with raised hands on where **"were"** should look. They will pick *keys*, not *cabinet* — the same thing the model must learn, and the same thing grammar-checkers historically got wrong.
- Round 2: rerun with **"on"** as the Query. Notice how it wants something completely different. Same room, different question, different winners.

**Debrief:** the words didn't change between rounds. The *question* changed. Attention is recomputed from scratch for every word, every time.

### Optional maths box — for the one person who will ask (5 min)

Show it once, explain it in words, move on:

```
Attention(Q, K, V) = softmax( Q · Kᵀ / √d ) · V
```

- `Q · Kᵀ` — compare every Query against every Key. That's the matching step.
- `/ √d` — a volume knob that keeps the scores from getting extreme. Housekeeping, not an idea.
- `softmax(...)` — turn scores into percentages that add to 100%.
- `· V` — blend everyone's Values according to those percentages.

Say plainly: *"Every idea in this formula is one you already have. The notation is bookkeeping."*

### Check for understanding (10 min)

Each person writes their own analogy for Q/K/V — dating apps, job postings, library catalogues, radio frequencies. Share three. **Insist that each analogy explains why Key and Value are different things.** The ones that can't are the ones that will mislead later.

### Common misconceptions to correct on the spot

- ❌ *"Q, K, V are three separate networks."* They are three different views of the same word, produced at the same moment from the same starting point.
- ❌ *"Attention picks the single most relevant word."* It always blends. Sometimes the blend is very concentrated, which looks like picking — but it's a spectrum.
- ❌ *"Query and Key are the same thing."* A question and an advertisement are not the same object, even when they're about the same subject.

---

## Session 3 — How Q, K, and V actually get trained (75 min)

**Goal:** the heart of the course. Where the three roles come from, and how they get good at their jobs when nobody ever tells them what a good job looks like.

### Key idea, part 1 — three lenses

Each word arrives as a list of numbers — its raw meaning. It then passes through **three learned filters**, one each for Q, K, and V. Think of them as three lenses:

- The **Query lens** extracts *"what am I missing?"*
- The **Key lens** extracts *"what am I offering?"*
- The **Value lens** extracts *"what should I pass on?"*

**These three lenses are the only thing that gets trained.** They're shared by every word in every sentence — one Query lens, not one per word. The model doesn't memorise that verbs should look at subjects. It learns a lens that, when applied to any verb, produces a query that happens to match what subjects advertise.

That is the single most important structural fact in the course:

> **The model learns how to look. It never learns what to look at.**
> The lenses are fixed after training. The attention pattern is computed fresh for every sentence the model has never seen.

### Key idea, part 2 — the only thing the model is graded on (20 min)

Draw this loop on the board and walk it slowly:

```
   ┌─────────────────────────────────────────────────┐
   │                                                 │
   ▼                                                 │
Read text  →  Q/K/V lenses shape                 Nudge all three
"The keys      who looks at whom      →  Predict  →  lenses slightly
 to the ...                              the next    toward what
 cabinet                                 word        would have
 ___"                                       │        been less wrong
                                            ▼               ▲
                                    Compare to the truth ───┘
                                    ("were") — how wrong?
```

Run the example out loud:

1. The model reads *"The keys to the cabinet ___"* and predicts **"was"**.
2. The correct next word was **"were"**. That's a mistake, and the size of the mistake is measured.
3. That error is traced backwards through every step that contributed to it. One of those steps was: *how much did the prediction slot look at "keys" versus "cabinet"?*
4. It had looked mostly at *cabinet* (singular → "was"). Looking at *keys* would have helped.
5. So all three lenses are nudged, very slightly:
   - the **Query lens**, so verb-ish positions produce queries that lean more toward plural-subject-ish keys,
   - the **Key lens**, so nouns advertise their number more clearly,
   - the **Value lens**, so once *keys* is found, what it passes along is more useful.
6. Repeat across billions of examples.

**The punchline, said explicitly:** no human ever wrote down "verbs should attend to their subjects." No training example contains an attention pattern. The only feedback in the entire system is *"the next word was X, you said Y."* Grammar-shaped looking behaviour appears because it happens to reduce that error — and for no other reason.

### Analogy — the tuning dials (10 min)

Picture three dials for a radio you can't see, only hear.

- After each attempt you're told only: *your signal was this fuzzy.*
- You turn each dial a hair in whichever direction seemed to reduce fuzz.
- One nudge tells you almost nothing. A billion nudges tune the radio precisely.

Nobody ever told you the station's frequency. You found it by being graded on fuzziness, over and over. Q, K, and V are tuned the same way: not aimed, just relentlessly corrected.

### Activity — Reverse-engineer the pressure (20 min)

Small groups. Give each a sentence pattern the model must handle:

- *"Marie went to the shop. **She** bought bread."* → the pronoun must find Marie.
- *"The report that the committee published **was** long."* → the verb must skip the nearer noun.
- *"He opened the door, walked in, and closed **it**."* → *it* must find *door*, not *shop* or *committee*.

Each group answers:

1. Which word needs to look at which?
2. What would go wrong in the *prediction* if it looked at the wrong one?
3. Therefore, what would the error signal push the lenses to do?

This makes the causal chain concrete: **wrong looking → worse prediction → correction → better looking.** Learners who can run this chain in both directions have genuinely understood the training process.

### Check for understanding (10 min)

*"A model handles a sentence it has never seen, on a topic that didn't exist when it was trained. How can its attention be right?"*

Looking for: because what was trained is a general *way of asking and advertising*, not a stored list of word pairs. New words go through the same lenses and produce new, sensible queries and keys.

### Facilitator notes

- The most common stumble: people assume there must be some attention supervision somewhere. Say "there is none" three times, in three different ways. It genuinely surprises people.
- If asked about instruction tuning or RLHF: same principle, different grade. The feedback signal changes; the mechanism for how it reshapes the lenses does not.

---

## Session 4 — Why heads specialize, and how to see it (75 min)

**Goal:** from one attention mechanism to many, and how a division of labour emerges without a manager.

### Key idea, part 1 — many heads, running in parallel

A model doesn't run attention once per layer. It runs it many times side by side — 12, 32, 96 copies, depending on the model. Each copy is called a **head**, and each has its own private set of three lenses.

Why parallel copies? Because one question per word isn't enough. Reading *"were"*, you simultaneously want to know: what's my subject? what tense is this? am I inside a quotation? is this a list? One head can only ask one kind of question at a time. So the model asks many at once and combines the answers.

### Key idea, part 2 — why they don't all learn the same thing (20 min)

The obvious worry: if every head is trained by the same signal on the same data, why don't they all converge on the same job?

Two forces pull them apart:

**1. They start out different.** Every head's lenses begin as small random numbers. Purely by luck, head 3 is a hair better at tracking word order and head 7 is a hair better at matching repeated words. Training amplifies whatever a head is already slightly good at, because that's where its corrections do the most good. Small accidental differences compound into distinct roles.

**2. Doing someone else's job earns you nothing.** This is the important one. If two heads compute the identical thing, the second one adds no new information — so removing it wouldn't change the prediction, so it receives almost no corrective pressure to stay as it is. It drifts. Meanwhile, any job *nobody* is doing yet is a job where a head can measurably reduce the error, so pressure there is strong. **Specialization is not designed. It is what's left over once redundancy stops paying.**

An analogy that lands: nobody assigns roles in a small startup either. People drift toward whatever isn't being covered, because that's where their effort visibly matters. Same dynamic, no meeting required.

### What researchers actually find (15 min)

When people inspect trained models, recognisable head types show up again and again across independently trained systems — which is good evidence this is a real dynamic and not wishful pattern-matching:

- **Previous-token heads** — each word looks at the one just before it. Simple, appears early in the network, and is a building block for everything else.
- **Syntactic heads** — verbs find subjects, adjectives find their nouns, prepositions find their objects.
- **Coreference heads** — pronouns find the name they refer to. *She* → *Marie*, across sentences.
- **Induction heads** — spot a repeated pattern and continue it. Having seen *"Marie Curie"* earlier, when *"Marie"* appears again this head points at *"Curie"*. This is a large part of how models copy names, formats, and styles from earlier in your prompt — and much of why few-shot prompting works at all.
- **Delimiter and "resting" heads** — some heads park their attention on punctuation or on the very first token when they have nothing useful to do. It's a real, documented behaviour, sometimes called an attention sink. Worth mentioning because it inoculates against over-interpreting every pattern as meaningful.

**Say the caveat out loud:** these names are *our* labels, applied afterwards, to behaviour that is usually messier than the label suggests. Most heads do several partial things at once, and plenty do nothing we can name. Clean job titles are a teaching simplification, not a finding.

### Key idea, part 3 — depth changes the questions (10 min)

Stacked layers mean each layer's lenses read what the layer below already enriched. So the questions get more abstract as you go up:

- **Early layers** — position and surface form. *Which word is next to me? Is this the start of a sentence?*
- **Middle layers** — grammar and entity tracking. *Who is the subject? Which character is this pronoun?*
- **Late layers** — assembling the answer. *What information do I need to commit to the next word?*

A late-layer head can ask a sophisticated question only because earlier layers already turned raw words into something worth asking about. This is why bigger models specialize more sharply: more layers means more room for the questions to become abstract.

### Activity — Look at real attention (20 min)

Load an attention visualiser (BertViz, or any hosted attention map) and put one sentence through it in front of the group. Use their sentence from Session 1's whiteboard — the callback lands well.

Ask them to hunt for:

1. A head that looks mostly one word back.
2. A head where the pronoun connects to a name.
3. A head that looks like nothing at all — noise, or everything parked on the first token.

Finding (3) is the most valuable finding of the session, not the least. It's the evidence for the caveat.

**Closing debrief — the two questions that matter:**

- *"Does this show us what the model is thinking?"* It shows what each word looked at. That's real and useful, and it is not the same as an explanation of the decision. Information also flows through paths attention maps don't display.
- *"Who decided head 7 would track pronouns?"* Nobody. Randomness, plus prediction error, plus the fact that duplicated work earns no credit. That's the whole story.

---

## Assessment

Pick one. All three test explanation rather than recall.

**A. The three-minute colleague test.** Each participant explains Q/K/V to a partner who wasn't in the room, using their own analogy. The partner scores: did they explain why Key and Value are separate? Did they say the model learns *how* to look rather than *what* to look at?

**B. Spot the error.** Give five statements, three wrong. Learners mark which and fix them.

1. *"Engineers assign each attention head a linguistic job before training."* — Wrong. Roles emerge; nothing is assigned.
2. *"Attention weights always add up to 100% across the words being looked at."* — Correct.
3. *"Attention patterns are stored in the model and reused for sentences it has seen before."* — Wrong. The lenses are stored; patterns are recomputed every time.
4. *"The Key and the Value for a word can be different because being findable and being useful are different jobs."* — Correct.
5. *"During training, examples include labels for which words should attend to which."* — Wrong. The only label is the next word.

**C. Apply it.** *"Your product summarises 40-page contracts. Using what you learned, explain to a non-technical stakeholder why the model sometimes attaches a clause to the wrong party — and why that isn't a bug someone forgot to fix."*

---

## Glossary

| Term | Plain-language meaning |
|---|---|
| **Token** | A chunk of text the model handles — roughly a word or word-piece |
| **Query (Q)** | What this word is looking for |
| **Key (K)** | What this word advertises about itself |
| **Value (V)** | What this word contributes when it gets looked at |
| **Attention weight** | How much of one word's output comes from another word, as a percentage |
| **Head** | One independent copy of the attention mechanism, with its own three lenses |
| **Layer** | One full round of attention plus processing; models stack dozens |
| **Softmax** | The step that turns raw match scores into percentages adding to 100% |
| **Loss** | A number measuring how wrong the prediction was |
| **Induction head** | A head that spots a repeated pattern and continues it |

---

## Facilitator quick reference

**The five things to say at least twice:**

1. Attention is words fetching what they need from other words.
2. Query = what I need. Key = what I offer. Value = what I give.
3. Only the three lenses are trained. Patterns are recomputed every time.
4. The only grade is next-word prediction. Attention behaviour is a side effect.
5. Specialization emerges because duplicated work earns no credit.

**If you are short on time:** cut Session 1's activity to 10 minutes and drop the optional maths box. Do not cut Session 3 — the training loop is the point of the course, and every other session exists to set it up or pay it off.

**If the group is more technical than expected:** keep the same structure and add depth in the debriefs — multi-head concatenation and output projection, causal masking, why scaling by √d matters for gradient stability, KV caching at inference. Don't restructure the sessions; the analogies still carry the load.
