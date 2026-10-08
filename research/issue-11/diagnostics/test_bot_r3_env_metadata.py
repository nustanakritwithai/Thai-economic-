"""Offline mocked GitHub Environment security metadata tests; zero real HTTP."""
import json
import unittest
from bot_r3_env_metadata import ENV_URL, POLICIES_URL, evaluate, collect

def protected():
    return {
        "status": 200, "body": {
            "name": "bot-statistics-r3",
            "protection_rules": [{
                "type": "required_reviewers",
                "prevent_self_review": True,
                "reviewers": [{"login": "SECRET_PERSON_SHOULD_NOT_LOG", "id": 999}],
            }],
            "can_admins_bypass": False,
            "deployment_branch_policy": {
                "protected_branches": False, "custom_branch_policies": True
            }
        }, "problem": None,
    }

def branch_main():
    return {
        "status": 200,
        "body": {"total_count": 1, "branch_policies": [{"name": "main", "id": 4444}]},
        "problem": None,
    }

class Tests(unittest.TestCase):
    def test_environment_404_not_assumed_absent(self):
        r=evaluate({"status":404,"body":None,"problem":"not accessible"})
        self.assertFalse(r["environment_retrievable"])
        self.assertEqual(r["classification"], "BLOCKED_UNVERIFIED_ENVIRONMENT_PROTECTION")
        self.assertFalse(r["live_r3_request_authorized"])
        self.assertFalse(r["bot_token_provisioned_or_checked"])

    def test_reviewer_required_does_not_read_identity(self):
        r=evaluate(protected(),branch_main())
        self.assertTrue(r["deployment_protection_metadata_pass"])
        self.assertFalse(r["live_r3_request_authorized"])
        self.assertNotIn("SECRET_PERSON_SHOULD_NOT_LOG",json.dumps(r))
        self.assertNotIn("999",json.dumps(r))
        self.assertFalse(r["github_secret_names_or_values_read"])

    def test_prevent_self_review_is_required(self):
        o=protected()
        o["body"]["protection_rules"][0]["prevent_self_review"]=False
        self.assertFalse(evaluate(o,branch_main())["deployment_protection_metadata_pass"])

    def test_missing_admin_bypass_setting_unknown(self):
        o=protected()
        del o["body"]["can_admins_bypass"]
        r=evaluate(o,branch_main())
        self.assertEqual(r["admin_bypass_disabled"],"UNKNOWN")
        self.assertFalse(r["deployment_protection_metadata_pass"])

    def test_branch_wildcard_rejected(self):
        b=branch_main()
        b["body"]["branch_policies"][0]["name"]="main*"
        self.assertFalse(evaluate(protected(),b)["main_is_only_permitted_branch"])

    def test_multiple_branches_rejected(self):
        b=branch_main()
        b["body"]["total_count"]=2
        b["body"]["branch_policies"].append({"name":"feature"})
        self.assertFalse(evaluate(protected(),b)["deployment_protection_metadata_pass"])

    def test_missing_branch_policy_payload_blocks(self):
        r=evaluate(protected(),{"status":403,"body":None,"problem":"inaccessible"})
        self.assertFalse(r["deployment_protection_metadata_pass"])

    def test_repo_metadata_not_other_repo(self):
        o=protected()
        o["body"]["name"]="unrelated"
        self.assertFalse(evaluate(o,branch_main())["environment_retrievable"])

    def test_no_auth_external_get_probes_bounded_paths(self):
        urls=[]
        def fetcher(url):
            urls.append(url)
            return protected() if url == ENV_URL else branch_main()
        r=collect(fetcher=fetcher)
        self.assertEqual(urls,[ENV_URL,POLICIES_URL])
        self.assertEqual(r["fetch_count"],2)
        self.assertEqual(r["bot_http_requests"],0)
        self.assertFalse(r["live_r3_executed"])

    def test_no_branch_fetch_without_custom_policy(self):
        urls=[]
        o=protected()
        o["body"]["deployment_branch_policy"]={"protected_branches":True,"custom_branch_policies":False}
        def fetcher(url):
            urls.append(url)
            return o
        r=collect(fetcher=fetcher)
        self.assertEqual(urls,[ENV_URL])
        self.assertEqual(r["fetch_count"],1)
        self.assertFalse(r["deployment_protection_metadata_pass"])

if __name__=="__main__":
    unittest.main()
