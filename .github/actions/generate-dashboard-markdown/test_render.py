"""Self-check for render.py: python3 test_render.py (no dependencies)."""
import render

ENVS = ["DEV", "PRD"]


def iflow(iid, dev, prd, git=True):
    return {"id": iid, "name": iid, "source": "btp", "hasGitConfig": git,
            "environments": {"DEV": dev, "PRD": prd}}


def env(status=None, version="", deploy=None, log=None):
    return {"deploy": deploy, "logLevel": log, "runtimeStatus": status, "runtimeVersion": version}


def pkg(pid, iflows, found=ENVS, git=True, source="btp"):
    return {"id": pid, "name": pid, "source": source, "foundOnEnvironments": found,
            "gitConfig": {"found": git, "jsonFormat": "new" if git else None}, "iflows": iflows}


ok = env("STARTED", "1.0.0", True, "INFO")
data = {"generated": "2026-11-06T00:00:00Z", "environments": ENVS, "environmentUrls": {},
        "summary": {"btpPackageCount": 6, "gitOnlyPackageCount": 1, "totalPackageCount": 7},
        "packages": [
            pkg("Good", [iflow("a", ok, ok)]),
            pkg("Err", [iflow("b", env("ERROR", "1.0.0"), ok)]),
            pkg("Mismatch", [iflow("c", env("NOT_DEPLOYED", deploy=True), ok)]),
            pkg("Diff", [iflow("d", ok, env("STARTED", "2.0.0", True))]),
            pkg("NoGit", [iflow("e", ok, ok, git=False)], git=False),
            pkg("DevOnly", [iflow("f", ok, env())], found=["DEV"]),
            pkg("GitOnly|x", [], found=[], source="git-only"),
        ]}

md = render.dashboard(data, "org/repo")
line = {p: next(l for l in md.splitlines() if f"<code>{p}</code>" in l) for p in
        ["Good", "Err", "Mismatch", "Diff", "NoGit", "DevOnly", "GitOnly|x"]}
assert line["Good"].startswith("<summary>✅"), line["Good"]
assert line["Err"].startswith("<summary>🔴")
assert line["Mismatch"].startswith("<summary>🔴")
assert line["Diff"].startswith("<summary>⚠️")
assert line["NoGit"].startswith("<summary>❓")
assert line["DevOnly"].startswith("<summary>⚠️")
assert line["GitOnly|x"].startswith("<summary>🔴")
assert "<b>GitOnly\\|x</b>" in md                      # | escaped for tables
assert "🔍 Git-Only Packages" in md
assert "| ✅ a | `a` | ✅ true · 🔵 INFO · ✅ STARTED v1.0.0 | ✅ true · 🔵 INFO · ✅ STARTED v1.0.0 |" in md
assert "| ✅ f | `f` | ✅ true · 🔵 INFO · ✅ STARTED v1.0.0 | 📦 Not found |" in md
assert "**Not found on:** PRD" in md
assert "1 packages missing entirely" in md and "1 IFlow(s)" in md
assert "**[📊 Dashboard" not in md and "**📊 Dashboard** · [🔑 IFlow Roles](roles.md)" in md

roles = {"generated": "g", "devEnvironment": "DEV",
         "summary": {"iflowsWithRole": 1, "iflowsParamUnresolved": 1},
         "packages": [{"id": "P", "name": "P", "iflows": [
             {"id": "x", "name": "x", "userRole": "ESBMessaging.send", "roleStatus": "defined", "roleSource": "param-resolved"},
             {"id": "y", "name": "y", "userRole": "{{role}}", "roleStatus": "error", "roleSource": "param-unresolved"},
             {"id": "z", "name": "z", "userRole": "", "roleStatus": "none", "roleSource": "direct"}]},
             {"id": "Q", "name": "Q", "iflows": [{"id": "q", "name": "q", "userRole": "", "roleStatus": "not-in-git", "roleSource": "none"}]}]}
rmd = render.roles(roles, "org/repo")
assert "| ✅ x | `x` | `ESBMessaging.send` (ext.) |" in rmd
assert "| 🔴 y | `y` | `{{role}}` |" in rmd
assert "`z`" not in rmd and "📦 Q" not in rmd           # no role / not in git: not listed
assert "· 2 IFlows" in rmd and "🔴 Unresolved" in rmd
print("render.py self-check passed")
