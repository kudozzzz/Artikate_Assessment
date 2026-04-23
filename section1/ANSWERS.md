## Section 1 — Problem 1: Hallucinated Pricing Responses

### Hypothesis Tree

When a chatbot gives incorrect pricing with high confidence, I would consider four likely causes:

1. **Retrieval issue**  
The chatbot may depend on a pricing database or knowledge base and the wrong price is being retrieved or no relevant data is being retrieved at all.

2. **Knowledge cutoff issue**  
If the model is answering from pretraining knowledge instead of live pricing data, it may return outdated prices.

3. **Prompt issue**  
The prompt may not clearly instruct the model to use verified pricing sources only, causing it to guess when data is missing.

4. **Temperature / generation settings**  
If temperature is high, the model may produce more speculative responses instead of deterministic answers.

---

### Tests Performed

#### Test 1: Ask about a recently changed product price

If the model gives an old price, that points toward stale internal knowledge or outdated retrieval data.

#### Test 2: Check retrieval logs

I would inspect whether the correct pricing document, table or API result was fetched before generation.

If no pricing source was retrieved, the issue is retrieval rather than generation.

#### Test 3: Force temperature to 0

If wrong answers still appear, temperature is not the primary cause.

#### Test 4: Remove retrieval and ask directly

If the model still guesses prices, then prompt controls are weak and the model is relying on memory.

---

### Root Cause Identified

The most likely root cause is a **retrieval failure combined with weak fallback behaviour**.

Pricing is dynamic data and should not be answered from model memory. If retrieval misses the latest pricing source, the model fills the gap confidently.

---

### Fix

1. Treat pricing as structured live data, not LLM memory.  
Use a pricing API or regularly updated pricing database.

2. Add prompt constraints such as:

> If verified pricing data is unavailable, state that pricing could not be confirmed.

3. Require source grounding before answering pricing questions.

4. Set temperature to 0 for factual pricing responses.

5. Add monitoring for pricing mismatches between generated responses and source data.

---

### Final Decision

This is primarily a **retrieval issue**, not a model intelligence issue.
The model should never be the source of truth for changing prices.



## Section 1 — Problem 2: Bot Replies in English Even When User Writes in Hindi or Arabic

### Hypothesis Tree

When a multilingual chatbot sometimes switches to English despite receiving Hindi or Arabic input, I would investigate the following causes:

1. **Prompt hierarchy issue**  
The system prompt may instruct the model to be helpful but does not explicitly require replying in the user’s language.

2. **Mixed-language context issue**  
Earlier conversation history, retrieved documents or tool outputs may be in English, causing the model to drift toward English.

3. **Fallback behaviour of the model**  
If the query is ambiguous or domain-specific, the model may default to English because most training data and business content are English-heavy.

4. **Pre-processing issue**  
Language detection or translation middleware may be incorrectly normalising input before sending it to the model.

---

### Tests Performed

#### Test 1: Reproduce with isolated prompt

I would send a Hindi and Arabic query in a fresh session without history.  
If the model still replies in English, the issue is likely in the system prompt.

#### Test 2: Remove conversation history

If the problem disappears after clearing prior messages, context contamination is likely.

#### Test 3: Inspect retrieved context

If retrieved product docs or support snippets are only in English, the model may mirror that language.

#### Test 4: Review middleware logs

I would verify that the original user text reaches the model unchanged and is not translated upstream.

---

### Root Cause Identified

The most likely root cause is a **weak system prompt combined with English-heavy context**.

If the prompt does not clearly prioritise response language, the model often defaults to English, especially when surrounding context and knowledge sources are English.

---

### Fix

Update the system prompt to make language behaviour explicit and deterministic.

**Recommended system prompt change:**

> Always reply in the same language as the user’s latest message.  
> If the user switches languages, switch with them.  
> Do not default to English unless the user asks in English.

Additional controls:

1. Detect user language from the latest message, not older history.  
2. Keep retrieved answers but translate the final response when needed.  
3. Add regression tests using Hindi, Arabic and mixed language prompts.

---

### Final Decision

This is primarily a **prompt control issue**, not a model capability issue.

The model can respond in multiple languages but the instruction hierarchy must clearly define which language to use.


## Section 1 — Problem 3: Response Time Increased from 1.2s to 8–12s Over Two Weeks

### Hypothesis Tree

When latency gradually worsens over time without prompt or model changes, I would investigate system level causes before blaming the model itself.

1. **Traffic growth / queue saturation**  
The user base may have grown, causing requests to wait in queues or hit concurrency limits.

2. **Longer prompts and growing conversation history**  
As users continue chats, more tokens are sent per request, increasing processing time.

3. **Retrieval layer slowdown**  
Vector search, database queries or document fetching may have slowed as data volume increased.

4. **Provider-side throttling or rate limits**  
The external LLM provider may be applying slower throughput during peak load.

5. **Infrastructure degradation**  
CPU, memory, disk I/O, or network bottlenecks may have appeared over time.

---

### Tests Performed

#### Test 1: Compare latency breakdown by stage

I would split total latency into:

- request queue time  
- retrieval time  
- model API time  
- post-processing time

This identifies where delay is actually occurring.

#### Test 2: Compare token counts over time

If average prompt size or conversation history increased significantly, slower responses are expected.

#### Test 3: Check request volume and concurrency metrics

If traffic increased while infrastructure remained the same, queue delays are likely.

#### Test 4: Review provider API logs

I would inspect timeout rates, throttling responses and average model inference times.

#### Test 5: Check infrastructure metrics

CPU spikes, memory pressure, swap usage or slow disk/network activity can create gradual degradation.

---

### Root Cause Identified

The most likely root cause is **increased traffic combined with growing prompt size**.

No code change is needed for latency to worsen if more users are active and each request contains larger conversation history than earlier test traffic.

---

### Fix

1. Limit conversation history sent to the model.  
Use summarisation or rolling context windows.

2. Add request queue monitoring and autoscaling.

3. Cache repeated retrieval results and common answers.

4. Use async request handling and connection pooling.

5. Track p50 / p95 / p99 latency separately for retrieval and model calls.

6. If needed, move some traffic to a faster or smaller model tier.

---

### What I Would Investigate First and Why

I would first inspect **queue time and token growth** because they commonly increase gradually with usage and often explain large latency jumps without any code changes.

---

### Final Decision

This is most likely an **operations and scaling issue**, not a prompt issue.
The system performed well in testing but was not sized for production growth.


## Section 1 — Post-Mortem Summary

During production rollout, three separate issues affected chatbot quality and speed.

Incorrect pricing responses were caused by the assistant relying on incomplete or outdated data instead of a verified live pricing source. Pricing answers should be grounded to structured backend data, with refusal behaviour when current data is unavailable.

Language inconsistency occurred because prompt instructions did not strongly enforce replying in the same language as the user. In multilingual systems, response language should be explicitly controlled at the system prompt level and tested regularly.

Latency increased over time mainly due to production growth. As more users joined, request queues increased and larger conversation histories raised token processing time. This created slower responses even without code changes.

To prevent recurrence, we would add retrieval monitoring, prompt regression tests, token budgeting, queue dashboards, and autoscaling alerts. These issues were operational and architectural, not model capability failures.