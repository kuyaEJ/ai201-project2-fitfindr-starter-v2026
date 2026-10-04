# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does
This project allows user to inquire on clothes from a set of item listings of different categories, sizes, and styles. The listing includes tops, bottoms, outerwear, and shoes providing affordable list of clothes in the listings. Apart from the listings this project provides ouftfit suggestions and examples of fits that combine well together. 
<!-- Three or four sentences: what a user asks for, and what they get back. -->



---

## Tool Inventory

<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** Searches the `listings.json` file for clothings and accessories, so the most relevant items are provided.
- **Inputs:** The `description` (str), `size` (str), `max_price` (float)
- **Returns:** A `matched` (list[dicts]):: This is a reversed, sorted by score, list of dicts each with `id` (str), `score` (float), `price`(float) (inclusive or not), and a dictionary called `listing`. The `listing` dictionary has these fields: `id` (str), `title` (str), `description` (str), `category` (str), `style_tags` (list(str)), `size` (str), `condition` (str), `price` (float), `colors` (list(str)), `brand` (str), and `platform` (str).
- **When it has nothing:** Returns the first result (most relevant) searched listings that match the description then run `suggest_outfit` with it, otherwise, returns an error string in `session["error"]` when the tool returns an empty list `[]`.

### `suggest_outfit`

- **What it does:** When given a thrifted item and the user's wardrobe, suggest one or two outfits.
- **Inputs:** A `new_item` a listing dict - the item the user is considering, `wardrobe` a wardrobe dict with an `items` key holding the list of items. **It may be empty** . The `new_item` has fields each with an `id` (str), `name` (str), `category` (str), `colors` (list(str)), `style_tags` (list(str)), and `notes` (str or null). The `wardrobe` has these same fields but inside the key `items` array which has a list of dicts.
- **Returns:** A `response` str of the generated suggestion of 1 or 2 outfits to combine `new_item` (dict) with other items from the user's existing `wardrobe` (dict) which are all pieces in the outfit areexplicitly mentioned. 
- **When it has nothing:** Returns a generated suggestion str, like a personal fashion stylist giving helpful and clear suggestions of at least 2 outfits, otherwise, if the parameters are empty then errors that list is empty and needs to be filled with content from `search_listings`. If generated suggestion fails then returns str of generic advice in `agent.py`'s `session["outfit_suggestion"]` for the `new_item` styling to be paired with neutral basics and complementary layers. 

### `create_fit_card`

- **What it does:** Writes a short caption about what someone would actually post on social media about what they found while thrifting.
- **Inputs:** A `outfit` str of the outfit suggestion from `suggest_outfit` and `new_item` the dict of the item they found. The `new_item` dict has these fields: `id` (str), `title` (str), `description` (str), `category` (str), `colors (str)`, `style_tags` (str), and `notes` (str).
- **Returns:** Returns a `response` str of generated captions for the outfit in 2-4 sentences, with the item name, price, and platform being specifically mentioned. The generated str includes details about the vibe that sounds like a real person sharing a thrift haul post on social media, not a store ad.
- **When it has nothing:** Returns a generated caption str in session["fit_card"] otherwise, if parameters are empty then errors that they need to be filled with content from `suggest_outfits`. If generated caption fails and is empty, it returns a generic caption with the item `title` (str), `price` (str), `platform` (str), and a short description.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:**

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->

**What moves through the session:** <!-- which fields, in what order -->

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"

```
[{'id': 'lst_002', 'score': 10.92, 'price': 'price is inclusive to 30', 'listing':{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Supercute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}}, {'id': 'lst_006', 'score': 8.67, 'price': 'price is inclusive to 30', 'listing': {'id': 'lst_006', 'title': 'Graphic Tee — 2003 Tour Bootleg Style', 'description': 'Vintage-style bootleg tee with faded graphic. Slightly boxy fit. 100% cotton, soft and worn-in.', 'category': 'tops', 'style_tags': ['graphic tee', 'vintage', 'grunge', 'streetwear', 'band tee'], 'size': 'L', 'condition': 'good', 'price': 24.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}}, {'id': 'lst_033', 'score': 7.99,'price': 'price is inclusive to 30', 'listing': {'id': 'lst_033', 'title': 'Vintage Band Tee — Faded Grey', 'description': 'Faded grey band-style tee with distressedgraphic. Crew neck. Fits boxy. Well-loved but no holes or major damage.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'band tee', 'graphic tee', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 19.0, 'colors': ['grey', 'charcoal'], 'brand': None, 'platform': 'depop'}}, {'id': 'lst_015', 'score': 4.3, 'price':'price is inclusive to 30', 'listing': {'id': 'lst_015', 'title': 'Vintage GraphicHoodie — Faded Black', 'description': 'Faded black pullover hoodie with barely-visible vintage graphic on the chest. Cozy interior. Some pilling but adds to the worn-in look.', 'category': 'tops', 'style_tags': ['vintage', 'grunge', 'graphic', 'streetwear'], 'size': 'L', 'condition': 'fair', 'price': 26.0, 'colors': ['black', 'charcoal'], 'brand': None, 'platform': 'depop'}}, {'id': 'lst_017', 'score': 4.04, 'price': 'price is inclusive to 30', 'listing': {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.','category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}}, {'id': 'lst_030', 'score': 3.0, 'price': 'price is inclusiveto 30', 'listing': {'id': 'lst_030', 'title': 'Vintage Knit Vest — Argyle Brown/Cream', 'description': 'Classic argyle knit vest in brown and cream. Fits medium. V-neck. Ideal for the dark academia or preppy vintage aesthetic.', 'category': 'tops','style_tags': ['vintage', 'preppy', 'knitwear', 'dark academia', 'earth tones'], 'size': 'M', 'condition': 'good', 'price': 25.0, 'colors': ['brown', 'cream', 'tan'], 'brand': None, 'platform': 'thredUp'}}, {'id': 'lst_034', 'score': 3.0, 'price': 'price is inclusive to 30', 'listing': {'id': 'lst_034', 'title': 'Bucket Hat — Reversible, Brown Plaid', 'description': 'Reversible bucket hat — plaid on one side, solid tan on the other. Unstructured brim. One size fits most.', 'category': 'accessories', 'style_tags': ['90s', 'streetwear', 'vintage', 'accessories'], 'size': 'OneSize', 'condition': 'excellent', 'price': 14.0, 'colors': ['brown', 'tan', 'plaid'], 'brand': None, 'platform': 'thredUp'}}, {'id': 'lst_038', 'score': 3.0, 'price':'price is inclusive to 30', 'listing': {'id': 'lst_038', 'title': 'Denim Vest — Medium Wash, Studded', 'description': 'Denim vest with silver stud detailing along the collar and pockets. Classic rock-inspired customization. Fits like a medium.', 'category': 'outerwear', 'style_tags': ['grunge', 'vintage', 'denim', 'customized', 'rock'], 'size': 'M', 'condition': 'good', 'price': 27.0, 'colors': ['medium blue'],'brand': None, 'platform': 'depop'}}, {'id': 'lst_011', 'score': 1.99, 'price': 'price is inclusive to 30', 'listing': {'id': 'lst_011', 'title': 'Low-Rise Cargo Pants — Khaki', 'description': 'Y2K era low-rise cargo pants. Lots of pockets. Khaki color, slightly distressed at the hems. Great for layering with a long tee.', 'category': 'bottoms', 'style_tags': ['y2k', 'cargo', '2000s', 'streetwear'], 'size': 'W29', 'condition': 'fair', 'price': 27.0, 'colors': ['khaki', 'tan'], 'brand': None, 'platform': 'poshmark'}}]
```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

```
**Outfit 1: Casual Streetwear**
Pair the new Vintage Levi's 501 Jeans (New Item) with the white ribbed tank top (w_003), layered under the oversized grey crewneck sweatshirt (w_004). Finish the look with chunky white sneakers (w_007) and the black crossbody bag (w_010).

**Outfit 2: Edge & Denim**
Combine the Vintage Levi's 501 Jeans (New Item) with the black cropped zip hoodie (w_005) and the vintage black denim jacket (w_006) for a double-denim moment. Ground the outfit with black combat boots (w_008) and the brown leather belt (w_009).
```
$ python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"

```
Just scored these Vintage Levi's 501 Jeans in a sick medium wash on depop for only$38.0. The vintage denim streetwear vibe is unmatched and the fit is genuinely chefs kiss. Throw them on with some fresh white sneakers and an oversized tee for the ultimate lazy-day fit. 🤌✨

---

## How I Used AI

<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:* I asked Gemini to help me think of how to score keywords and gave it my `search_listings` tool as descriptions and my `app.py` fields in `listings.json` as references.
- *What came back:* It suggested for me to use a industry standard Bm25 system where the listings are scored higher based on things that are rarer.
- *What I changed:* It gave a generic scoring system whose average scores were too high, so I had certain keywords get higher scores in order for the scores to not be too high. Additionally, I added a size scoring addition as well. If the item size matches exactly with `max_size` it will earn 3 full pts, while inclusive sizes get 1.5 pts, and the rest gets 0 pts. I wanted there to be more room for error on sizes so I suggest it to provide a score of  0.75pts when the size is 2 sizes smaller or larger.

**Moment 2**

- *What I asked for:* I asked Gemini to attack my acceptance criteria that I drafted.
- *What came back:* It provided edge cases and a perspective on testing indicating how there can be errors that happens such as false positives, LLM hallucinations, and empty matches in the `search_listings`, sessions getting modified after being recieved by other tools, and more. It gave me session["error"] example that helped me write errors for empty search results.
- *What I changed:* As a result I added a check to ensure the right instance is being passed, and the item searches the correct field such as the `listing` field since it has the metadata of the item inside. I asserted the objects identity as well to ensure the fields don't change after being passed to the session before being sent to the next tool `suggest_outfit`.

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
