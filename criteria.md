# Acceptance criteria — FitFindr

Five criteria that say what "working" means for this agent, written in unit 3 **before** any results existed.

An acceptance criterion names a target: a number, a count, a rate, or something a person could plainly observe. *"The agent handles errors"* is an opinion. *"When search returns nothing, the agent stops before calling the second tool, in 5 of 5 tries"* is a criterion.

Under each one, write a sentence or two on **why that target** and not a stricter one. A reason that says something about your tools, your loop, or the data earns credit; *"80% seemed reasonable"* does not.

> Missing your own targets next unit costs you nothing. Setting a target so easy you can't miss it does.

**Two are written for you. You write three.**

---

## 1. A matching query completes all three tools

Given a query that matches at least one listing, the agent completes all three tool calls and returns a fit card — in at least 4 of 5 tries.

**Why this target:**

I am confident in my keyword matches and logic for the agent to complete 3 tool calls. All of the keywords in the listings dicts fields for `description`, `title`, `style_tags`, and `colors`, are scanned and scored with BM25 + IDF weights. Additionally, I have a relevance gate for item sizes with an impacted smaller score for partial matches or misses. However, should `SEARCH_RESULT_LIMIT` in `config.py` be too low or if there are too many tokens then there may be cases where scores that should be correct instead become wrong. The amount of keywords in the provided search can change scoring of items. Additionally, the agent may terminate in `search_listings` if the query price and query size is too low as well.
<!-- Why 4 of 5 and not 5 of 5? Something about your search, probably —
     "my search is a plain keyword match and some phrasings will miss" is a real answer. -->

---

## 2. An impossible query stops before the second tool

Given a query that matches no listings, the agent stops before calling
`suggest_outfit` and returns a message naming what to change — 5 of 5 tries.

**Why this target:**

The file `agent.py` has a `run_agent` method that guards and ensures listings is not empty and returns the session so it doesn't proceed. The tool for `suggest_outfit` will never be given an empty listing unless it the hardware malfunctions in runtime which is a very small probability. Additionally, it's not possible for `matches.sort` to not be equal to None unless someone manually changes it internally meaning matches will almost always have at least 1 item. The only way for the list to be empty is when the price, size, or descriptions for the item is way too small and not mentioned anywhere in the data and in those cases `app.py` and `agent.py` already handle it.
<!-- Why is 5 of 5 reasonable here when criterion 1 isn't? What's different about this path? -->

---

## 3. The session item fields should match the tool results

Given a query when `search_listings` ends, the listing should verify that `session["selected_item"]` has the same metadata fields for `id`, `title`, `price`, and `size` after the session is set. The check should pass 3 of 5 tries.

<!-- YOU WRITE THIS ONE.

     How would you know that the item your search found is the same item the next tool received? Name something countable or observable.

     This is the criterion people find hardest, because state failure doesn't look like state failure — it looks like a tool problem. Something that compares session["selected_item"] against what actually reached suggest_outfit is the shape you're after. -->



**Why this target:**

I chose 3 of 5 tries since `search_listings` results are still passed to an AI model, therefore, the results in the session can change after being passed or after it uses them to generate another result like in the `suggest_outfits` tool.

This target accounts for AI hallucinations where a typo or mistake is made. The target might miss in cases where `search_listings` returns an empty string as well. The target ensures that the state is unchanged by an LLM hallucination by checking that it didn't make up a new listing since AI hallucinations are not preventable when limits are reached then the agent should fail eventually.


---

## 4. Something about the fit card

Given a query the fit card shouldn't repeat the same caption or in other tools the AI should not add unwanted results i.e., invalid listing fields such as a wrong `id`, `title`, or a new field in 3 of 5 tries.

<!-- YOU WRITE THIS ONE.

     The fit card calls a model, so the same input can produce different words each time. That's not a bug — it's the nature of the tool. So what would make it acceptable?

     Think about what you'd actually be unhappy to see. A caption that never mentions the price? Two different items producing the same opening sentence? A card longer than a caption anyone would post? Any of those can be turned into a number. -->



**Why this target:**
I picked 3 of 5 since AI noticeably hallucinates and the AI model will forget or lose some details as it is generating the results.

AI is known to repeat hallucinations so criteria 4 ensures the hallucinations are kept to a minimum. In the `create_fit_card` tool the AI has more possibilities of it's results being non-creative without having varied details in prompts as well. There are also 3 tools used in 1 try so hallucinations have a increased chance of occuring.

---

## 5. Your choice

Given a query the `search_listings` tool should accurately find the size of an item when it is described in the `description` field for size scoring in 3 of 5 tries.

<!-- YOU WRITE THIS ONE TOO.

     Pick something you actually care about getting right. Speed, the empty
     wardrobe path, what happens when the model can't be reached, whether the
     search respects a price ceiling — anything, as long as it names a number
     or an observable outcome. -->



**Why this target:**

I picked 3 of 5 since my search will account for keyword sizes described in the description.

The dataset has a good pattern where some clauses can be separated on common phrases such as "says size x but fits like y". This can be indexed. In cases where the size fits "good enough" in the description the cases won't have the `but` keyword or incorrect tags which is also indexable but harder to measure. False positives can occur when a different sizing phrase is used or when the keywords `small`, `medium`, `large`, `extra large`, or `oversized` are used out of the sizing context which should be accounted for in data sets.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     UNIT 4 — read this before you change anything above.

     If a criterion turns out to be BROKEN rather than merely unmet, you can
     revise it, and that earns credit. But never delete or edit the original
     line. Add the revision underneath it, like this:

         ## 4. Something about the fit card

         The fit card is different every time.

         **Why this target:** ...

         > **Revised in unit 4:** For 5 different items, the 5 fit cards share
         > no opening sentence.
         >
         > **Why revised:** "different" wasn't checkable — two cards that
         > differed by one word still counted. The new version is something I
         > can actually score.

     That's a revision because the criterion couldn't be MEASURED.

     Lowering a target because you missed it is not a revision, and it costs
     you the point:

         ✗ "I said the empty search stops it 5 of 5 times, but I got 3 of 5,
            so 3 of 5 is more realistic."

     A number you missed stays where it is, gets diagnosed, and gets a fix
     attempted. That's where the points are.
     ───────────────────────────────────────────────────────────────────────── -->
