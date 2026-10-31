# mermaid-diagram-generator

VS Code の Copilot 向けカスタムスキル。要件・ドキュメント・コードから Mermaid 図を作成・説明・レビュー・修復するためのスキルです。

## 概要

このスキルを有効にすると、Copilot エージェントが Mermaid 図を扱う際に以下のワークフローで動作するようになります。

- **作成 (create)**: 要件やコードから適切な図ファミリ(フローチャート、シーケンス、ER、状態、クラス、ガント等)を選んで図を生成
- **修復 (repair)**: 構文エラーのある図を、意味を保ったまま最小限の変更で修正
- **説明 (explain)**: 既存の図の要素と関係を、憶測を交えずに説明

レンダラー(GitHub、VS Code 拡張、Mermaid Live 等)や Mermaid バージョンによる構文の互換性差異も考慮します。

## ファイル構成

スキル本体は `skills/mermaid-diagram-generator/` にまとまっており、このフォルダをそのままコピーするだけでインストールできます。

```text
skills/
  mermaid-diagram-generator/
    SKILL.md                        スキル本体(ワークフロー、互換性ガイド、例、チェックリスト)
    references/
      diagram-families.md           図ファミリの選択ガイド(対応バージョン付き)
      flowchart-shapes.md           フローチャートシェイプのカタログ(対応バージョン付き)
```

## インストール

### ユーザースキルとして(全ワークスペースで有効)

リポジトリをクローンし、スキルフォルダをユーザースキルフォルダにコピーします。

```powershell
git clone https://github.com/Surfin3000GTRs/mermaid-diagram-generator.git
Copy-Item -Recurse mermaid-diagram-generator\skills\mermaid-diagram-generator "$env:USERPROFILE\.copilot\skills\mermaid-diagram-generator"
```

更新する場合は、既存のフォルダを削除してからコピーしてください。

```powershell
Remove-Item -Recurse "$env:USERPROFILE\.copilot\skills\mermaid-diagram-generator" -ErrorAction SilentlyContinue
Copy-Item -Recurse mermaid-diagram-generator\skills\mermaid-diagram-generator "$env:USERPROFILE\.copilot\skills\mermaid-diagram-generator"
```

### プロジェクトスキルとして(特定のリポジトリのみ有効)

対象リポジトリの `.github/skills/` に `skills/mermaid-diagram-generator/` フォルダを丸ごとコピーします。

配置後、VS Code で Copilot チャットを開き、Mermaid 図の作成・修復・説明を依頼するとスキルが自動的に読み込まれます。

## 使い方

チャットで以下のように依頼するだけで、スキルのワークフローが適用されます。

- 「この処理の流れを Mermaid のフローチャートにして」
- 「この Mermaid 図がレンダリングエラーになるので直して」
- 「このシーケンス図の内容を説明して」

## メンテナンス方針

- `SKILL.md` および `references/` の内容は英語で統一
- Mermaid の新しい図ファミリが追加されたら [diagram-families.md](./skills/mermaid-diagram-generator/references/diagram-families.md)、新しいシェイプが追加されたら [flowchart-shapes.md](./skills/mermaid-diagram-generator/references/flowchart-shapes.md) を更新
- バージョン依存の構文を扱う際は、公式ドキュメントで対応バージョンを確認してから記載

## ライセンス

[MIT](./LICENSE)
