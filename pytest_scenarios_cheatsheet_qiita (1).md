# 【Python/pytest】実務で使える！シーン別テストパターン完全チートシート

## はじめに

実務でpytestを使うとき、「このケースってどうテストするんだっけ？」と迷ったことはありませんか？

この記事では、**実際の開発でよく遭遇する15のシーン**について、コピペで使えるテストパターンを紹介します。

### 対象読者
- Pythonの基本構文は理解している
- pytestを使い始めた、または使いたい
- 実務で使えるテストパターンを知りたい

### この記事で学べること
✅ 基本的なテストの書き方
✅ クラス変数・インスタンス変数のテスト
✅ プロパティ（getter/setter）のテスト
✅ 継承のテスト
✅ 標準出力のキャプチャ
✅ エッジケースのテスト
✅ フィクスチャの活用
✅ パラメータ化テスト

---

## 環境構築

```bash
# pytestのインストール
pip install pytest

# カバレッジ測定用（オプション）
pip install pytest-cov

# バージョン確認
pytest --version
```

---

## 📋 目次

1. [基本的なアサーション](#1-基本的なアサーション)
2. [列挙型（Enum）のテスト](#2-列挙型enumのテスト)
3. [クラスの初期化テスト](#3-クラスの初期化テスト)
4. [プロパティ（読み取り専用）のテスト](#4-プロパティ読み取り専用のテスト)
5. [クラス変数 vs インスタンス変数](#5-クラス変数-vs-インスタンス変数)
6. [継承のテスト](#6-継承のテスト)
7. [標準出力のキャプチャ](#7-標準出力のキャプチャ)
8. [メソッドの副作用をテスト](#8-メソッドの副作用をテスト)
9. [エッジケースのテスト](#9-エッジケースのテスト)
10. [リストや辞書のテスト](#10-リストや辞書のテスト)
11. [フィクスチャの活用](#11-フィクスチャの活用)
12. [パラメータ化テスト](#12-パラメータ化テスト)
13. [例外のテスト](#13-例外のテスト)
14. [プロパティ（setter付き）のテスト](#14-プロパティsetter付きのテスト)
15. [統合テスト](#15-統合テスト)

---

## 1. 基本的なアサーション

### シーン
「値が期待通りか確認したい」

### テストコード

```python
def test_basic_assertions():
    """基本的なアサーションの例"""
    # 等価
    assert 1 + 1 == 2
    
    # 不等価
    assert 1 + 1 != 3
    
    # 大小比較
    assert 10 > 5
    assert 3 < 5
    
    # 真偽値
    assert True
    assert not False
    
    # コレクションの要素
    assert "a" in ["a", "b", "c"]
    assert "d" not in ["a", "b", "c"]
    
    # 型チェック
    assert isinstance(123, int)
    assert isinstance("hello", str)
```

### ポイント
- `assert`の後に条件式を書く
- 条件がFalseだとテスト失敗
- エラーメッセージは自動生成される

---

## 2. 列挙型（Enum）のテスト

### シーン
「列挙型の値が正しいか確認したい」

### 実装コード

```python
from enum import Enum

class Gender(Enum):
    """性別を表す列挙型"""
    MAN = "男性"
    WOMAN = "女性"
    OTHER = "その他"
```

### テストコード

```python
def test_enum_values():
    """列挙型の値をテスト"""
    # 値が正しいか
    assert Gender.MAN.value == "男性"
    assert Gender.WOMAN.value == "女性"
    assert Gender.OTHER.value == "その他"

def test_enum_members():
    """すべてのメンバーが存在するか"""
    members = list(Gender)
    
    assert len(members) == 3
    assert Gender.MAN in members
    assert Gender.WOMAN in members
    assert Gender.OTHER in members
```

### ポイント
- `.value`で列挙型の値を取得
- `list(EnumClass)`ですべてのメンバーを取得

---

## 3. クラスの初期化テスト

### シーン
「クラスのインスタンスが正しく作られるか確認したい」

### 実装コード

```python
class User:
    """ユーザークラス"""
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age
```

### テストコード

```python
def test_user_initialization():
    """ユーザーが正しく初期化される"""
    # インスタンス作成
    user = User("太郎", 25)
    
    # 属性が正しく設定されているか
    assert user.name == "太郎"
    assert user.age == 25
    
    # 型が正しいか
    assert isinstance(user.name, str)
    assert isinstance(user.age, int)
```

### ポイント
- インスタンス作成後、すぐに属性を確認
- 型チェックも忘れずに

---

## 4. プロパティ（読み取り専用）のテスト

### シーン
「プロパティが読み取り専用か確認したい」

### 実装コード

```python
class User:
    """ユーザークラス"""
    def __init__(self, name: str):
        self._name = name
    
    @property
    def name(self) -> str:
        """名前を取得（読み取り専用）"""
        return self._name
```

### テストコード

```python
import pytest

def test_readonly_property():
    """プロパティが読み取り専用であることを確認"""
    user = User("太郎")
    
    # 読み取りはOK
    assert user.name == "太郎"
    
    # 書き込みはNG
    with pytest.raises(AttributeError):
        user.name = "花子"
```

### ポイント
- `pytest.raises()`で例外をキャッチ
- `AttributeError`が発生すればテスト成功

---

## 5. クラス変数 vs インスタンス変数

### シーン
「クラス変数とインスタンス変数の違いを確認したい」

### 実装コード

```python
class Employee:
    """社員クラス"""
    # クラス変数（全員で共有）
    company_name = "ABC株式会社"
    
    def __init__(self, name: str):
        # インスタンス変数（個人専用）
        self.name = name
```

### テストコード

```python
def test_class_variable_shared():
    """クラス変数が全インスタンスで共有される"""
    emp1 = Employee("太郎")
    emp2 = Employee("花子")
    
    # クラス変数は共有される
    assert emp1.company_name == "ABC株式会社"
    assert emp2.company_name == "ABC株式会社"
    assert emp1.company_name == emp2.company_name

def test_instance_variable_independent():
    """インスタンス変数は独立している"""
    emp1 = Employee("太郎")
    emp2 = Employee("花子")
    
    # インスタンス変数は独立
    assert emp1.name == "太郎"
    assert emp2.name == "花子"
    assert emp1.name != emp2.name
```

### ポイント
- クラス変数：すべてのインスタンスで共有
- インスタンス変数：各インスタンスで独立

---

## 6. 継承のテスト

### シーン
「クラスが正しく継承されているか確認したい」

### 実装コード

```python
class Animal:
    """動物クラス（親）"""
    def __init__(self, name: str):
        self.name = name
    
    def speak(self):
        return "何か鳴く"

class Dog(Animal):
    """犬クラス（子）"""
    def speak(self):
        return "ワン"
```

### テストコード

```python
def test_inheritance():
    """継承関係を確認"""
    dog = Dog("ポチ")
    
    # 親クラスのインスタンスでもある
    assert isinstance(dog, Dog)
    assert isinstance(dog, Animal)
    
    # 親クラスの属性を継承
    assert dog.name == "ポチ"
    
    # メソッドのオーバーライド
    assert dog.speak() == "ワン"

def test_has_parent_methods():
    """親クラスのメソッドを持っているか"""
    dog = Dog("ポチ")
    
    # メソッドの存在確認
    assert hasattr(dog, 'speak')
    assert callable(dog.speak)
```

### ポイント
- `isinstance()`で継承関係を確認
- `hasattr()`でメソッドの存在を確認

---

## 7. 標準出力のキャプチャ

### シーン
「print文の出力内容を確認したい」

### 実装コード

```python
class User:
    """ユーザークラス"""
    def __init__(self, name: str):
        self.name = name
    
    def greet(self):
        """挨拶を表示"""
        print(f"こんにちは、{self.name}さん")
```

### テストコード

```python
def test_print_output(capsys):
    """標準出力をキャプチャしてテスト
    
    Args:
        capsys: pytestの標準出力キャプチャフィクスチャ
    """
    user = User("太郎")
    
    # メソッドを実行
    user.greet()
    
    # 出力をキャプチャ
    captured = capsys.readouterr()
    
    # 出力内容を確認
    assert "こんにちは" in captured.out
    assert "太郎さん" in captured.out
    assert captured.out == "こんにちは、太郎さん\n"
```

### ポイント
- テスト関数の引数に`capsys`を追加
- `capsys.readouterr()`で出力を取得
- `captured.out`に標準出力の内容が入る

---

## 8. メソッドの副作用をテスト

### シーン
「メソッド実行後、状態が変わることを確認したい」

### 実装コード

```python
class Counter:
    """カウンタークラス"""
    def __init__(self):
        self.count = 0
    
    def increment(self):
        """カウントを1増やす"""
        self.count += 1
    
    def reset(self):
        """カウントを0に戻す"""
        self.count = 0
```

### テストコード

```python
def test_counter_increment():
    """incrementで値が増えることを確認"""
    counter = Counter()
    
    # 初期状態
    assert counter.count == 0
    
    # 1回実行
    counter.increment()
    assert counter.count == 1
    
    # もう1回実行
    counter.increment()
    assert counter.count == 2

def test_counter_reset():
    """resetで0に戻ることを確認"""
    counter = Counter()
    
    # カウントを増やす
    counter.increment()
    counter.increment()
    assert counter.count == 2
    
    # リセット
    counter.reset()
    assert counter.count == 0
```

### ポイント
- メソッド実行前後で状態を確認
- 複数回実行してテスト

---

## 9. エッジケースのテスト

### シーン
「境界値や異常なケースをテストしたい」

### 実装コード

```python
class BankAccount:
    """銀行口座クラス"""
    def __init__(self, balance: float):
        self.balance = balance
    
    def withdraw(self, amount: float) -> bool:
        """出金"""
        if amount <= 0:
            return False
        if self.balance < amount:
            return False
        self.balance -= amount
        return True
```

### テストコード

```python
def test_withdraw_zero():
    """0円の出金（エッジケース）"""
    account = BankAccount(1000)
    
    result = account.withdraw(0)
    
    assert result is False
    assert account.balance == 1000  # 変わらない

def test_withdraw_negative():
    """マイナス金額の出金（異常系）"""
    account = BankAccount(1000)
    
    result = account.withdraw(-100)
    
    assert result is False
    assert account.balance == 1000

def test_withdraw_exactly_balance():
    """残高ちょうどの出金（境界値）"""
    account = BankAccount(1000)
    
    result = account.withdraw(1000)
    
    assert result is True
    assert account.balance == 0

def test_withdraw_more_than_balance():
    """残高以上の出金（エッジケース）"""
    account = BankAccount(1000)
    
    result = account.withdraw(1001)
    
    assert result is False
    assert account.balance == 1000
```

### ポイント
- 正常系だけでなく異常系もテスト
- 境界値（0、最大値、最小値）を必ずテスト

---

## 10. リストや辞書のテスト

### シーン
「リストや辞書の操作をテストしたい」

### 実装コード

```python
class Team:
    """チームクラス"""
    def __init__(self):
        self.members = []
    
    def add_member(self, name: str):
        """メンバーを追加"""
        self.members.append(name)
    
    def remove_member(self, name: str):
        """メンバーを削除"""
        if name in self.members:
            self.members.remove(name)
    
    def get_member_count(self) -> int:
        """メンバー数を取得"""
        return len(self.members)
```

### テストコード

```python
def test_team_add_member():
    """メンバー追加のテスト"""
    team = Team()
    
    # 初期状態
    assert len(team.members) == 0
    assert team.get_member_count() == 0
    
    # メンバー追加
    team.add_member("太郎")
    assert "太郎" in team.members
    assert team.get_member_count() == 1
    
    # さらに追加
    team.add_member("花子")
    assert team.members == ["太郎", "花子"]
    assert team.get_member_count() == 2

def test_team_remove_member():
    """メンバー削除のテスト"""
    team = Team()
    team.add_member("太郎")
    team.add_member("花子")
    
    # 削除
    team.remove_member("太郎")
    assert "太郎" not in team.members
    assert "花子" in team.members
    assert team.get_member_count() == 1

def test_team_remove_nonexistent_member():
    """存在しないメンバーの削除"""
    team = Team()
    team.add_member("太郎")
    
    # 存在しないメンバーを削除（エラーにならない）
    team.remove_member("花子")
    assert team.get_member_count() == 1
```

### ポイント
- リストの要素確認は`in`演算子
- リスト全体の比較は`==`
- `len()`で要素数を確認

---

## 11. フィクスチャの活用

### シーン
「複数のテストで同じ準備処理を使いたい」

### テストコード

```python
import pytest

@pytest.fixture
def sample_user():
    """テスト用のユーザーを作成するフィクスチャ"""
    user = User("太郎", 25)
    return user

@pytest.fixture
def sample_team():
    """テスト用のチームを作成するフィクスチャ"""
    team = Team()
    team.add_member("太郎")
    team.add_member("花子")
    team.add_member("次郎")
    return team

def test_with_fixture(sample_user):
    """フィクスチャを使ったテスト
    
    Args:
        sample_user: pytest.fixtureで作成されたユーザー
    """
    # 準備不要！すぐに使える
    assert sample_user.name == "太郎"
    assert sample_user.age == 25

def test_team_with_fixture(sample_team):
    """チームフィクスチャを使ったテスト"""
    assert sample_team.get_member_count() == 3
    assert "太郎" in sample_team.members
```

### ポイント
- `@pytest.fixture`デコレーターで定義
- テスト関数の引数に指定すると自動で実行
- 共通の準備処理を再利用できる

---

## 12. パラメータ化テスト

### シーン
「同じテストを複数のデータで実行したい」

### 実装コード

```python
def calculate_tax(price: int, tax_rate: float) -> int:
    """税込価格を計算"""
    return int(price * (1 + tax_rate))
```

### テストコード

```python
@pytest.mark.parametrize("price, tax_rate, expected", [
    (100, 0.1, 110),   # ケース1
    (200, 0.1, 220),   # ケース2
    (1000, 0.08, 1080), # ケース3
    (500, 0.0, 500),   # ケース4（税率0）
])
def test_calculate_tax_parametrized(price, tax_rate, expected):
    """税込価格の計算（パラメータ化）
    
    Args:
        price: 価格
        tax_rate: 税率
        expected: 期待される税込価格
    """
    result = calculate_tax(price, tax_rate)
    assert result == expected
```

### 実行結果

```bash
$ pytest test_file.py::test_calculate_tax_parametrized -v

test_file.py::test_calculate_tax_parametrized[100-0.1-110] PASSED
test_file.py::test_calculate_tax_parametrized[200-0.1-220] PASSED
test_file.py::test_calculate_tax_parametrized[1000-0.08-1080] PASSED
test_file.py::test_calculate_tax_parametrized[500-0.0-500] PASSED
```

### ポイント
- `@pytest.mark.parametrize`デコレーターを使用
- 第1引数：パラメータ名（カンマ区切り）
- 第2引数：テストデータのリスト
- 1つのテストで複数のケースを実行

---

## 13. 例外のテスト

### シーン
「例外が正しく発生するか確認したい」

### 実装コード

```python
class BankAccount:
    """銀行口座クラス"""
    def __init__(self, balance: float):
        if balance < 0:
            raise ValueError("残高はマイナスにできません")
        self.balance = balance
```

### テストコード

```python
import pytest

def test_negative_balance_raises_error():
    """マイナス残高で例外が発生"""
    with pytest.raises(ValueError):
        BankAccount(-1000)

def test_exception_message():
    """例外メッセージも確認"""
    with pytest.raises(ValueError, match="マイナスにできません"):
        BankAccount(-1000)

def test_no_exception_with_valid_balance():
    """正常な残高では例外が発生しない"""
    # 例外が発生しないことを確認
    account = BankAccount(1000)
    assert account.balance == 1000
```

### ポイント
- `pytest.raises(ExceptionType)`で例外をキャッチ
- `match`パラメータでメッセージを検証
- 例外が発生しないケースもテスト

---

## 14. プロパティ（setter付き）のテスト

### シーン
「getterとsetterの両方をテストしたい」

### 実装コード

```python
class Product:
    """商品クラス"""
    def __init__(self, price: float):
        self._price = price
    
    @property
    def price(self) -> float:
        """価格を取得"""
        return self._price
    
    @price.setter
    def price(self, value: float):
        """価格を設定"""
        if value < 0:
            raise ValueError("価格はマイナスにできません")
        self._price = value
```

### テストコード

```python
def test_property_getter():
    """getterのテスト"""
    product = Product(1000)
    assert product.price == 1000

def test_property_setter():
    """setterのテスト"""
    product = Product(1000)
    
    # 価格を変更
    product.price = 2000
    assert product.price == 2000

def test_property_setter_validation():
    """setterのバリデーション"""
    product = Product(1000)
    
    # マイナスの価格を設定しようとする
    with pytest.raises(ValueError, match="マイナスにできません"):
        product.price = -100
    
    # 価格は変わっていない
    assert product.price == 1000
```

### ポイント
- getterとsetterを別々にテスト
- setterのバリデーションも確認

---

## 15. 統合テスト

### シーン
「複数のクラスを組み合わせた動作を確認したい」

### 実装コード

```python
class User:
    """ユーザークラス"""
    def __init__(self, name: str):
        self.name = name
        self.items = []
    
    def add_item(self, item):
        """アイテムを追加"""
        self.items.append(item)

class Item:
    """アイテムクラス"""
    def __init__(self, name: str, price: int):
        self.name = name
        self.price = price
```

### テストコード

```python
def test_user_with_items_integration():
    """ユーザーとアイテムの統合テスト"""
    # ステップ1: ユーザーを作成
    user = User("太郎")
    assert len(user.items) == 0
    
    # ステップ2: アイテムを作成
    item1 = Item("リンゴ", 100)
    item2 = Item("バナナ", 150)
    
    # ステップ3: ユーザーにアイテムを追加
    user.add_item(item1)
    user.add_item(item2)
    
    # ステップ4: 結果を確認
    assert len(user.items) == 2
    assert user.items[0].name == "リンゴ"
    assert user.items[1].name == "バナナ"
    
    # ステップ5: 合計金額を計算
    total = sum(item.price for item in user.items)
    assert total == 250
```

### ポイント
- 複数のクラスを組み合わせてテスト
- ステップごとに状態を確認
- 実際の使用シナリオをテスト

---

## 🚀 実行コマンド集

```bash
# 基本的な実行
pytest

# 詳細表示
pytest -v

# 特定のファイルだけ実行
pytest test_user.py

# 特定のテストクラスだけ実行
pytest test_user.py::TestUser

# 特定のテストメソッドだけ実行
pytest test_user.py::TestUser::test_initialization

# カバレッジ測定
pytest --cov=your_module --cov-report=html

# 失敗したテストだけ再実行
pytest --lf

# 最初に失敗したテストで停止
pytest -x

# 並列実行（pytest-xdist必要）
pytest -n auto

# 詳細な出力
pytest -vv

# 標準出力を表示
pytest -s
```

---

## 📊 よく使うアサーション一覧

```python
# 等価・不等価
assert a == b
assert a != b

# 比較
assert a > b
assert a >= b
assert a < b
assert a <= b

# 真偽値
assert condition
assert not condition

# コレクション
assert item in collection
assert item not in collection

# 型チェック
assert isinstance(obj, ClassName)

# None チェック
assert value is None
assert value is not None

# 属性の存在
assert hasattr(obj, 'attribute_name')

# 呼び出し可能
assert callable(func)

# 長さ
assert len(collection) == expected_length

# 空チェック
assert not collection  # 空
assert collection      # 空でない
```

---

## 💡 ベストプラクティス

### 1. テスト名は分かりやすく

```python
# ❌ 悪い例
def test1():
    pass

# ✅ 良い例
def test_user_creation_with_valid_data():
    pass
```

### 2. AAAパターンを使う

```python
def test_withdraw():
    # Arrange（準備）
    account = BankAccount(1000)
    
    # Act（実行）
    result = account.withdraw(300)
    
    # Assert（検証）
    assert result is True
    assert account.balance == 700
```

### 3. テストは独立させる

```python
# ❌ 悪い例（テストが依存）
user = User("太郎")  # グローバル変数

def test_first():
    user.age = 25

def test_second():
    assert user.age == 25  # test_firstに依存

# ✅ 良い例（独立）
def test_first():
    user = User("太郎")
    user.age = 25
    assert user.age == 25

def test_second():
    user = User("太郎")
    user.age = 30
    assert user.age == 30
```

### 4. エッジケースをテスト

- 境界値（0、最大値、最小値）
- 空のコレクション
- None
- 異常な入力

### 5. テストは小さく

```python
# ❌ 悪い例（1つのテストで複数のことをテスト）
def test_everything():
    user = User("太郎")
    user.age = 25
    user.email = "taro@example.com"
    assert user.age == 25
    assert user.email == "taro@example.com"

# ✅ 良い例（1つのテストで1つのことをテスト）
def test_user_age():
    user = User("太郎")
    user.age = 25
    assert user.age == 25

def test_user_email():
    user = User("太郎")
    user.email = "taro@example.com"
    assert user.email == "taro@example.com"
```

---

## 🎯 まとめ

この記事では、実務でよく使う15のテストパターンを紹介しました。

### 重要ポイント

1. **基本のアサーション**から始めよう
2. **capsys**で標準出力をキャプチャ
3. **フィクスチャ**で共通処理を再利用
4. **パラメータ化**で効率的にテスト
5. **エッジケース**を忘れずにテスト

### 次のステップ

- モックとパッチを学ぶ
- CI/CDでテストを