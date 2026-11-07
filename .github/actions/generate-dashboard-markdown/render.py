#!/usr/bin/env python3
"""Render the Integration Suite dashboard and the IFlow roles page as Markdown.

Same data, status rules and layout as generate-dashboard (index.html) and
generate-roles-page (roles.html), for repositories that cannot publish GitHub Pages
privately: the files are committed and GitHub renders them in the repository.

Usage: render.py <dashboard-data.json> <roles-data.json|-> <out-dir> [owner/repo]
Writes <out-dir>/README.md (dashboard) and, when roles data is given, <out-dir>/roles.md.
"""
import json
import sys
from pathlib import Path

SCOPE = ("ℹ️ This dashboard covers Integration Flow (IFlow) artifacts only. Other artifact "
         "types (Value Mappings, Script Collections, etc.) are not included.")


def cell(text):
    """Table-safe text: a | or line break would end the cell."""
    return str(text).replace("|", "\\|").replace("\n", " ")


def deploy_badge(v):
    return {"true": "✅ true", "false": "❌ false"}.get(str(v).lower() if v is not None else "", "—")


def loglevel_badge(v):
    if not v:
        return "—"
    return {"ERROR": "🔴 ERROR", "WARN": "🟡 WARN", "INFO": "🔵 INFO",
            "DEBUG": "🟢 DEBUG", "TRACE": "🟣 TRACE"}.get(v, v)


def runtime_badge(status, version):
    if not status:
        return "—"
    v = f" v{version}" if version else ""
    if status == "STARTED":
        return f"✅ STARTED{v}"
    if status == "ERROR":
        return f"🔴 ERROR{v}"
    if status == "NOT_DEPLOYED":
        return "⚫ N/A"
    return f"{status}{v}"


def format_badge(fmt):
    return {"new": "🟢 new", "old": "🟡 old"}.get(fmt, "⚪ none")


def is_true(v):
    return v is True or v == "true"


def is_false(v):
    return v is False or v == "false"


def iflow_flags(iflow, envs):
    e = [iflow.get("environments", {}).get(n) or {} for n in envs]
    error = any(x.get("runtimeStatus") == "ERROR" for x in e)
    active = [x.get("runtimeVersion") or None for x in e
              if x.get("runtimeStatus") not in (None, "", "NOT_DEPLOYED")]
    diff = len(set(active)) > 1
    mismatch = any(
        (is_true(x.get("deploy")) and x.get("runtimeStatus") in (None, "", "NOT_DEPLOYED"))
        or (is_false(x.get("deploy")) and x.get("runtimeStatus") == "STARTED")
        for x in e)
    return error, diff, mismatch


def header(title, data_generated, envs, repo, extra, nav_active):
    meta = []
    if repo:
        meta.append(f"📁 **{repo}**")
    meta.append(f"📅 {data_generated}")
    meta.append(f"🌍 {', '.join(envs)}")
    meta += extra
    nav = [("📊 Dashboard", "README.md"), ("🔑 IFlow Roles", "roles.md")]
    nav = " · ".join(f"**{t}**" if f == nav_active else f"[{t}]({f})" for t, f in nav)
    return [f"# {title}", "", " · ".join(meta), "", nav, ""]


def dashboard(data, repo):
    envs = data.get("environments") or []
    pkgs = data["packages"]
    s = data["summary"]
    btp = [p for p in pkgs if p["source"] == "btp"]
    no_git_pkgs = [p for p in btp if not p["gitConfig"]["found"]]
    no_git_iflows = [i for p in pkgs for i in p["iflows"]
                     if i.get("source") == "btp" and i.get("hasGitConfig") is False]
    partial = [p for p in btp if p["gitConfig"]["found"] and any(i.get("hasGitConfig") is False for i in p["iflows"])]

    pkg_label = f"📦 {s['btpPackageCount']} BTP packages"
    if s["gitOnlyPackageCount"]:
        pkg_label += f" (+{s['gitOnlyPackageCount']} Git-only)"
    out = header("📊 Integration Suite Dashboard", data["generated"], envs, repo, [pkg_label], "README.md")
    out += [f"> {SCOPE}", "", "## 📈 Summary", ""]
    cards = [(s["btpPackageCount"], "BTP Packages"), (len(no_git_pkgs) + len(partial), "Git Config Issues")]
    if s["gitOnlyPackageCount"]:
        cards.append((s["gitOnlyPackageCount"], "🔍 Git-only Packages"))
    out += ["| " + " | ".join(label for _, label in cards) + " |",
            "|" + "---|" * len(cards),
            "| " + " | ".join(f"**{n}**" for n, _ in cards) + " |", "",
            f"🔴 {len(no_git_pkgs)} packages missing entirely · ⚠️ {len(partial)} packages with missing IFlows", ""]
    if no_git_pkgs or no_git_iflows:
        out += [f"> ⚠️ **Action required:** {len(no_git_pkgs)} package(s) and {len(no_git_iflows)} IFlow(s) "
                "found on BTP have no Git deployment configuration.", ""]

    out += ["## 📦 Packages", ""]
    env_head = " | ".join(f"{n}<br><sub>Deploy · LogLevel · Runtime</sub>" for n in envs)
    git_only_divider = False
    for p in pkgs:
        if p["source"] == "git-only" and not git_only_divider:
            out += ["### 🔍 Git-Only Packages — exist in Git but not found on any BTP tenant", ""]
            git_only_divider = True
        flags = [iflow_flags(i, envs) for i in p["iflows"]]
        found = p.get("foundOnEnvironments") or []
        missing = [e for e in envs if e not in found] if p["source"] == "btp" else []
        missing_note = f" · 📦 **Not found on:** {', '.join(missing)}" if missing else ""
        fmt = f"Deployment JSON: {format_badge(p['gitConfig'].get('jsonFormat'))}"
        if any(f[0] for f in flags):
            icon, meta = "🔴", f"{fmt} · 🔴 Some IFlows have runtime ERROR status{missing_note}"
        elif any(f[2] for f in flags):
            icon, meta = "🔴", f"{fmt} · 🔴 Config mismatch: deployment config differs from BTP reality{missing_note}"
        elif not p["gitConfig"]["found"]:
            icon, meta = "❓", f"❓ **Not found in Git** — This package exists on BTP but has no deployment configuration{missing_note}"
        elif p["source"] == "git-only":
            icon, meta = "🔴", f"{fmt} · 🔴 Not found on any BTP tenant"
        elif missing:
            icon, meta = "⚠️", f"{fmt}{missing_note}"
        elif any(f[1] for f in flags):
            icon, meta = "⚠️", f"{fmt} · ⚠️ Some IFlows have different versions across stages{missing_note}"
        else:
            icon, meta = "✅", f"{fmt} · ✅ All good"

        out += ["<details>", f"<summary>{icon} 📦 <b>{cell(p['name'])}</b> (<code>{p['id']}</code>)</summary>", "",
                meta, "", f"| IFlow Name | IFlow ID | {env_head} |", "|---|---|" + "---|" * len(envs)]
        if not p["iflows"]:
            note = "⚠️ *No IFlows found — package not in Git*" if not p["gitConfig"]["found"] else "ℹ️ *No IFlows found*"
            out.append(f"| {note} | |" + " |" * len(envs))
        for i, (error, diff, mismatch) in zip(p["iflows"], flags):
            if error or mismatch:
                prefix = "🔴"
            elif i.get("hasGitConfig") is False:
                prefix = "❓"
            elif diff:
                prefix = "⚠️"
            else:
                prefix = "✅"
            cells = []
            for n in envs:
                if n in missing:
                    cells.append("📦 Not found")
                    continue
                e = i.get("environments", {}).get(n) or {}
                cells.append(" · ".join([deploy_badge(e.get("deploy")), loglevel_badge(e.get("logLevel")),
                                         runtime_badge(e.get("runtimeStatus"), e.get("runtimeVersion"))]))
            out.append(f"| {prefix} {cell(i['name'])} | `{i['id']}` | " + " | ".join(cells) + " |")
        out += ["", "</details>", ""]

    out += ["## 📋 Legend", "", "| | |", "|---|---|",
            "| ✅ | Deployed / Enabled / Started |",
            "| ❌ | Not deployed / Disabled |",
            "| ⚫ | Not available on runtime |",
            "| ⚠️ | No Git configuration found (BTP-only) / Different values across stages |",
            "| 🔴 | Error / ERROR log level |",
            "| 🟡 | Warning / Old JSON format |",
            "| 🔵 | INFO log level |",
            "| 🟢 | New JSON format |",
            "| 🔍 | Exists in Git but not found on BTP |",
            "| 📦 Not found | Package does not exist on this environment |",
            "| — | Not configured / Unknown |", "",
            "**JSON Format:** 🟢 new = Enhanced format with Environments overrides · 🟡 old = Legacy format with "
            "flat Deploy flag · ⚪ none = No deployment configuration found", "",
            "Deployment configuration goes in "
            "`IntegrationPackages/<PackageFolder>/Configuration/Deployment_INTEGRATION_FLOW.json`.", ""]
    return "\n".join(out)


def roles(data, repo):
    s = data["summary"]
    out = header("🔑 IFlow Roles", data["generated"], [data.get("devEnvironment", "")], repo, [], "roles.md")
    out += ["> ℹ️ Shows the configured userRole per IFlow. IFlows without a role are not listed.", "",
            "## 📈 Summary", ""]
    cards = [(s["iflowsWithRole"], "✅ Role Defined")]
    if s.get("iflowsParamUnresolved"):
        cards.append((s["iflowsParamUnresolved"], "🔴 Unresolved"))
    out += ["| " + " | ".join(label for _, label in cards) + " |", "|" + "---|" * len(cards),
            "| " + " | ".join(f"**{n}**" for n, _ in cards) + " |", ""]

    listed = [(p, [i for i in p["iflows"] if i["roleStatus"] in ("defined", "error")]) for p in data["packages"]]
    listed = [(p, i) for p, i in listed if i]
    if not listed:
        out += ["*No IFlows with a configured role.*", ""]
    for p, iflows in listed:
        n = len(iflows)
        out += [f"### 📦 {cell(p['name'])} · `{p['id']}` · {n} IFlow{'s' if n != 1 else ''}", "",
                "| IFlow Name | IFlow ID | User Role |", "|---|---|---|"]
        for i in iflows:
            icon = "✅" if i["roleStatus"] == "defined" else "🔴"
            ext = " (ext.)" if i.get("roleSource") == "param-resolved" else ""
            role = f"`{cell(i['userRole'])}`{ext}" if i["userRole"] else "—"
            out.append(f"| {icon} {cell(i['name'])} | `{i['id']}` | {role} |")
        out.append("")
    out += ["---", "", "✅ Role defined · 🔴 Externalized parameter not found in ConfigParams · "
            "(ext.) = value resolved from externalized parameter", ""]
    return "\n".join(out)


def main():
    dash_file, roles_file, out_dir = sys.argv[1:4]
    repo = sys.argv[4] if len(sys.argv) > 4 else ""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    data = json.loads(Path(dash_file).read_text(encoding="utf-8"))
    (out / "README.md").write_text(dashboard(data, repo), encoding="utf-8")
    written = ["README.md"]
    if roles_file != "-" and Path(roles_file).is_file():
        rdata = json.loads(Path(roles_file).read_text(encoding="utf-8"))
        (out / "roles.md").write_text(roles(rdata, repo), encoding="utf-8")
        written.append("roles.md")
    print(f"Wrote {', '.join(written)} to {out}")


if __name__ == "__main__":
    main()
