"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""

import config
import trace
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable
import re


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }

# Helper query parser using regex (no additional LLM latency required)
def parse_query(query: str) -> dict:
    query_lower = query.lower()
    
    # Extract max price (e.g., "under $30", "under 30", "max $25")
    price_match = re.search(r'(?:under|below|max|\$)\s*\$?(\d+(?:\.\d+)?)', query_lower)
    max_price = float(price_match.group(1)) if price_match else 0.0

    # Extract common clothing sizes
    size_match = re.search(r'\b(xxs|xs|s|m|l|xl|xxl|w\d{2})\b', query_lower)
    size = size_match.group(1).upper() if size_match else ""

    # Clean description by stripping price and size patterns
    desc = query_lower
    if price_match:
        desc = desc.replace(price_match.group(0), "")
    if size_match:
        desc = desc.replace(size_match.group(0), "")
    desc = re.sub(r'\b(under|below|size|max)\b', '', desc).strip()

    return {
        "description": desc,
        "size": size,
        "max_price": max_price
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """
    Run the loop once and return the finished session.

    Args:
        query:    what the user asked for, in plain language
                  (e.g. "vintage graphic tee under $30, size M").
        wardrobe: a wardrobe dict — get_example_wardrobe() or
                  get_empty_wardrobe() from utils/data_loader.py.

    Returns:
        The session dict. **Check session["error"] first** — if it isn't None,
        the run ended early and the later fields will still be None.

    ─────────────────────────────────────────────────────────────────────────
    TODO — build this, following the branch rule you wrote in Milestone 2.

      1. Start a session with new_session().

      2. Count the times round the loop, and call trace.check_iterations(count)
         on each one before you go again. It raises when the count passes
         MAX_ITERATIONS in config.py — see trace.py.

      3. Parse the query into a description, a size, and a max_price. Regex,
         string splitting, or asking the model are all fine — say which you
         chose in your README. Put the result in session["parsed"].

      4. Call search_listings() with what you parsed.
         Put the results in session["search_results"].

         ⚠️ THIS IS THE BRANCH. If nothing came back:
              - put a message in session["error"] saying what the user could
                change — "No results" is not that message
              - return the session
              - do NOT call suggest_outfit with nothing

      5. Choose an item — the first result is fine. Put it in
         session["selected_item"].

      6. Call suggest_outfit() with the selected item and the wardrobe.
         Put the result in session["outfit_suggestion"].

      7. Call create_fit_card() with the outfit and the item.
         Put the result in session["fit_card"].

      8. Return the session.

      python -c "from agent import run_agent; from utils.data_loader import get_example_wardrobe, load_listings; print(run_agent('', get_example_wardrobe()))"

    ─────────────────────────────────────────────────────────────────────────
    IN UNIT 4 you come back and add two things:

      • Trace calls. One per step. `trace.step("search_listings", inputs=...,
        returned=...)` — see trace.py. Your README needs the output.

      • A handler for ModelUnavailable, so a bad key produces a message rather
        than a stack trace. The import is already at the top of this file.
    """
    session = new_session(query, wardrobe)
    iteration_count = 0

    try:
        # Step 1: Iteration Check
        iteration_count += 1
        trace.check_iterations(iteration_count)

        # Step 2: Parse Query
        session["parsed"] = parse_query(query)
        parsed = session["parsed"]
        # trace.step("parse_query", inputs={"query": query}, returned=parsed)


        # Step 3: Search Listings
        # Extract parsed components for search_listings(query, size_filter, max_price)
        search_query = parsed.get("description")
        size_filter = parsed.get("size")
        max_price = parsed.get("max_price")

        if not search_query:
            session["error"] = (
                f"No items matching search for empty query"
                f"\nPlease enter a non-empty search requirement"
            )
            return session["error"]

        session["search_results"] = search_listings(search_query, size_filter, max_price)
        results = session["search_results"]
        if results == []:
            print("Recieved empty string. Query might have returned empty")
        # trace.step(
        #     "search_listings", 
        #     inputs={"query": search_query, "size_filter": size_filter, "max_price": max_price}, 
        #     returned=f"Found {len(results)} items"
        # )

        # Step 4: THE BRANCH (Guard against empty search results)
        if not results:
            price_msg = f" under ${max_price:.2f}" if max_price > 0 else ""
            size_msg = f" in size {size_filter}" if size_filter else ""
            session["error"] = (
                f"No items matched your search for '{search_query}'{size_msg}{price_msg}. "
                f"Try loosening your price cap, broadening your search terms, or checking for other sizes."
            )
            return session["error"]

        # Step 5: Select Item (Grab top listing dict directly)
        first_result = session["search_results"][0]

        # Extract inner listing dictionary from search_listings result wrapper
        if isinstance(first_result, dict) and "listing" in first_result:
            selected_item = first_result["listing"]
        else:
            selected_item = first_result

        session["selected_item"] = selected_item

        # Trace step
        item_title = selected_item.get("title", "Unknown Item")
        item_price = selected_item.get("price", 0.0)
        item_platform = selected_item.get("platform", "")
        item_size = selected_item.get("size", "")
        # print(item_title + str(item_price) + item_size + item_platform == title_session + str(price_session) + size_session + platform_session)
        # trace.step(
        #     "select_item",
        #     inputs={"results_count": len(results)},
        #     returned=f"{item_title} (${item_price}, {item_size}, {item_platform})"
        # )

        # Step 6: Suggest Outfit
        session["outfit_suggestion"] = suggest_outfit(session["selected_item"], wardrobe)
        outfit = session["outfit_suggestion"]
        # trace.step("suggest_outfit", inputs={"item_id": selected_item.get("id")}, returned=outfit[:50] + "...")
        
        
        title_session = session["selected_item"].get("title", "")
        price_session = session["selected_item"].get("price", 0)
        platform_session = session["selected_item"].get("platform", "")
        size_session = session["selected_item"].get("size", "")
        assert item_title + str(item_price) + item_size + item_platform == title_session + str(price_session) + size_session + platform_session, "Failed acceptance criteria 3 this run"

        # Step 7: Create Fit Card
        session["fit_card"] = create_fit_card(outfit, selected_item)

        # fit_card = session["fit_card"]
        # trace.step("create_fit_card", inputs={"item_id": selected_item.get("id")}, returned=fit_card[:50] + "...")

    except ModelUnavailable as e:
        # Gracefully capture network or API issues without crashing the process
        session["error"] = f"Model service unavailable: {e}"
        # trace.step("model_error", inputs={"query": query}, returned=str(e))

    return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
