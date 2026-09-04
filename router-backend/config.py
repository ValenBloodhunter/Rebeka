"""
config.py
Holds pricing, settings, and cost/token helper functions for the
LLM Cost Optimizer backend. All values are MOCKED - no API keys.
"""

# ---------------------------------------------------------------------------
# TIER DEFINITIONS
# Prices are USD per 1,000,000 tokens (locked numbers from the spec).
# ---------------------------------------------------------------------------
TIERS = {
    "cheap": {
        "name": "Cheap Tier (Small Model)",
        "input_price_per_1m": 0.25,
        "output_price_per_1m": 1.25,
    },
    "frontier": {
        "name": "Frontier Tier (Expensive Model)",
        "input_price_per_1m": 3.00,
        "output_price_per_1m": 15.00,
    },
}

# Cached input tokens are billed at 10% of the normal input price.
CACHED_INPUT_DISCOUNT = 0.10

# ---------------------------------------------------------------------------
# MUTABLE SETTINGS
# These can be changed at runtime via POST /config.
# ---------------------------------------------------------------------------
SETTINGS = {
    "threshold": 0.45,
    "cache_enabled": True,
    "mode": "mock",
}


def estimate_tokens(text: str) -> int:
    """
    Rough token estimate: 1 token ~= 4 characters.
    """
    return len(text) // 4


def calculate_cost(tier: str, tokens_in: int, tokens_out: int, cached_tokens: int = 0) -> float:
    """
    Calculate the USD cost for a request against a given tier.

    - tier: "cheap" or "frontier"
    - tokens_in: total input tokens for this request
    - tokens_out: total output tokens for this request
    - cached_tokens: how many of the input tokens were served from cache
      (billed at CACHED_INPUT_DISCOUNT of the normal input price)
    """
    if tier not in TIERS:
        raise ValueError(f"Unknown tier: {tier}")

    pricing = TIERS[tier]
    input_price = pricing["input_price_per_1m"]
    output_price = pricing["output_price_per_1m"]

    # Split input tokens into cached vs non-cached
    cached_tokens = min(cached_tokens, tokens_in)
    normal_input_tokens = tokens_in - cached_tokens

    normal_input_cost = (normal_input_tokens / 1_000_000) * input_price
    cached_input_cost = (cached_tokens / 1_000_000) * input_price * CACHED_INPUT_DISCOUNT
    output_cost = (tokens_out / 1_000_000) * output_price

    total_cost = normal_input_cost + cached_input_cost + output_cost
    return total_cost


if __name__ == "__main__":
    # Sanity check: sample cost for both tiers with the same token counts
    sample_tokens_in = 1000
    sample_tokens_out = 300
    sample_cached_tokens = 200

    print("=== Sample Cost Sanity Check ===")
    print(f"tokens_in={sample_tokens_in}, tokens_out={sample_tokens_out}, "
          f"cached_tokens={sample_cached_tokens}\n")

    for tier_key in TIERS:
        cost = calculate_cost(
            tier=tier_key,
            tokens_in=sample_tokens_in,
            tokens_out=sample_tokens_out,
            cached_tokens=sample_cached_tokens,
        )
        print(f"{TIERS[tier_key]['name']} ({tier_key}): ${cost:.6f}")

    print("\n=== Token Estimate Sanity Check ===")
    sample_text = "This is a sample piece of text used to test estimate_tokens()."
    print(f"Text: {sample_text!r}")
    print(f"Estimated tokens: {estimate_tokens(sample_text)}")