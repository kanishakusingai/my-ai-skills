#!/usr/bin/env python3
"""Look up the Amazon connector and prepare a read-only workflow for Codex."""
import argparse
import json
from pathlib import Path
import re
import sys


GUIDES = Path(__file__).resolve().parents[1] / "references"
PREFIX = "mcp__codex_apps__amazon_"
RECIPES = {
    "connection": "Check marketplace, server version and the approval mechanism.",
    "sku-review": "Inspect listing issues, product images and the competitive offer for a SKU.",
    "order-money": "Compare an order and its financial transactions.",
    "feed-review": "Inspect processing and per-SKU results for one bulk feed.",
    "report-watch": "Poll one report to a terminal state or the selected check limit.",
}


def catalog():
    entries = {}
    for guide in sorted(GUIDES.glob("*.md")):
        sections = re.split(r"^## ([a-z][a-z0-9_]+)\s*$", guide.read_text(encoding="utf-8"), flags=re.M)
        for name, body in zip(sections[1::2], sections[2::2]):
            if name in entries:
                raise ValueError(f"Duplicate guide entry: {name}")
            entries[name] = (guide.stem, body.strip())
    return entries


def make_plan(args, parser):
    requirements = {"sku-review": "sku", "order-money": "order_id",
                    "feed-review": "feed_id", "report-watch": "report_id"}
    required = requirements.get(args.recipe)
    for key in requirements.values():
        value = getattr(args, key)
        if key == required and not (value and value.strip()):
            parser.error(f"{args.recipe} requires --{key.replace('_', '-')}")
        if key != required and value is not None:
            parser.error(f"--{key.replace('_', '-')} does not apply to {args.recipe}")
    if args.recipe != "report-watch" and args.checks is not None:
        parser.error("--checks applies only to report-watch")
    calls = {
        "connection": [("server_info", {})],
        "sku-review": [("listings_get", {"sku": args.sku, "includeAttributes": True}),
                       ("listing_images", {"skus": [args.sku]}),
                       ("pricing_competitive", {"sku": args.sku})],
        "order-money": [("orders_get", {"orderId": args.order_id}),
                        ("finances_order", {"orderId": args.order_id})],
        "feed-review": [("feeds_status", {"feedId": args.feed_id})],
        "report-watch": [("reports_status", {"reportId": args.report_id})],
    }[args.recipe]
    return {"recipe": args.recipe, "calls": [{"tool": name, "args": data} for name, data in calls],
            "checks": args.checks or 3 if args.recipe == "report-watch" else 1}


# The host provides tools, text and setTimeout. Keep the raw connector response
# for failures, unrecognised statuses and partial data.
HOST = r"""
async function runStep(step) {
  const qualified = "mcp__codex_apps__amazon_" + step.tool;
  try {
    if (typeof tools[qualified] !== "function") {
      return {tool: step.tool, ok: false, error: "Tool unavailable in this session"};
    }
    const response = await tools[qualified](step.args);
    return {tool: step.tool, ok: !response.isError,
            result: response.structuredContent ?? response.content};
  } catch (error) {
    return {tool: step.tool, ok: false, error: String(error)};
  }
}
function reportState(result) {
  const known = /^(IN_QUEUE|IN_PROGRESS|DONE|CANCELLED|FATAL)$/;
  for (const candidate of [result?.processingStatus, result?.status]) {
    if (typeof candidate === "string" && known.test(candidate)) return candidate;
  }
  const blocks = Array.isArray(result) ? result : [];
  const message = blocks.filter(x => x.type === "text").map(x => x.text).join("\n");
  const states = [...new Set(message.match(/\b(?:IN_QUEUE|IN_PROGRESS|DONE|CANCELLED|FATAL)\b/g) || [])];
  return states.length === 1 ? states[0] : "UNKNOWN";
}
if (plan.recipe === "report-watch") {
  for (let i = 1; i <= plan.checks; i++) {
    const item = await runStep(plan.calls[0]);
    const state = item.ok ? reportState(item.result) : "ERROR";
    text({check: i, reportId: plan.calls[0].args.reportId, state, ...item});
    if (!["IN_QUEUE", "IN_PROGRESS"].includes(state) || i === plan.checks) break;
    await new Promise(resolve => setTimeout(resolve, 10000));
  }
} else {
  const results = await Promise.all(plan.calls.map(runStep));
  text({recipe: plan.recipe, results});
}
"""


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    cmd = parser.add_subparsers(dest="command", required=True)
    search = cmd.add_parser("search", help="Search tool names and descriptions; omit terms to list all.")
    search.add_argument("terms", nargs="*")
    show = cmd.add_parser("show", help="Print purpose, example and full input signature.")
    show.add_argument("name")
    run = cmd.add_parser("workflow", help="Print a plan or executable Codex host code.")
    run.add_argument("recipe", choices=RECIPES, help="; ".join(f"{k}: {v}" for k, v in RECIPES.items()))
    for flag in ("sku", "order-id", "feed-id", "report-id"):
        run.add_argument("--" + flag)
    run.add_argument("--checks", type=int, choices=range(1, 7), metavar="1..6")
    run.add_argument("--emit-js", action="store_true", help="Print JavaScript for the connected Codex host.")
    args = parser.parse_args()
    entries = catalog()
    if args.command == "show":
        name = args.name.removeprefix(PREFIX)
        if name not in entries:
            parser.error(f"Unknown tool: {name}. Try search.")
        print(name + "\n\n" + entries[name][1])
    elif args.command == "search":
        terms = " ".join(args.terms).casefold().split()
        hits = []
        for name, (group, body) in entries.items():
            purpose = body.split("\n\n", 1)[0]
            words = (name.replace("_", " ") + " " + name + " " + group + " " + purpose).casefold()
            if all(term in words for term in terms):
                hits.append((sum(term in name for term in terms), name, group, purpose))
        for _, name, group, purpose in sorted(hits, key=lambda hit: (-hit[0], hit[1])):
            print(f"{name} [{group}]  {purpose}")
        if not hits:
            print("No matches. Try fewer terms.", file=sys.stderr)
            return 1
    else:
        plan = make_plan(args, parser)
        if any(step["tool"] not in entries for step in plan["calls"]):
            parser.error("Workflow references a missing tool guide.")
        value = json.dumps(plan, ensure_ascii=True, indent=2)
        print("const plan = " + value + ";\n" + HOST if args.emit_js else value)
    return 0


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    raise SystemExit(main())
