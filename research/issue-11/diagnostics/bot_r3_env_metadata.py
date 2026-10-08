#!/usr/bin/env python3
"""Read-only public GitHub Environment metadata check for BOT R3.
Never requests Secrets APIs, never reads environment values, and never calls BOT.
"""
import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import urllib.error
import urllib.request

REPO = "nustanakritwithai/Thai-economic-"
ENVIRONMENT = "bot-statistics-r3"
API_ROOT = "https://api.github.com/repos/" + REPO + "/environments/" + ENVIRONMENT
ENV_URL = API_ROOT
POLICIES_URL = API_ROOT + "/deployment-branch-policies"
LIST_URL = "https://api.github.com/repos/" + REPO + "/environments?per_page=100"
MAX_BYTES = 32768

class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, request, fp, code, msg, headers, newurl):
        return None

def public_get(url):
    if url not in (ENV_URL, POLICIES_URL, LIST_URL):
        raise ValueError("GitHub metadata URL is not allowlisted")
    request = urllib.request.Request(url, headers={
        "Accept": "application/vnd.github+json",
        "User-Agent": "Thailand-Economic-OS-BOT-R3-Public-Policy-Check/0.1",
    })
    opener = urllib.request.build_opener(NoRedirect)
    try:
        with opener.open(request, timeout=8) as response:
            status = response.status
            if response.geturl() != url:
                return {"status": None, "body": None, "problem": "UNEXPECTED_REDIRECT"}
            payload = response.read(MAX_BYTES + 1)
            if len(payload) > MAX_BYTES:
                return {"status": status, "body": None, "problem": "RESPONSE_OVERSIZE"}
            if status != 200:
                return {"status": status, "body": None, "problem": "NON_200_METADATA"}
            try:
                document = json.loads(payload)
            except (ValueError, UnicodeDecodeError):
                return {"status": status, "body": None, "problem": "UNPARSEABLE_METADATA"}
            return {"status": status, "body": document, "problem": None}
    except urllib.error.HTTPError as exc:
        # Never retain error body, response headers, account/user names or exception text.
        return {"status": exc.code, "body": None, "problem": "METADATA_NOT_ACCESSIBLE_OR_ERROR"}
    except (urllib.error.URLError, TimeoutError, OSError, ValueError) as exc:
        return {"status": None, "body": None, "problem": type(exc).__name__}

def evaluate(environment, branch_policies=None):
    """Fail closed. Only public metadata controls, not BOT approval/secret/access proof."""
    result = {
        "schema_version": 1,
        "issue": 11, "project": "Thailand Economic OS",
        "evidence_kind": "PUBLIC_GITHUB_ENVIRONMENT_PROTECTION_METADATA_ONLY",
        "repository": REPO, "environment_name": ENVIRONMENT,
        "environment_http_status": environment.get("status"),
        "environment_list_http_status": None,
        "environment_list_complete": False,
        "environment_found_in_list": "UNKNOWN",
        "branch_policy_http_status": (branch_policies or {}).get("status"),
        "environment_retrievable": False,
        "required_reviewer_rule_present": False,
        "required_reviewer_count_positive": False,
        "prevent_self_review": "UNKNOWN",
        "admin_bypass_disabled": "UNKNOWN",
        "custom_branch_policies": False,
        "main_is_only_permitted_branch": False,
        "deployment_protection_metadata_pass": False,
        "bot_statistics_approved_access_verified": False,
        "bot_token_provisioned_or_checked": False,
        "github_secret_names_or_values_read": False,
        "github_credentials_used": False,
        "bot_http_requests": 0,
        "live_r3_request_authorized": False,
        "live_r3_executed": False,
        "day02_gate": "BLOCKED_CRITICAL_EVIDENCE",
        "classification": "BLOCKED_UNVERIFIED_ENVIRONMENT_PROTECTION",
        "rule": "UNKNOWN != PASS",
    }
    data = environment.get("body")
    if environment.get("status") != 200 or not isinstance(data, dict):
        return result
    if data.get("name") != ENVIRONMENT:
        return result
    result["environment_retrievable"] = True
    rules = data.get("protection_rules")
    if isinstance(rules, list):
        reviews = [x for x in rules if isinstance(x, dict) and x.get("type") == "required_reviewers"]
        if reviews:
            result["required_reviewer_rule_present"] = True
            result["required_reviewer_count_positive"] = any(
                isinstance(x.get("reviewers"), list) and len(x["reviewers"]) > 0 for x in reviews)
            result["prevent_self_review"] = any(x.get("prevent_self_review") is True for x in reviews)
    if isinstance(data.get("can_admins_bypass"), bool):
        result["admin_bypass_disabled"] = data["can_admins_bypass"] is False
    deployment = data.get("deployment_branch_policy")
    if isinstance(deployment, dict):
        result["custom_branch_policies"] = (
            deployment.get("protected_branches") is False and
            deployment.get("custom_branch_policies") is True)
    branches = (branch_policies or {}).get("body")
    if result["custom_branch_policies"] and (branch_policies or {}).get("status") == 200 and isinstance(branches, dict):
        policies = branches.get("branch_policies")
        if (isinstance(policies, list) and branches.get("total_count") == 1 and
                len(policies) == 1 and isinstance(policies[0], dict) and
                policies[0].get("name") == "main"):
            result["main_is_only_permitted_branch"] = True

    result["deployment_protection_metadata_pass"] = all(
        result[x] is True for x in (
            "required_reviewer_rule_present", "required_reviewer_count_positive",
            "prevent_self_review", "admin_bypass_disabled", "custom_branch_policies",
            "main_is_only_permitted_branch"
        )
    )
    result["classification"] = (
        "PUBLIC_PROTECTION_METADATA_PASS_ONLY_BOT_ENTITLEMENT_AND_SECRET_NOT_VERIFIED"
        if result["deployment_protection_metadata_pass"]
        else "BLOCKED_UNVERIFIED_ENVIRONMENT_PROTECTION"
    )
    return result

def collect(fetcher=public_get):
    env = fetcher(ENV_URL)
    policy = None
    listed = None
    details = env.get("body")
    # If exact environment GET is 404, read at most one public listing
    # to distinguish complete-list absence from inaccessible/unknown.
    if env.get("status") == 404:
        listed = fetcher(LIST_URL)
    # Otherwise inspect custom branch policies only if configured.
    elif env.get("status") == 200 and isinstance(details, dict):
        deployment = details.get("deployment_branch_policy")
        if (isinstance(deployment, dict) and
                deployment.get("protected_branches") is False and
                deployment.get("custom_branch_policies") is True):
            policy = fetcher(POLICIES_URL)
    output = evaluate(env, policy)
    if listed is not None:
        output["environment_list_http_status"] = listed.get("status")
        listing = listed.get("body")
        if listed.get("status") == 200 and isinstance(listing, dict):
            environments = listing.get("environments")
            count = listing.get("total_count")
            if (isinstance(environments, list) and isinstance(count, int)
                    and count == len(environments)):
                output["environment_list_complete"] = True
                is_listed = any(isinstance(x, dict) and x.get("name") == ENVIRONMENT
                                for x in environments)
                output["environment_found_in_list"] = is_listed
                output["classification"] = (
                    "BLOCKED_ENVIRONMENT_GET_404_BUT_LIST_CONTAINS_TARGET_INCONSISTENT"
                    if is_listed else "BLOCKED_TARGET_NOT_LISTED_IN_COMPLETE_PUBLIC_ENVIRONMENT_LIST"
                )
    output["checked_at_utc"] = datetime.now(timezone.utc).isoformat()
    output["runner"] = {
        "github_run_id": os.getenv("GITHUB_RUN_ID"),
        "commit_sha": os.getenv("GITHUB_SHA"),
    }
    output["fetch_count"] = 1 + (1 if policy is not None else 0) + (1 if listed is not None else 0)
    output["limitations"] = [
        "Metadata is publicly retrievable on some repositories and can be unavailable without authentication",
        "A standalone 404 is not proof of absence; a full public list of environments strengthens the same-time classification",
        "Required reviewer metadata does not establish a particular reviewer gave approval for a job",
        "No Secrets API, secret names/values, BOT portal account, Token, or live BOT requests checked",
        "A metadata pass alone CANNOT enable R3 or certify actual environment secret injection",
        "Existing secret-free research workflow remains offline-only",
    ]
    return output

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="bot-r3-environment-evidence")
    args = parser.parse_args()
    result = collect()
    target = Path(args.output_dir)
    target.mkdir(parents=True, exist_ok=True)
    (target / "environment-evidence.json").write_text(
        json.dumps(result, sort_keys=True, indent=2) + "\n", encoding="utf-8")
    (target / "summary.md").write_text(
        "# BOT R3 public GitHub Environment protection inspection\n\n"
        "Metadata result: " + result["classification"] + "\n\n"
        "Required reviewer rule: " + str(result["required_reviewer_rule_present"]) + "\n\n"
        "Prevent self-review: " + str(result["prevent_self_review"]) + "\n\n"
        "Admin bypass disabled: " + str(result["admin_bypass_disabled"]) + "\n\n"
        "Only main allowed: " + str(result["main_is_only_permitted_branch"]) + "\n\n"
        "BOT Approved Access: NOT VERIFIED. Secrets: NEVER READ. Live R3: BLOCKED.\n\n"
        "Day-02 Gate: BLOCKED_CRITICAL_EVIDENCE.\n\nUNKNOWN != PASS.\n",
        encoding="utf-8")
    # No response bodies, usernames, reviewer IDs or secret identifiers in output.
    print("BOT_R3_ENV_METADATA_EVIDENCE=" + json.dumps(result, sort_keys=True))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
