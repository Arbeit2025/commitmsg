"""コミット文メーカー commitmsg

種別・スコープ・概要・本文を入力すると、Conventional Commits 形式の
コミットメッセージ候補を3パターン生成するツール。生成はすべて
テンプレートベースで、外部AIは使わない。単一ファイル Flask（DBなし）。
"""
import os

from flask import Flask, jsonify, render_template_string, request

app = Flask(__name__)

TYPES = ["feat", "fix", "docs", "style", "refactor", "perf", "test", "chore"]

TYPE_LABELS = {
    "feat": "feat（新機能）",
    "fix": "fix（バグ修正）",
    "docs": "docs（ドキュメント）",
    "style": "style（見た目・整形）",
    "refactor": "refactor（リファクタリング）",
    "perf": "perf（性能改善）",
    "test": "test（テスト）",
    "chore": "chore（雑務・設定）",
}


def make_candidates(ctype, scope, summary, body):
    """Conventional Commits 風の候補を3つ作る（スコープ付き／なし／本文付き）。"""
    scope = (scope or "").strip()
    summary = (summary or "").strip()
    body = (body or "").strip()
    header_scoped = f"{ctype}({scope}): {summary}" if scope else f"{ctype}: {summary}"
    header_plain = f"{ctype}: {summary}"
    with_body = header_scoped + "\n\n" + (body if body else "（本文未入力）")
    return [
        ("候補1：スコープ付き" if scope else "候補1：スコープ付き（未入力のため候補2と同じ）", header_scoped),
        ("候補2：スコープなし", header_plain),
        ("候補3：本文付き", with_body),
    ]


PAGE = """<!doctype html>
<html lang="ja"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>コミット文メーカー</title>
<style>body{font-family:sans-serif;max-width:680px;margin:2em auto;padding:0 1em}
textarea{width:100%;box-sizing:border-box}
.cand{background:#f6f8fa;border:1px solid #ccc;border-radius:8px;padding:.8em;margin:.8em 0}
.cand pre{white-space:pre-wrap;word-break:break-all;margin:.4em 0}
input[type=text]{width:100%;box-sizing:border-box}</style>
</head><body>
<h1>コミット文メーカー</h1>
<p>Conventional Commits 形式のコミットメッセージ候補を作ります。生成はテンプレート方式で、<strong>外部AIは使っていません</strong>。</p>
<form method="post" action="{{ url_for('index') }}">
  <div><label>種別
    <select name="type">{% for t in types %}<option value="{{ t }}"{% if t == form.type %} selected{% endif %}>{{ labels[t] }}</option>{% endfor %}</select></label></div>
  <div><label>スコープ（任意）<input type="text" name="scope" value="{{ form.scope }}" placeholder="例：auth、ui"></label></div>
  <div><label>概要<input type="text" name="summary" value="{{ form.summary }}" placeholder="例：ログイン画面にパスワード表示切替を追加" required></label></div>
  <div><label>本文（任意）</label><textarea name="body" rows="3" placeholder="変更の理由や詳細">{{ form.body }}</textarea></div>
  <button type="submit">候補を作る</button>
</form>

{% if candidates %}
<h2>候補</h2>
{% for label, text in candidates %}
<div class="cand">
  <strong>{{ label }}</strong>
  <pre id="cand{{ loop.index }}">{{ text }}</pre>
  <button type="button" onclick="copyText('cand{{ loop.index }}')">コピー</button>
</div>
{% endfor %}
<script>
function copyText(id) {
  const el = document.getElementById(id);
  if (navigator.clipboard) { navigator.clipboard.writeText(el.textContent); }
}
</script>
{% endif %}
</body></html>"""


@app.route("/healthz")
def healthz():
    return jsonify({"status": "ok"})


@app.route("/", methods=["GET", "POST"])
def index():
    form = {"type": "feat", "scope": "", "summary": "", "body": ""}
    candidates = None
    if request.method == "POST":
        form = {
            "type": request.form.get("type", "feat"),
            "scope": request.form.get("scope", ""),
            "summary": request.form.get("summary", ""),
            "body": request.form.get("body", ""),
        }
        if form["type"] not in TYPES:
            form["type"] = "feat"
        if form["summary"].strip():
            candidates = make_candidates(
                form["type"], form["scope"], form["summary"], form["body"]
            )
    return render_template_string(
        PAGE, types=TYPES, labels=TYPE_LABELS, form=form, candidates=candidates
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")))
