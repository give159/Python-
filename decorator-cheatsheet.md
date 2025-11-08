# 🎯 Pythonロギングデコレーター 完全チートシート

## 📦 インストール不要！コピペで使える

`logging_decorators.py` をプロジェクトに配置するだけ！

---

## 🚀 クイックスタート

### 基本的な使い方

```python
# 1. モジュールをインポート
from logging_decorators import log_call, log_time, log_errors

# 2. 関数にデコレーターを付ける
@log_call
def my_function(x, y):
    return x + y

# 3. 普通に関数を呼ぶだけ！
result = my_function(3, 5)  # ログが自動で出力される
```

---

## 📋 デコレーター一覧

| デコレーター | 用途 | パラメータ | 使用頻度 |
|-------------|------|-----------|---------|
| `@log_call` | 関数呼び出しをログ | なし | ⭐⭐⭐⭐⭐ |
| `@log_time` | 実行時間を計測 | なし | ⭐⭐⭐⭐⭐ |
| `@log_errors` | エラーをキャッチ | なし | ⭐⭐⭐⭐⭐ |
| `@count_calls` | 呼び出し回数カウント | なし | ⭐⭐⭐ |
| `@log_detailed` | 詳細な情報を出力 | なし | ⭐⭐⭐⭐ |
| `@retry()` | 失敗時に再試行 | あり | ⭐⭐⭐⭐ |
| `@cache_result` | 結果をキャッシュ | なし | ⭐⭐⭐⭐ |
| `@validate_args()` | 引数を検証 | あり | ⭐⭐⭐ |
| `@debug` | デバッグ情報出力 | なし | ⭐⭐⭐ |
| `@log_all` | 全部盛り | なし | ⭐⭐⭐⭐ |

---

## 📖 各デコレーターの詳細

### 1️⃣ @log_call - 関数呼び出しをログ出力

**いつ使う**: どの関数がいつ呼ばれたか確認したい時

```python
@log_call
def calculate_tax(price, rate):
    return price * rate

calculate_tax(1000, 0.1)
```

**出力例**:
```
[2025-01-10 10:30:15] INFO  → 呼び出し: calculate_tax(1000, 0.1)
[2025-01-10 10:30:15] INFO  ← 完了: calculate_tax() → 100.0
```

**ポイント**:
- ✅ 引数の値が自動で記録される
- ✅ 戻り値も記録される
- ✅ 関数の実行フローが可視化される

---

### 2️⃣ @log_time - 実行時間を計測

**いつ使う**: パフォーマンスのボトルネックを見つけたい時

```python
@log_time
def process_data(data):
    # 重い処理
    result = []
    for item in data:
        result.append(item * 2)
    return result

process_data(range(100000))
```

**出力例**:
```
[2025-01-10 10:30:15] INFO  ⏱ process_data() の実行時間: 125.43ms
```

**ポイント**:
- ✅ ミリ秒単位で計測
- ✅ どの関数が遅いか一目瞭然
- ✅ 最適化の優先順位が決められる

---

### 3️⃣ @log_errors - エラーをキャッチしてログ出力

**いつ使う**: エラーが発生した場所と原因を記録したい時

```python
@log_errors
def divide(a, b):
    return a / b

try:
    divide(10, 0)
except ZeroDivisionError:
    print("エラーを処理しました")
```

**出力例**:
```
[2025-01-10 10:30:15] ERROR ❌ divide() でエラー発生: ZeroDivisionError: division by zero
[2025-01-10 10:30:15] ERROR スタックトレース:
Traceback (most recent call last):
  File "...", line X, in wrapper
    return func(*args, **kwargs)
  ...
```

**ポイント**:
- ✅ エラー情報が詳細に記録される
- ✅ スタックトレースも自動で出力
- ✅ 例外は再送出されるので上位で処理可能

---

### 4️⃣ @count_calls - 呼び出し回数をカウント

**いつ使う**: 関数が何回呼ばれているか監視したい時

```python
@count_calls
def api_call():
    # API呼び出し
    pass

api_call()
api_call()
api_call()

print(f"API呼び出し回数: {api_call.call_count}")
# 出力: API呼び出し回数: 3
```

**ポイント**:
- ✅ `.call_count` 属性で回数を取得可能
- ✅ API制限の監視に便利
- ✅ 不要な呼び出しの発見に役立つ

---

### 5️⃣ @log_detailed - 詳細な情報を出力

**いつ使う**: デバッグ時に引数と戻り値の型も確認したい時

```python
@log_detailed
def process_user(user_id, name, age=None):
    return {"id": user_id, "name": name, "age": age}

process_user(123, "田中太郎", age=30)
```

**出力例**:
```
============================================================
関数: process_user()
============================================================
位置引数:
  [0] int: 123
  [1] str: '田中太郎'
キーワード引数:
  age: int = 30
戻り値: dict = {'id': 123, 'name': '田中太郎', 'age': 30}
============================================================
```

**ポイント**:
- ✅ 引数の型と値が明確
- ✅ デバッグ時に超便利
- ✅ 型の不一致を発見しやすい

---

### 6️⃣ @retry() - 失敗時に自動リトライ（パラメータ付き）

**いつ使う**: 不安定なAPI呼び出しやネットワーク処理

```python
@retry(max_attempts=3, delay=1.0)
def fetch_data_from_api(url):
    # 不安定なAPI呼び出し
    response = requests.get(url)
    return response.json()

data = fetch_data_from_api("https://api.example.com/data")
```

**パラメータ**:
- `max_attempts`: 最大試行回数（デフォルト: 3）
- `delay`: 試行間の待機時間・秒（デフォルト: 1.0）

**出力例**:
```
[2025-01-10 10:30:15] INFO  🔄 fetch_data_from_api() 試行 1/3
[2025-01-10 10:30:16] WARNING ⚠️ fetch_data_from_api() 失敗（1/3）: ConnectionError
[2025-01-10 10:30:16] INFO  ⏳ 1.0秒待機後に再試行...
[2025-01-10 10:30:17] INFO  🔄 fetch_data_from_api() 試行 2/3
[2025-01-10 10:30:17] INFO  ✅ fetch_data_from_api() 成功（2回目で成功）
```

**ポイント**:
- ✅ 一時的なエラーを自動で回避
- ✅ リトライ回数と間隔を調整可能
- ✅ 本番環境で超重要

---

### 7️⃣ @cache_result - 結果をキャッシュ（メモ化）

**いつ使う**: 同じ計算を繰り返したくない時

```python
@cache_result
def fibonacci(n):
    if n <= 1:
        return n
    return fibonacci(n-1) + fibonacci(n-2)

# 1回目: 計算される（遅い）
result1 = fibonacci(35)

# 2回目: キャッシュから取得（超速い）
result2 = fibonacci(35)

# キャッシュをクリア
fibonacci.clear_cache()
```

**出力例**:
```
[2025-01-10 10:30:15] DEBUG 🔍 fibonacci() キャッシュミス（新規計算）
[2025-01-10 10:30:15] DEBUG 💾 fibonacci() キャッシュヒット（ヒット率: 1/2）
```

**ポイント**:
- ✅ 計算時間が劇的に短縮
- ✅ `.clear_cache()` でキャッシュクリア
- ⚠️ 副作用のある関数には使えない

---

### 8️⃣ @validate_args() - 引数を検証（パラメータ付き）

**いつ使う**: 関数に不正な引数が渡されるのを防ぎたい時

```python
@validate_args(
    age=lambda x: isinstance(x, int) and 0 <= x <= 150,
    name=lambda x: isinstance(x, str) and len(x) > 0,
    email=lambda x: isinstance(x, str) and '@' in x
)
def register_user(name, age, email):
    return f"登録完了: {name}"

# OK
register_user("田中", 25, "tanaka@example.com")

# NG: ValueError が発生
register_user("", 25, "tanaka@example.com")  # 名前が空
register_user("田中", -5, "tanaka@example.com")  # 年齢が負
```

**パラメータ**:
- 引数名をキーに、検証関数（lambda）を値にした辞書

**ポイント**:
- ✅ 引数の型と値を事前チェック
- ✅ バグを早期に発見
- ✅ 関数のドキュメント代わりにもなる

---

### 9️⃣ @debug - デバッグ情報を詳細出力

**いつ使う**: 開発中に関数の詳細情報が欲しい時

```python
@debug
def complex_calculation(x, y):
    return x ** y

complex_calculation(2, 10)
```

**出力例**:
```
======= 🐛 DEBUG INFO ====================================
関数名: complex_calculation
モジュール: __main__
定義場所: /path/to/file.py:123
引数: args=(2, 10), kwargs={}
実行開始...
実行完了: 戻り値=1024
============================================================
```

**ポイント**:
- ✅ 関数の全情報が一覧できる
- ✅ どこで定義されているかわかる
- ✅ 開発時のみ使用推奨

---

### 🔟 @log_all - 全部盛り（便利）

**いつ使う**: とりあえず全部のログが欲しい時

```python
@log_all
def important_function(x, y):
    return x * y

important_function(7, 8)
```

**機能**:
- ✅ エラーハンドリング（@log_errors）
- ✅ 実行時間計測（@log_time）
- ✅ 関数呼び出しログ（@log_call）

**出力例**:
```
[2025-01-10 10:30:15] INFO  → 呼び出し: important_function(7, 8)
[2025-01-10 10:30:15] INFO  ⏱ important_function() の実行時間: 0.05ms
[2025-01-10 10:30:15] INFO  ← 完了: important_function() → 56
```

---

## 🔗 デコレーターの組み合わせ

### 複数のデコレーターを重ねる

```python
@log_errors        # 3番目に実行（外側）
@log_time          # 2番目に実行
@log_call          # 1番目に実行（内側）
def complex_task():
    time.sleep(0.1)
    return "完了"

complex_task()
```

**ポイント**:
- ✅ 下から上に適用される
- ✅ 順序が重要！
- ✅ よく使う組み合わせ: `@log_errors` → `@log_time` → `@log_call`

---

## 📊 実務での使い分け

### 開発時（ローカル環境）

```python
@log_detailed  # 詳細な情報
@debug         # デバッグ情報
def development_function():
    pass
```

### テスト時

```python
@log_call      # 呼び出しログ
@count_calls   # 回数カウント
def test_function():
    pass
```

### 本番環境

```python
@log_errors    # エラーログ（必須）
@log_time      # パフォーマンス監視
@retry(max_attempts=3, delay=2.0)  # リトライ
def production_function():
    pass
```

---

## ⚙️ ロガーのカスタマイズ

### ログレベルを変更

```python
import logging
from logging_decorators import logger

# DEBUGレベルに変更（開発時）
logger.setLevel(logging.DEBUG)

# INFOレベルに変更（本番環境）
logger.setLevel(logging.INFO)

# WARNINGレベルに変更（本番環境・静か）
logger.setLevel(logging.WARNING)
```

### ファイルにもログ出力

```python
import logging
from logging_decorators import logger

# ファイルハンドラーを追加
file_handler = logging.FileHandler('app.log')
file_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)s - %(message)s'
)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
```

---

## 🎨 実践例

### 例1: Webアプリケーションのエンドポイント

```python
from flask import Flask
from logging_decorators import log_all, retry

app = Flask(__name__)

@app.route('/api/users/<int:user_id>')
@log_all
@retry(max_attempts=2, delay=0.5)
def get_user(user_id):
    """ユーザー情報を取得"""
    # データベースから取得
    user = db.get_user(user_id)
    return jsonify(user)
```

### 例2: データ処理パイプライン

```python
from logging_decorators import log_time, log_errors, cache_result

@log_errors
@log_time
def load_data(file_path):
    """データを読み込む"""
    with open(file_path) as f:
        return json.load(f)

@log_errors
@log_time
@cache_result
def transform_data(data):
    """データを変換（キャッシュ有効）"""
    return [item['value'] * 2 for item in data]

@log_errors
@log_time
def save_data(data, output_path):
    """データを保存"""
    with open(output_path, 'w') as f:
        json.dump(data, f)

# パイプライン実行
data = load_data('input.json')
transformed = transform_data(data)
save_data(transformed, 'output.json')
```

### 例3: API クライアント

```python
from logging_decorators import retry, log_call, log_errors
import requests

class APIClient:
    @log_call
    @log_errors
    @retry(max_attempts=3, delay=2.0)
    def fetch_data(self, endpoint):
        """APIからデータを取得（リトライ付き）"""
        response = requests.get(f"{self.base_url}/{endpoint}")
        response.raise_for_status()
        return response.json()
    
    @log_call
    @validate_args(
        data=lambda x: isinstance(x, dict)
    )
    def post_data(self, endpoint, data):
        """APIにデータを送信（検証付き）"""
        response = requests.post(
            f"{self.base_url}/{endpoint}",
            json=data
        )
        return response.json()
```

---

## 🐛 トラブルシューティング

### Q1: ログが2回表示される

**原因**: ハンドラーが重複している

**解決策**:
```python
# ハンドラーをクリアしてから追加
logger.handlers.clear()
logger.addHandler(console_handler)
```

### Q2: デコレーターの順序がわからない

**ルール**: 下から上に適用される

```python
@outer  # 3番目
@middle # 2番目
@inner  # 1番目（最初に実行）
def func():
    pass
```

### Q3: キャッシュが効かない

**原因**: 引数がハッシュ不可能（リストや辞書）

**解決策**:
```python
# NG: リストはハッシュ不可能
@cache_result
def func(items: list):
    pass

# OK: タプルを使う
@cache_result
def func(items: tuple):
    pass
```

---

## 📝 チェックリスト

開発時:
- [ ] `@log_call` で関数の流れを確認
- [ ] `@log_detailed` で引数の型を確認
- [ ] `@debug` でデバッグ情報を確認

本番環境デプロイ前:
- [ ] `@log_errors` でエラーハンドリング
- [ ] `@log_time` でパフォーマンス確認
- [ ] `@retry` で一時的なエラーに対応
- [ ] ログレベルを INFO 以上に設定
- [ ] DEBUG レベルのログを削除

---

## 🔗 参考資料

- [Python logging 公式ドキュメント](https://docs.python.org/ja/3/library/logging.html)
- [Python functools 公式ドキュメント](https://docs.python.org/ja/3/library/functools.html)
- [PEP 318 - Decorators](https://www.python.org/dev/peps/pep-0318/)

---

## 💡 Tips

1. **開発時は詳細に、本番は簡潔に**
   - 開発: `@log_detailed`, `@debug`
   - 本番: `@log_errors`, `@log_time`

2. **パフォーマンスが気になる関数には `@log_time`**
   - ボトルネックが一目瞭然

3. **不安定な処理には `@retry`**
   - API呼び出し、ネットワーク処理、DB接続

4. **重い計算には `@cache_result`**
   - フィボナッチ、素数判定、データ集計

5. **本番環境では必ず `@log_errors`**
   - エラーを見逃さない

---

## 🎓 まとめ

| 状況 | おすすめデコレーター |
|-----|-------------------|
| 開発中 | `@log_detailed`, `@debug` |
| デバッグ中 | `@log_call`, `@count_calls` |
| パフォーマンス改善 | `@log_time`, `@cache_result` |
| 本番環境 | `@log_errors`, `@retry` |
| とりあえず全部 | `@log_all` |

**デコレーターを使いこなせば、コードの品質が劇的に向上します！** 🚀