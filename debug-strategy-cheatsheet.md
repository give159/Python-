# 🐛 Pythonデバッグ完全チートシート

## 📋 デバッグ手法の使い分け

| 状況 | 推奨手法 | 理由 |
|------|---------|------|
| 簡単な値確認 | `print()` | 最速・最もシンプル |
| 本番環境 | `logging` | ログレベルで制御可能 |
| 複雑なバグ | `breakpoint()` | 対話的に調査できる |
| IDE使用時 | VSCode デバッガー | GUIで見やすい |
| CI/CD環境 | `logging` + テスト | 自動化可能 |
| パフォーマンス問題 | `cProfile` | 実行時間を計測 |

---

## 🚀 VSCode デバッグ設定

### launch.json の基本設定

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: 現在のファイル",
            "type": "python",
            "request": "launch",
            "program": "${file}",
            "console": "integratedTerminal",
            "justMyCode": true
        },
        {
            "name": "Python: モジュール",
            "type": "python",
            "request": "launch",
            "module": "app.main",
            "console": "integratedTerminal"
        },
        {
            "name": "Python: Django",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": ["runserver"],
            "django": true
        },
        {
            "name": "Python: Flask",
            "type": "python",
            "request": "launch",
            "module": "flask",
            "env": {
                "FLASK_APP": "app.py",
                "FLASK_ENV": "development"
            },
            "args": ["run", "--no-debugger", "--no-reload"],
            "jinja": true
        },
        {
            "name": "Python: FastAPI",
            "type": "python",
            "request": "launch",
            "module": "uvicorn",
            "args": ["app.main:app", "--reload"],
            "jinja": true
        }
    ]
}
```

### VSCode ショートカットキー

| 操作 | Windows/Linux | Mac |
|------|---------------|-----|
| デバッグ開始 | `F5` | `F5` |
| 停止 | `Shift+F5` | `Shift+F5` |
| ステップオーバー | `F10` | `F10` |
| ステップイン | `F11` | `F11` |
| ステップアウト | `Shift+F11` | `Shift+F11` |
| 続行 | `F5` | `F5` |
| ブレークポイント切替 | `F9` | `F9` |
| 条件付きブレークポイント | 右クリック → 条件付き | 右クリック → 条件付き |

---

## 📝 logging レベルの使い分け

### ログレベル一覧

```python
DEBUG    = 10  # 詳細な診断情報（開発時のみ）
INFO     = 20  # 正常な動作の確認
WARNING  = 30  # 想定外だが処理は続行
ERROR    = 40  # エラー発生、機能の一部が動作不可
CRITICAL = 50  # 致命的エラー、システム停止
```

### 実務での使い分け例

```python
# DEBUG: 変数の値、ループの進行状況
logger.debug(f"変数x={x}, y={y}, z={z}")
logger.debug(f"ループ {i}/{total} 処理中")

# INFO: 処理の開始・終了、正常完了
logger.info("アプリケーション起動")
logger.info("データベース接続成功")
logger.info(f"ファイル {filename} を処理完了")

# WARNING: 推奨されない使い方、非推奨機能
logger.warning("設定ファイルが見つかりません。デフォルト値を使用")
logger.warning(f"API rate limit: {remaining}/1000")
logger.warning("この関数は非推奨です。new_function()を使用してください")

# ERROR: 例外発生、処理失敗
logger.error("データベース接続に失敗", exc_info=True)
logger.error(f"ファイル {filename} の読み込みに失敗")

# CRITICAL: システム停止レベルの重大エラー
logger.critical("データベース接続が完全に失敗しました")
logger.critical("必須の設定ファイルが見つかりません")
```

---

## 🎯 実践的デバッグ戦略

### ステップ1: 問題の再現

```python
# ✅ 良い例：再現手順を記録
"""
バグ再現手順:
1. ユーザーID=100でログイン
2. 商品ID=500を3個カートに追加
3. チェックアウトボタンを押す
→ ValueError: 在庫数が不正です

期待する動作: 在庫チェック後にエラーメッセージを表示
実際の動作: 例外が発生してアプリケーションが停止
"""

def reproduce_bug():
    """バグの再現用関数"""
    user_id = 100
    product_id = 500
    quantity = 3
    # ... バグを再現するコード
```

### ステップ2: 仮説を立てる

```python
# print デバッグで情報収集
def checkout(user_id, items):
    print(f"[DEBUG] checkout called: user_id={user_id}")
    print(f"[DEBUG] items: {items}")
    
    for item in items:
        stock = get_stock(item['product_id'])
        print(f"[DEBUG] product_id={item['product_id']}, stock={stock}, requested={item['quantity']}")
        
        # 仮説: stockがNoneの場合に比較エラー？
        if stock < item['quantity']:  # ← ここでエラー？
            raise ValueError("在庫数が不正です")
```

### ステップ3: 仮説を検証

```python
def checkout(user_id, items):
    logger.info(f"チェックアウト開始: user_id={user_id}, items={len(items)}")
    
    for item in items:
        stock = get_stock(item['product_id'])
        
        # 仮説検証: stockがNoneの場合をチェック
        if stock is None:
            logger.error(f"在庫情報取得失敗: product_id={item['product_id']}")
            raise ValueError(f"商品ID {item['product_id']} の在庫情報が取得できません")
        
        logger.debug(f"在庫確認: product_id={item['product_id']}, stock={stock}, requested={item['quantity']}")
        
        if stock < item['quantity']:
            logger.warning(f"在庫不足: product_id={item['product_id']}, stock={stock}, requested={item['quantity']}")
            raise ValueError(f"在庫が不足しています（在庫: {stock}個）")
```

### ステップ4: 修正と防止

```python
def checkout(user_id, items):
    """
    チェックアウト処理
    
    修正内容:
    - 在庫情報がNoneの場合のハンドリング追加
    - エラーメッセージを具体的に改善
    - ログレベルを適切に設定
    """
    logger.info(f"チェックアウト開始: user_id={user_id}, items_count={len(items)}")
    
    try:
        for item in items:
            # 在庫情報の取得と検証
            stock = get_stock(item['product_id'])
            
            if stock is None:
                logger.error(f"在庫情報取得失敗: product_id={item['product_id']}")
                raise ValueError(
                    f"商品ID {item['product_id']} の在庫情報が取得できません。"
                    "管理者に連絡してください。"
                )
            
            if stock < item['quantity']:
                logger.warning(
                    f"在庫不足: product_id={item['product_id']}, "
                    f"stock={stock}, requested={item['quantity']}"
                )
                raise ValueError(
                    f"商品ID {item['product_id']} の在庫が不足しています。"
                    f"（在庫: {stock}個、注文: {item['quantity']}個）"
                )
            
            logger.debug(f"在庫確認OK: product_id={item['product_id']}")
        
        # チェックアウト処理本体
        # ...
        
        logger.info(f"チェックアウト完了: user_id={user_id}")
        
    except ValueError as e:
        logger.error(f"チェックアウトエラー: {e}", exc_info=True)
        raise
    except Exception as e:
        logger.critical(f"予期しないエラー: {e}", exc_info=True)
        raise


# ユニットテストで防止
def test_checkout_with_none_stock():
    """在庫情報がNoneの場合のテスト"""
    # モックで在庫情報をNoneに設定
    with patch('get_stock', return_value=None):
        with pytest.raises(ValueError, match="在庫情報が取得できません"):
            checkout(100, [{'product_id': 500, 'quantity': 1}])
```

---

## 🔍 よくあるバグのデバッグ方法

### 1. None参照エラー

```python
# ❌ エラーが発生するコード
result = data['user']['name']  # KeyError or TypeError

# ✅ デバッグ方法
print(f"data type: {type(data)}")
print(f"data: {data}")
print(f"'user' in data: {'user' in data}")

if data and 'user' in data:
    print(f"user: {data['user']}")
    if data['user'] and 'name' in data['user']:
        result = data['user']['name']
```

### 2. ループ内のバグ

```python
# デバッグ前
for item in items:
    process(item)  # 特定のitemでエラー

# デバッグ中
for index, item in enumerate(items):
    print(f"[{index}/{len(items)}] Processing: {item}")
    try:
        process(item)
    except Exception as e:
        print(f"Error at index {index}: {e}")
        print(f"Item data: {item}")
        raise

# breakpoint を使う場合
for index, item in enumerate(items):
    if index == 5:  # 5番目でエラーが出る
        breakpoint()  # ここで停止して調査
    process(item)
```

### 3. 型エラー

```python
# デバッグヘルパー関数
def debug_type(var_name, var_value):
    print(f"{var_name}:")
    print(f"  value: {var_value}")
    print(f"  type: {type(var_value)}")
    print(f"  dir: {dir(var_value)[:5]}...")  # メソッド一覧（最初の5個）
    if hasattr(var_value, '__len__'):
        print(f"  len: {len(var_value)}")

# 使用例
debug_type("user_input", user_input)
debug_type("result", result)
```

### 4. 文字エンコーディングエラー

```python
# デバッグ情報の表示
import sys

print(f"システムエンコーディング: {sys.getdefaultencoding()}")
print(f"ファイルシステムエンコーディング: {sys.getfilesystemencoding()}")

# ファイル読み込み時
try:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeDecodeError as e:
    print(f"エンコーディングエラー: {e}")
    print(f"ファイル: {filename}")
    
    # 別のエンコーディングを試す
    for enc in ['shift_jis', 'cp932', 'latin-1']:
        try:
            with open(filename, 'r', encoding=enc) as f:
                content = f.read()
            print(f"成功: {enc}")
            break
        except:
            continue
```

---

## 📊 パフォーマンスデバッグ

### 実行時間の計測

```python
import time
from functools import wraps

# デコレータで関数の実行時間を計測
def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        print(f"{func.__name__} took {end - start:.4f} seconds")
        return result
    return wrapper

@measure_time
def slow_function():
    time.sleep(1)
    return "done"

# コンテキストマネージャーで計測
from contextlib import contextmanager

@contextmanager
def timer(name):
    start = time.time()
    yield
    end = time.time()
    print(f"{name}: {end - start:.4f} seconds")

# 使用例
with timer("データベースクエリ"):
    # ... 処理
    pass
```

### プロファイリング

```python
import cProfile
import pstats

# プロファイリング実行
cProfile.run('my_function()', 'profile_stats')

# 結果の表示
stats = pstats.Stats('profile_stats')
stats.sort_stats('cumulative')
stats.print_stats(10)  # 上位10件を表示
```

---

## 🛡️ 本番環境でのデバッグ

### 絶対にやってはいけないこと

```python
# ❌ NG: 本番環境で breakpoint()
def production_function():
    breakpoint()  # システムが停止する！

# ❌ NG: 本番環境で DEBUG レベル
logging.basicConfig(level=logging.DEBUG)  # ログが膨大になる

# ❌ NG: 機密情報のログ出力
logger.info(f"パスワード: {password}")  # セキュリティリスク！
logger.debug(f"クレジットカード: {card_number}")  # 絶対NG！
```

### 本番環境で安全にデバッグ

```python
# ✅ OK: 環境変数で制御
import os

DEBUG_MODE = os.environ.get('DEBUG_MODE', 'False') == 'True'

if DEBUG_MODE:
    logger.debug("デバッグ情報（開発環境のみ）")

# ✅ OK: 機密情報をマスク
def mask_sensitive_data(data):
    """機密情報をマスク"""
    if isinstance(data, str) and len(data) > 4:
        return data[:2] + '*' * (len(data) - 4) + data[-2:]
    return '****'

logger.info(f"カード番号: {mask_sensitive_data(card_number)}")

# ✅ OK: エラー時のみ詳細ログ
try:
    risky_operation()
except Exception as e:
    logger.error(f"エラー発生: {type(e).__name__}", exc_info=True)
    # 必要な情報のみをログに記録
    logger.error(f"user_id: {user_id}, operation: {operation_name}")
```

---

## 💡 デバッグTips集

### 1. 二分探索デバッグ

```python
# コードの真ん中にbreakpointを置く
def long_function():
    # 処理1-10
    # ...
    
    breakpoint()  # ← ここまで正常に動作するか確認
    
    # 処理11-20
    # ...
```

### 2. ラバーダックデバッグ

```python
# コメントで処理を説明する（バグに気づくことが多い）
def calculate_discount(price, customer_type):
    # 1. 顧客タイプを確認
    # 2. 基本割引率を取得
    # 3. 価格に応じた追加割引を計算
    # 4. 最終価格を計算
    # ↑ ここで「あれ、追加割引の計算が間違ってる？」と気づく
    pass
```

### 3. アサーションでバグを早期発見

```python
def divide(a, b):
    assert b != 0, "除数は0にできません"
    assert isinstance(a, (int, float)), "被除数は数値である必要があります"
    assert isinstance(b, (int, float)), "除数は数値である必要があります"
    return a / b
```

---

## 📚 参考リソース

### 公式ドキュメント
- [Python logging](https://docs.python.org/ja/3/library/logging.html)
- [Python pdb](https://docs.python.org/ja/3/library/pdb.html)
- [VSCode Python Debugging](https://code.visualstudio.com/docs/python/debugging)

### 推奨ツール
- **ipdb**: pdbの拡張版（タブ補完、シンタックスハイライト）
- **pudb**: フルスクリーンのビジュアルデバッガー
- **icecream**: print()の強化版
- **loguru**: loggingの簡単版

### インストール

```bash
# 拡張デバッガー
pip install ipdb pudb

# ログ・デバッグユーティリティ
pip install icecream loguru

# パフォーマンス解析
pip install line_profiler memory_profiler
```

---

## ✅ デバッグチェックリスト

```markdown
□ エラーメッセージを正確に読んだ
□ スタックトレースで発生箇所を特定した
□ 問題を再現できる最小限のコードを作成した
□ 変数の型と値を確認した
□ 境界値（空リスト、None、0など）でテストした
□ ログに十分な情報を出力した
□ デバッガーで1行ずつ実行した
□ 修正後にテストを追加した
□ コードレビューを依頼した
□ ドキュメント・コメントを更新した
```