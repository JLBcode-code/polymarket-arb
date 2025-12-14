"""从 Polymarket 事件 slug 获取市场/代币 ID 的工具。

解析事件页面 `https://polymarket.com/event/<slug>` 并提取
市场 ID 和 clob 代币 ID（顺序遵循结果列表）。
"""

import json
import re
from datetime import datetime
from typing import Dict

import httpx


def fetch_market_from_slug(slug: str) -> Dict[str, str]:
    # 允许包含查询参数的 slug（例如，从浏览器复制）
    slug = slug.split("?")[0]
    url = f"https://polymarket.com/event/{slug}"
    resp = httpx.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=10)
    resp.raise_for_status()

    # 提取 __NEXT_DATA__ JSON 载荷
    m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', resp.text, re.DOTALL)
    if not m:
        raise RuntimeError("__NEXT_DATA__ payload not found on page")
    payload = json.loads(m.group(1))

    queries = payload.get("props", {}).get("pageProps", {}).get("dehydratedState", {}).get("queries", [])
    market = None
    for q in queries:
        data = q.get("state", {}).get("data")
        if isinstance(data, dict) and "markets" in data:
            for mk in data["markets"]:
                if mk.get("slug") == slug:
                    market = mk
                    break
        if market:
            break

    if not market:
        raise RuntimeError("Market slug not found in dehydrated state")

    clob_tokens = market.get("clobTokenIds") or []
    outcomes = market.get("outcomes") or []
    if len(clob_tokens) != 2 or len(outcomes) != 2:
        raise RuntimeError("Expected binary market with two clob tokens")

    return {
        "market_id": market.get("id", ""),
        "yes_token_id": clob_tokens[0],
        "no_token_id": clob_tokens[1],
        "outcomes": outcomes,
        "question": market.get("question", ""),
        "start_date": market.get("startDate"),
        "end_date": market.get("endDate"),
    }


def next_slug(slug: str) -> str:
    # 将尾部类似 epoch 的数字增加 900 秒（15分钟）
    m = re.match(r"(.+-)(\d+)$", slug)
    if not m:
        raise ValueError(f"Slug not in expected format: {slug}")
    prefix, num = m.groups()
    return f"{prefix}{int(num) + 900}"


def parse_iso(dt: str) -> datetime | None:
    if not dt:
        return None
    try:
        return datetime.fromisoformat(dt.replace("Z", "+00:00"))
    except Exception:
        return None


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python -m src.market_lookup <slug>")
        sys.exit(1)
    info = fetch_market_from_slug(sys.argv[1])
    print(json.dumps(info, indent=2))