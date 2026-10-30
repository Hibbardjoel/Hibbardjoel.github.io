#!/usr/bin/env python3
"""Rank master-resume evidence against a job description.

  python3 tools/score_jd.py jd.txt [data/master.json] > match.json

This is a deterministic first pass, not the final tailoring. It shows which
bullets carry the JD's language and which JD terms have no evidence (gaps), so
the rewrite step stays honest: reorder and reword real work, never invent it.
"""
import json, re, sys, collections, pathlib

# JD phrasing -> master tag vocabulary. Extend as new JDs come in.
SYNONYMS = {
    "digital transformation": ["modernization", "modernize", "transformation", "legacy"],
    "platform migration": ["migration", "migrate", "re-platform", "cutover"],
    "data architecture": ["data model", "data modeling", "schema", "database design", "data platform"],
    "PostgreSQL": ["postgres", "postgresql", "rds", "relational database", "sql"],
    "RBAC": ["role-based", "access control", "permissions", "entitlements", "least privilege", "iam"],
    "security": ["security", "zero trust", "secure", "cyber"],
    "governance": ["governance", "standards", "policy", "controls"],
    "compliance": ["compliance", "regulatory", "audit", "sox", "hipaa", "fedramp"],
    "React": ["react", "jsx", "front-end", "frontend", "javascript", "typescript"],
    "ToolJet": ["low-code", "low code", "tooljet", "retool", "internal tools"],
    "Power Apps": ["power apps", "power platform", "power automate"],
    "SharePoint": ["sharepoint", "microsoft 365", "office 365", "m365"],
    "Microsoft Graph": ["graph api", "microsoft graph"],
    "data pipeline": ["pipeline", "etl", "elt", "ingestion", "integration"],
    "AI": ["ai", "machine learning", "llm", "genai", "generative", "automation"],
    "CI/CD": ["ci/cd", "devops", "github actions", "release", "deployment"],
    "change management": ["change management", "adoption", "enablement", "organizational change"],
    "training": ["training", "learning", "l&d", "lms", "instructional"],
    "stakeholder management": ["stakeholder", "cross-functional", "executive", "c-suite", "leadership team"],
    "program management": ["program management", "portfolio", "pmo", "roadmap", "delivery"],
    "dashboards": ["dashboard", "kpi", "metrics", "reporting", "analytics", "bi"],
    "healthcare": ["healthcare", "clinical", "medical", "behavioral health", "mental health", "patient"],
    "government": ["government", "dod", "federal", "public sector", "clearance"],
    "leadership": ["lead", "leader", "director", "head of", "manage teams", "people management"],
    "P&L": ["budget", "p&l", "financial ownership", "cost center"],
    "people management": ["people management", "direct reports", "team of", "manage a team", "hiring"],
    "HIPAA": ["hipaa", "phi", "protected health"],
    "contract negotiation": ["vendor", "contract", "procurement", "negotiat"],
}

def terms_in(jd: str):
    jd_l = jd.lower()
    hits = collections.Counter()
    for tag, keys in SYNONYMS.items():
        for k in keys + [tag.lower()]:
            n = len(re.findall(r"(?<![a-z])" + re.escape(k), jd_l))
            if n: hits[tag] += n
    return hits

def main():
    jd = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
    master = json.loads(pathlib.Path(sys.argv[2] if len(sys.argv) > 2 else "data/master.json").read_text())
    jd_terms = terms_in(jd)
    ranked, covered = [], set()
    for job in master["experience"]:
        for b in job["bullets"]:
            tags = {t.lower() for t in b["tags"]}
            overlap = [t for t in jd_terms if t.lower() in tags]
            score = sum(jd_terms[t] for t in overlap) * (b.get("weight", 5) / 10)
            covered.update(overlap)
            ranked.append({"id": b["id"], "job": job["id"], "score": round(score, 2), "matched": overlap})
    ranked.sort(key=lambda r: -r["score"])
    out = {
        "jd_terms": jd_terms.most_common(),
        "ranked_bullets": ranked,
        "gaps": [t for t in jd_terms if t not in covered],  # JD asks, master has no tagged evidence
    }
    json.dump(out, sys.stdout, indent=2)

if __name__ == "__main__":
    main()
