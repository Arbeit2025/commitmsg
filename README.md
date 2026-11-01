# コミット文メーカー（commitmsg）

Conventional Commits 形式のコミットメッセージ候補を作る小さなツールです。生成はテンプレート方式で、**外部AIは一切使っていません**（入力を外部に送信することもありません）。

## 使い方

- **種別**：feat / fix / docs / style / refactor / perf / test / chore から選びます。
- **スコープ**（任意）：auth や ui など、変更範囲を短く書きます。
- **概要**：変更内容を1行で書きます。
- **本文**（任意）：変更の理由や詳細を書きます。
- 「候補を作る」を押すと、3パターンの候補が表示されます。
  - 候補1：スコープ付き（`feat(auth): …`）
  - 候補2：スコープなし（`feat: …`）
  - 候補3：本文付き（1行目＋空行＋本文）
- 各候補にはコピーボタンがあります。

## ローカル実行

```bash
pip install -r requirements.txt
python app.py
# http://localhost:5000
```

## テスト

```bash
python -m unittest discover -s tests
```

## Render へのデプロイ

`render.yaml` 同梱。無料プラン（free）の Web Service としてデプロイできます（healthCheckPath: `/healthz`）。

## 制限事項（正直なところ）

- テンプレートに当てはめるだけなので、文章の推敲はしません。概要の文言は自分で考える必要があります。
- 破壊的変更の `!` やフッター（BREAKING CHANGE 等）には対応していません。
- 入力内容は保存されません（ページを閉じると消えます）。

## ライセンス

MIT License
