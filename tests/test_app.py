import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import app as app_module  # noqa: E402


class CommitMsgTest(unittest.TestCase):
    def setUp(self):
        self.client = app_module.app.test_client()

    def test_healthz(self):
        res = self.client.get("/healthz")
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()["status"], "ok")

    def test_index_ok(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        body = res.get_data(as_text=True)
        self.assertIn("コミット文メーカー", body)
        self.assertIn("外部AIは使っていません", body)

    def test_make_candidates(self):
        cands = app_module.make_candidates("feat", "auth", "ログインを追加", "理由は利便性向上")
        texts = [t for (_, t) in cands]
        self.assertEqual(len(cands), 3)
        self.assertEqual(texts[0], "feat(auth): ログインを追加")
        self.assertEqual(texts[1], "feat: ログインを追加")
        self.assertIn("理由は利便性向上", texts[2])
        self.assertTrue(texts[2].startswith("feat(auth): ログインを追加"))

    def test_post_generates(self):
        res = self.client.post(
            "/",
            data={"type": "fix", "scope": "ui", "summary": "ボタンのずれを修正", "body": ""},
        )
        body = res.get_data(as_text=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn("fix(ui): ボタンのずれを修正", body)
        self.assertIn("fix: ボタンのずれを修正", body)

    def test_invalid_type_falls_back(self):
        res = self.client.post(
            "/", data={"type": "unknown", "scope": "", "summary": "何か変更", "body": ""}
        )
        body = res.get_data(as_text=True)
        self.assertIn("feat: 何か変更", body)


if __name__ == "__main__":
    unittest.main()
