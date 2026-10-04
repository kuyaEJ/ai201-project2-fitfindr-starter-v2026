"""
The three FitFindr tools.

Each one is a standalone function you can call and test on its own, before any
of them are wired into the loop. Build and test them one at a time — three
untested tools joined by a loop is one problem that looks like six, because you
can't tell which layer is lying to you.

    search_listings(description, size, max_price)  → list[dict]
    suggest_outfit(new_item, wardrobe)             → str
    create_fit_card(outfit, new_item)              → str

All three are stubs right now. They run and they do nothing — that's the
starting position and it's deliberate.

⚠️ Before you write any of them, fill in the **Tool Inventory** section of your
README (Milestone 2). Four lines per tool: what it does, each input with its
type, exactly what it returns, and what it returns when it has nothing to give.
That last line is what your loop branches on. "Returns a list" earns nothing —
the description has to say what is *in* the list.
"""

import config  # noqa: F401 — you'll use this in search_listings
from generate import generate
from utils.data_loader import load_listings
import keywordScore
import re

# ── Tool 1: search_listings ───────────────────────────────────────────────────

_STOPWORDS = {
    "a", "at", "no", "or", "and", "but", "yet", "very", "be" "lots", "like", "tag", "says", "so", "the", "for", "just", "with", "sits", "can", "as", "on", "other", "from", "some", "under", "over", "in", "of", "-", "—", "[", "]", "'", '"', "(", ")", "_", ",", ".", "none"
}

# AI - generated dictionary 
CATEGORY_SIZE_TOKENS = {
    "tops": {
        "s": {"s"},
        "m": {"m", "s/m"},
        "l": {"l", "l/xl"},
        "xl": {"xl", "l/xl", "xl (oversized)", "xl (fits oversized)"},
        "os": {"one size / oversized"},
    },
    "outerwear": {
        "s": {"s"},
        "m": {"m", "m/l"},
        "l": {"l", "m/l"},
    },
    "bottoms": {
        "s": {"s"},
        "m": {"m", "m/l"},
        "27": {"w27"},
        "28": {"w28"},
        "29": {"w29"},
        "30": {"w30", "w30 l30"},
        "32": {"w32"},
    },
    "shoes": {
        "7": {"us 7"},
        "8": {"us 8"},
        "8.5": {"us 8.5"},
        "9": {"us 9"},
    },
    "accessories": {
        "os": {"one size", "one size (adjustable)"},
    },
}

SIZE_ORDER = ["s", "m", "l", "xl", "os", "7", "8", "8.5", "9", "27", "28", "29", "30", "32"]

# def _keywords(text: str) -> set[str]:
#     """lowercase words worth matching on, stopword removed."""
#     words = re.findall(r"[a-z0-9']+", (text or "").lower())
#     return {w for w in words if w not in _STOPWORDS and len(w) > 1}

# def _size_tokens(size: str) -> set[str]:
#     cleaned = re.sub(r"\([^)]*\)", " ", size or "") # drop parentheticals
#     parts = [p.strip().upper for p in cleaned.split("/")]
#     return {p for p in parts if p}

# def _size_matches(wanted: str, listing_size: str) -> bool:
#     if not wanted:
#         return True
#     listing_tokens = _size_tokens(listing_size)
#     if any(token.startswith("ONE SIZE") for token in listing_tokens):
#         return True
#     return bool(_size_tokens(wanted) * listing_tokens)

def load_listings() -> list[dict]:
    import json
    d = ""
    with open('data/listings.json', 'r', encoding='utf-8') as file:
        listings = json.load(file)
        converttostring = json.dumps(listings)
        d = json.loads( converttostring )
    return d


def find_size_in_text(text: str, category: dict) -> str | None:
    """Finds known categories of size tokens/words in any text string."""
    KEY_ALIASES = {
        "small":"s",
        "medium":"m",
        "large":"l",
        "oversized":"os",
        "one size":"os",
    }
    if not text:
        return None
    for key in KEY_ALIASES:
        isBut =  text.split('but')[1] if len(text.split('but')) > 1 else text
        # print(f"Looking for the key `{key}` in \"{isBut.strip()}\"...")
        # print(re.search(r'\b' + re.escape(key) + r'\b', isBut, re.IGNORECASE))
        if ' but ' in text:
            if re.search(r'\b' + re.escape(key) + r'\b', isBut, re.IGNORECASE):
                # print(f"Returning alias {KEY_ALIASES.get(key) if category.get(KEY_ALIASES.get(key)) else None}")
                return KEY_ALIASES.get(key) if category.get(KEY_ALIASES.get(key)) else None
        if re.search(r'\b' + re.escape(key) + r'\b', isBut, re.IGNORECASE):
            # print(f"Returning alias {KEY_ALIASES.get(key) if category.get(KEY_ALIASES.get(key)) else None}")
            return KEY_ALIASES.get(key) if category.get(KEY_ALIASES.get(key)) else None
    return None

def extract_fit_size(description: str, category: dict) -> str | None:
    """Parses listing description, handling 'but' contrast phrases and direct fit triggers."""
    if not description:
        return None

    FIT_TRIGGER_PATTERN = re.compile(
        r'\b(fits?\s+(like\s+a\s+|like\s+)?|cut\s+(more\s+like\s+a\s+|more\s+like\s+|like\s+a\s+|like\s+)?|sold\s+as\s+(a\s+)?|tag\s+says\s+)',
        re.IGNORECASE
    )

    clauses = re.split(r'[.;!]', description.lower())
    # print(f"Description")
    # print(f"    {clauses[0]}")
    # print(f"    {clauses[1]}")
    # print(f"    {clauses[2]}")
    # print(f"    {clauses[3]}")

    for clause in clauses:
        if FIT_TRIGGER_PATTERN.search(clause):
            extracted_size = find_size_in_text(clause, category)
            if extracted_size:
                # print(f"     {extracted_size}")
                return extracted_size

    return None

def extract_target_size(query_or_filter: str, category: str) -> str | None:
    """Reuses find_size_in_text to get target size from query or filter string."""
    return find_size_in_text(query_or_filter, category)


def get_base_size(category: str, raw_size: str) -> str | None:
    """Finds which standard base size key (e.g. 's', 'm') a raw size string belongs to."""
    if not raw_size:
        return None

    raw = raw_size.strip().lower()

    cat_map = CATEGORY_SIZE_TOKENS.get(category.lower(), {})
    for key, tokens in cat_map.items():
        # print(f"get_base_size::CATEGORY_SIZE_TOKENS.get({category}[{key}])")
        # print(f"     Index Size:      {key}")
        # print(f"     Aliases:         {tokens}")
        # print(f"     Item Size:       {raw}")
        # print(f"     [Category Token Matches][Size Token Matches]:")
        # print(f"               {raw in tokens}               {key in SIZE_ORDER}")
        if raw in tokens and key in SIZE_ORDER:
            # print("\n\nFOUND KEY\n\n")
            return key

    return None


def compareSizes(category: str, item_size: str, target_size: str) -> float:
    """
    Dynamically compares item_size (base) to target_size across size distances:
    - 3.0 pts: Exact size match (distance 0)
    - 1.5 pts: 1 size smaller or larger (distance 1)
    - 0.75 pts: 2 sizes smaller or larger (distance 2)
    - 0.0 pts: Greater distance or non-standard match
    """
    if not item_size or not target_size:
        return 0.0

    # 1. Exact string match check
    if item_size.strip().lower() == target_size.strip().lower():
        return 3.0

    # 2. Extract base size keys on the ordered scale
    base = get_base_size(category, item_size)
    target = get_base_size(category, target_size)

    # If both sizes can be placed on the ordered scale, calculate index distance
    if base in SIZE_ORDER and target in SIZE_ORDER:
        distance = abs(SIZE_ORDER.index(base) - SIZE_ORDER.index(target))

        if distance == 0:
            return 3.0
        elif distance == 1:
            return 1.5
        elif distance == 2:
            return 0.75

    return 0.0


def scoreSize(category: str, listing: dict, target_size: str | None) -> float:
    # If buyer specified no size preference, do not add or subtract size points
    if not target_size or target_size.strip() == "":
        return 0.0

    raw_description = listing.get("description", "")
    tag_size = listing.get("size", "")

    # Extract true fit size or fall back to tag size
    extracted_fit = extract_fit_size(raw_description, category)
    effective_size = extracted_fit if extracted_fit else tag_size

    return compareSizes(category, effective_size, target_size)

def search_listings(
    description: str,
    size: str | None = None,
    max_price: float | None = None,
) -> list[dict]:
    """
    Search the listings data for items matching a description, and optionally a
    size and a price ceiling.

    This is the tool that doesn't call the model, which makes it the easiest one
    to test and the one to move onto MCP in unit 4.

    Args:
        description: keywords describing what the user wants
                     (e.g. "vintage graphic tee").
        size:        a size string to filter by, or None to skip size filtering.
                     Match case-insensitively — "M" should match "S/M".

                     ⚠️ Read the sizes in the data before you reach for a plain
                     substring test. `"s" in "us 9"` is True, and so is
                     `"l" in "xl"`. A filter that returns shoes when someone
                     asked for a small top reads like a broken search, and it
                     will quietly cost you in unit 4 when you test criterion 1.
                     What counts as a size match is part of your spec — decide
                     it and write it into your Tool Inventory.
        max_price:   maximum price, inclusive, or None to skip price filtering.

    Returns:
        A list of matching listing dicts, best match first.
        **Returns an empty list when nothing matches — an empty list, not None,
        and not an exception.** Your loop branches on this.

    Each listing dict has these fields:
        id, title, description, category, style_tags (list), size,
        condition, price (float), colors (list), brand (str or None), platform

    Note that `brand` is None for most listings. That is deliberate and
    realistic — thrift listings often have no brand. If something you write
    assumes a brand is always there, you will find out in unit 4.

    TODO:
        1. Load every listing with load_listings().
        2. Filter by max_price and by size, when each is provided.
        3. Score what's left by keyword overlap with `description`.
        4. Drop anything scoring zero.
        5. Sort by score, highest first, and return the listing dicts —
           at most config.SEARCH_RESULT_LIMIT of them.

    Test it from a terminal before you move on:
        python -c "from tools import search_listings; print(search_listings('graphic tee', max_price=30))"
    """
    # TODO: replace this with your implementation
    index = 0
    BM25SearchEngine = keywordScore.BM25SearchEngine
    listings = load_listings()
    if not listings: return []

    if not description:
        print(f"\nNo matching description in string"
              f"\nPlease enter a valid description i.e. 'white striped pants 30W under $40'\n")
        return []
    if not size:
        print(f"No size matching in string"
              f"\nPlease enter a valid size i.e. 'small shirt'\n")
        return []
    if not max_price:
        print(f"\n0 is not a valid price range"
              f"\nPlease enter a valid price range i.e under $30.\n")
        return []

    # B. Calculate Text Relevance Scores using BM25 Engine
    engine = BM25SearchEngine(listings)
    text_scores = engine.get_text_scores(description)
    
    matches = []
    for idx, listing in enumerate(listings):
        score = 0

        # Check price and skip if it is above max_price
        item_price = listing.get('price')
        item_category = listing.get('category')
        item_desc = listing.get('description')
        item_size = listing.get('size')

        item_sz = get_base_size(item_category, item_size)
        c = CATEGORY_SIZE_TOKENS.get(item_category)

        target_size = size if size else extract_fit_size(item_desc, c)
        if max_price > 0 and item_price > max_price: continue;
        
        base_text_score = text_scores[idx]
        size_score = scoreSize(c, listing, target_size)
        score = base_text_score + size_score

        if score != 0 and index < config.SEARCH_RESULT_LIMIT:
            index += 1
            matches.append({'id':listing.get('id'), 'score':round(score, 2), 'price':f"price is inclusive to {max_price}" if max_price else "no price cap", 'listing':listing})
    # used ai to help me understand how to use sort(key=lambda x: x['score'])
    return matches if matches.sort(key=lambda x: x['score'], reverse=True) == None else []

# lists = search_listings("y2k cute vintage graphic tee", "", 30
# print(lists[0].get('score'))
# print(lists)
# for i in lists:
#     print(i)
#     print()
# print("Found", len(lists), "items from listings that matched.\n")
# print("Highest score:", lists[0].get('score'), "from", lists[0].get('id'))
# print("Average score:", f"{sum([int(i.get('score')) for i in lists])/len(lists):.2f}")
# print("Lowest score:", lists[len(lists)-1].get('score'), "from", lists[len(lists)-1].get('id'))

# ── Tool 2: suggest_outfit ────────────────────────────────────────────────────

def suggest_outfit(new_item: dict, wardrobe: dict) -> str:
    """
    Given a thrifted item and the user's wardrobe, suggest one or two outfits.

    This one calls the model, through `generate()`. You don't need to think
    about rate limits — the adapter handles pacing for you.

    Args:
        new_item: a listing dict — the item the user is considering.
        wardrobe: a wardrobe dict with an 'items' key holding a list of items.
                  **It may be empty.** Handle that.

    Returns:
        A non-empty string with outfit suggestions.
        With an empty wardrobe, return general styling advice rather than
        raising or returning "". Unit 4 has you trigger the empty wardrobe on
        purpose, so decide now what it should do.

    TODO:
        1. Check whether wardrobe['items'] is empty.
        2. If it is, ask the model for general styling ideas for this item.
        3. If it isn't, format the wardrobe items into the prompt and ask for
           specific combinations naming pieces the user already owns.
        4. Return the model's response.

    Test it from a terminal before you move on:
        python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"
    """
    # TODO: replace this with your implementation
    # 1. Safely extract items list from wardrobe dict
    wardrobe_items = wardrobe.get("items", []) if wardrobe else []

    # Format new item details
    item_title = new_item.get("title", "Item")
    item_cat = new_item.get("category", "")
    item_tags = ", ".join(new_item.get("style_tags", []))
    item_desc = new_item.get("description", "")

    item_info = (
        f"NEW ITEM TO STYLE:\n"
        f"- Title: {item_title}\n"
        f"- Category: {item_cat}\n"
        f"- Style Tags: {item_tags}\n"
        f"- Description: {item_desc}"
    )

    system_instruction = (
        """
        You are a personal fashion stylist giving clear, helpful outfit suggestions.
        
        Rules:
        - Be extremely punchy and brief 2-4 sentences.
        - No long intros, fluff, or markdown headers (###).
        - Clearly list which items are pieces from the wardrobe and which are not. 
        - Distinguish the outfit suggestions clearly
        - Explicitly add the listing's source id for easier reference, i.e., lst_019 or w_001 for every item in the wardrobe.
        """
    )

    # 2. Check whether wardrobe['items'] is empty
    if not wardrobe_items:
        # Ask model for general styling advice
        prompt = (
            f"{item_info}\n\n"
            f"The user's wardrobe is currently empty. Provide 2 general styling ideas "
            f"and practical fashion advice on what general types of pieces (bottoms, "
            f"layers, shoes, accessories) pair best with this item."
        )
    else:
        # Format existing wardrobe items into prompt
        wardrobe_lines = []
        for idx, piece in enumerate(wardrobe_items, start=1):
            p_name = piece.get("name") or piece.get("title", f"Piece {idx}")
            p_cat = piece.get("category", "")
            p_tags = ", ".join(piece.get("style_tags", []))
            p_notes = piece.get("notes", "")

            details = [f"Category: {p_cat}"]
            if p_tags:
                details.append(f"Tags: {p_tags}")
            if p_notes:
                details.append(f"Notes: {p_notes}")

            wardrobe_lines.append(f"{idx}. {p_name} ({', '.join(details)})")

        formatted_wardrobe = "\n".join(wardrobe_lines)

        prompt = (
            f"{item_info}\n\n"
            f"USER'S EXISTING WARDROBE:\n"
            f"{formatted_wardrobe}\n\n"
            f"Suggest 1 or 2 specific complete outfits combining the new item with "
            f"pieces from the user's existing wardrobe. You must explicitly name the "
            f"specific pieces they already own in your outfit suggestions."
        )

    # 3. Call generate() and return response
    response = generate(
        prompt,
        system=system_instruction,
        temperature=config.TEMPERATURE
    )
    # Fallback guard to ensure non-empty string return
    return (
        response.strip()
        if (wardrobe != {} or response and response.strip())
        else f"General styling advice for {item_title}: Pair with neutral basics and complementary layers."
    )

# from utils.data_loader import get_example_wardrobe
# outfits = suggest_outfit(load_listings()[0], get_example_wardrobe())
# print(outfits)

# ── Tool 3: create_fit_card ───────────────────────────────────────────────────

def create_fit_card(outfit: str, new_item: dict) -> str:
    """
    Write a short caption someone would actually post about the find.

    This calls the model too.

    Args:
        outfit:   the outfit suggestion string from suggest_outfit().
        new_item: the listing dict for the item.

    Returns:
        A two-to-four sentence caption.
        If `outfit` is empty or whitespace, return a descriptive message rather
        than raising.

    The caption should read like a real post rather than a product description,
    mention the item and its price and platform once each, and be specific about
    the vibe.

    It should also come out **differently for different inputs**. If you run
    this three times on the same item and get three word-for-word identical
    strings, it's one of two things, and both are near the top of `config.py`:

        • CACHE_ENABLED — the adapter handed back an answer it already had
        • TEMPERATURE   — at 0.0 the model gives the same words every time

    TODO:
        1. Guard against an empty or whitespace-only `outfit`.
        2. Build a prompt with the item details and the outfit.
        3. Call generate() and return the response.

    Test it from a terminal before you move on:
        python -c "from tools import create_fit_card; from utils.data_loader import load_listings; print(create_fit_card('jeans and white sneakers', load_listings()[0]))"
    """
    # TODO: replace this with your implementation
    # 1. Guard against empty or whitespace-only outfit input
    if not outfit or not outfit.strip():
        title = new_item.get("title", "thrift find")
        price = new_item.get("price", "bargain")
        platform = new_item.get("platform", "the shop")
        return f"Just scored this amazing {title} for ${price} on {platform}! Can't wait to style it into a casual weekend outfit."

    # Extract metadata required by the spec
    title = new_item.get("title", "Item")
    price = new_item.get("price", "")
    platform = new_item.get("platform", "online")
    style_tags = ", ".join(new_item.get("style_tags", []))
    condition = new_item.get("condition", "")

    # 2. Construct the prompt
    system_instruction = (
        """
        You are a trendy thrift shopper writing an authentic social media post caption about a recent thrift find.
        You write short, high-energy social media captions for them.
        
        Rules:
        - Keep it under 2-5 short sentences.
        - Explicitly include the item title, price, and platform.
        - Tone: Casual, trendy, 1-2 emojis max. No fluff.
        """
    )

    prompt = (
        f"Write a 2-to-4 sentence social media caption about this thrifted item and how to wear it.\n\n"
        f"ITEM DETAILS:\n"
        f"- Title: {title}\n"
        f"- Price: ${price}\n"
        f"- Platform: {platform}\n"
        f"- Vibe/Style Tags: {style_tags}\n"
        f"- Condition: {condition}\n\n"
        f"OUTFIT IDEA TO MENTION:\n"
        f"{outfit}\n\n"
        f"REQUIREMENTS:\n"
        f"1. Each item must be 1 sentence each\n"
        f"2. Mention the item name, its price (${price}), and the platform ({platform}) exactly once each.\n"
        f"3. Be specific about the vibe and sound like a real person sharing a thrift haul post, not a store ad."
    )

    # 3. Call generate() with system instruction
    response = generate(prompt, system=system_instruction, temperature=config.TEMPERATURE)

    # Fallback return in case model gives empty response
    if not response or not response.strip():
        return f"Obsessed with this {title} I picked up for ${price} on {platform}! The vibe is immaculate and it pairs so well with {outfit[:30]}..."

    return response.strip()


# print(create_fit_card(outfits, load_listings()[0]))