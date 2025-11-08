"""
Python breakpoint() とpdbデバッガー完全ガイド

実務で使える対話的デバッグの技術
"""

# ===================================================================
# 基本1: breakpoint()の使い方
# ===================================================================

def example_1_basic_breakpoint():
    """
    最も基本的な breakpoint() の使い方
    
    実行するとこの位置でプログラムが停止し、
    pdb(Pythonデバッガー)が起動します
    """
    
    print("処理開始")
    
    # 変数を準備
    name = "田中太郎"
    age = 25
    salary = 300000
    
    # ここでプログラムを一時停止
    # コメントアウトを外すと実行時に停止します
    # breakpoint()
    
    # デバッガーで以下のコマンドが使えます:
    # p name         → 変数nameの値を表示
    # p age          → 変数ageの値を表示
    # p salary * 12  → 計算結果を表示
    # n              → 次の行へ（ステップオーバー）
    # s              → 関数内に入る（ステップイン）
    # c              → 次のbreakpointまで実行
    # q              → デバッガーを終了
    
    result = salary * 12
    print(f"{name}さんの年収: {result}円")
    
    print("処理完了")


# ===================================================================
# 基本2: 条件付きbreakpoint
# ===================================================================

def example_2_conditional_breakpoint():
    """
    特定の条件でのみbreakpointを発動
    """
    
    for i in range(10):
        # iが5の時だけデバッガーを起動
        if i == 5:
            # breakpoint()  # コメントアウトを外すとi=5で停止
            pass
        
        print(f"i = {i}")


# ===================================================================
# 基本3: 関数内でのデバッグ
# ===================================================================

def calculate_tax(price: int) -> int:
    """税込価格を計算"""
    
    tax_rate = 0.1
    
    # ここでbreakpointを設定すると、
    # 関数が呼ばれるたびに停止する
    # breakpoint()
    
    tax = int(price * tax_rate)
    total = price + tax
    
    return total


def example_3_function_debug():
    """関数内のデバッグ"""
    
    prices = [1000, 2000, 3000]
    
    for price in prices:
        total = calculate_tax(price)
        print(f"税抜: {price}円 → 税込: {total}円")


# ===================================================================
# 実践4: 例外発生時に自動でbreakpoint
# ===================================================================

def example_4_exception_breakpoint():
    """
    例外が発生した時に自動でデバッガーを起動
    
    post_mortem を使うと、エラー発生時の状態を確認できる
    """
    import sys
    
    def risky_function(a, b):
        """エラーが発生する可能性がある関数"""
        result = a / b  # bが0だとエラー
        return result
    
    try:
        result = risky_function(10, 0)
        print(f"結果: {result}")
    except Exception as e:
        print(f"エラー発生: {e}")
        
        # エラー発生時にデバッガーを起動
        # コメントアウトを外すとエラー時の状態を確認できます
        # import pdb
        # pdb.post_mortem(sys.exc_info()[2])


# ===================================================================
# 実践5: ループ内の特定データをデバッグ
# ===================================================================

def example_5_loop_debug():
    """
    ループ内で特定のデータだけをデバッグ
    """
    
    users = [
        {"id": 1, "name": "田中", "age": 25, "role": "engineer"},
        {"id": 2, "name": "佐藤", "age": 30, "role": "manager"},
        {"id": 3, "name": "鈴木", "age": 22, "role": "engineer"},
        {"id": 4, "name": "高橋", "age": 28, "role": "designer"},
    ]
    
    for user in users:
        # 特定のユーザーだけをデバッグ
        if user["name"] == "佐藤":
            print(f"デバッグ対象: {user['name']}")
            # breakpoint()  # この時点でuser変数の中身を確認できる
        
        # 処理続行
        print(f"処理中: {user['name']} ({user['role']})")


# ===================================================================
# 実践6: クラスメソッド内のデバッグ
# ===================================================================

class BankAccount:
    """銀行口座クラス（デバッグ例）"""
    
    def __init__(self, owner: str, balance: int = 0):
        self.owner = owner
        self.balance = balance
    
    def deposit(self, amount: int):
        """入金"""
        print(f"{self.owner}: {amount}円を入金")
        
        # 入金前の状態を確認したい場合
        # breakpoint()  # self.balanceを確認できる
        
        self.balance += amount
        
        # 入金後の状態を確認したい場合
        # breakpoint()  # 更新後のself.balanceを確認できる
    
    def withdraw(self, amount: int) -> bool:
        """出金"""
        print(f"{self.owner}: {amount}円を出金試行")
        
        # 残高が不足する場合のデバッグ
        if self.balance < amount:
            print(f"  残高不足: 残高={self.balance}, 出金額={amount}")
            # breakpoint()  # 不足時の状態を確認
            return False
        
        self.balance -= amount
        return True


def example_6_class_debug():
    """クラス内のデバッグ"""
    
    account = BankAccount("田中太郎", 10000)
    
    account.deposit(5000)
    print(f"残高: {account.balance}円")
    
    account.withdraw(20000)  # 残高不足になる
    print(f"残高: {account.balance}円")


# ===================================================================
# 実践7: pdbの便利なコマンド一覧
# ===================================================================

def example_7_pdb_commands():
    """
    pdbデバッガーで使える便利なコマンド
    
    === 基本コマンド ===
    h (help)           : ヘルプを表示
    h <command>        : 特定のコマンドのヘルプ
    
    === 実行制御 ===
    n (next)           : 次の行へ（関数呼び出しはスキップ）
    s (step)           : 次の行へ（関数内に入る）
    c (continue)       : 次のbreakpointまで実行
    r (return)         : 現在の関数から戻るまで実行
    q (quit)           : デバッガーを終了
    
    === 変数確認 ===
    p <expression>     : 式の値を表示（例: p name）
    pp <expression>    : 整形して表示（例: pp user_dict）
    a (args)           : 現在の関数の引数を表示
    
    === コンテキスト確認 ===
    l (list)           : 現在の行周辺のコードを表示
    ll (longlist)      : 現在の関数全体を表示
    w (where)          : スタックトレースを表示
    u (up)             : スタックを1つ上に移動
    d (down)           : スタックを1つ下に移動
    
    === ブレークポイント管理 ===
    b (break)          : ブレークポイント一覧
    b <line>           : 指定行にブレークポイント設定
    b <file>:<line>    : 指定ファイルの指定行に設定
    cl (clear)         : ブレークポイントをクリア
    
    === その他 ===
    ! <statement>      : Python文を実行（例: ! x = 10）
    interact           : 対話モードに入る
    """
    
    data = [1, 2, 3, 4, 5]
    total = 0
    
    # breakpoint()  # ここで停止して上記コマンドを試せます
    
    for item in data:
        total += item
    
    print(f"合計: {total}")


# ===================================================================
# 実践8: カスタムデバッガー関数
# ===================================================================

def debug_vars(**kwargs):
    """
    変数の値を見やすく表示してからbreakpointを起動
    
    使用例:
        debug_vars(name=name, age=age, salary=salary)
    """
    print("\n" + "=" * 60)
    print("■ デバッグ情報")
    print("=" * 60)
    
    for key, value in kwargs.items():
        print(f"{key:15} = {value!r:30} (type: {type(value).__name__})")
    
    print("=" * 60)
    # breakpoint()  # 情報表示後にデバッガーを起動


def example_8_custom_debug():
    """カスタムデバッガー関数の使用例"""
    
    name = "田中太郎"
    age = 25
    skills = ["Python", "JavaScript", "SQL"]
    
    # 変数の値を表示してからデバッグ
    debug_vars(name=name, age=age, skills=skills)
    
    print("処理続行...")


# ===================================================================
# 実践9: リモートデバッグ（pdb over telnet）
# ===================================================================

def example_9_remote_debug():
    """
    リモートデバッグの概念
    
    本番環境やDockerコンテナ内でのデバッグに使用
    実際に使う場合は別途設定が必要
    """
    
    print("""
    リモートデバッグの方法:
    
    1. rpdbをインストール
       pip install rpdb
    
    2. コード内でrpdbを使用
       import rpdb
       rpdb.set_trace()  # 4444ポートでリモートデバッグ待機
    
    3. 別の端末から接続
       telnet localhost 4444
    
    ※本番環境では使用しないこと（セキュリティリスク）
    ※開発・テスト環境のみで使用
    """)


# ===================================================================
# 実践10: 環境変数でbreakpointの無効化
# ===================================================================

def example_10_disable_breakpoint():
    """
    環境変数でbreakpointを無効化
    
    本番環境では PYTHONBREAKPOINT=0 を設定することで
    breakpoint()をすべて無効化できる
    """
    import os
    
    print(f"PYTHONBREAKPOINT: {os.environ.get('PYTHONBREAKPOINT', '未設定')}")
    
    # 環境変数で無効化されている場合、このbreakpointは動作しない
    # breakpoint()
    
    print("""
    環境変数での制御:
    
    # breakpointを無効化（本番環境）
    export PYTHONBREAKPOINT=0
    
    # breakpointを有効化（デフォルト）
    unset PYTHONBREAKPOINT
    
    # 別のデバッガーを使用
    export PYTHONBREAKPOINT=ipdb.set_trace
    """)


# ===================================================================
# チートシート
# ===================================================================

def print_cheatsheet():
    """pdbコマンドチートシート"""
    
    cheatsheet = """
╔═══════════════════════════════════════════════════════════════╗
║              Python pdb デバッガー チートシート                ║
╠═══════════════════════════════════════════════════════════════╣
║ 【基本操作】                                                   ║
║   h, help          ヘルプ表示                                  ║
║   q, quit          デバッガー終了                              ║
║                                                                ║
║ 【実行制御】                                                   ║
║   n, next          次の行へ（関数はスキップ）                  ║
║   s, step          ステップイン（関数内に入る）                ║
║   c, continue      次のbreakpointまで実行                      ║
║   r, return        現在の関数から戻るまで実行                  ║
║   unt <line>       指定行まで実行                              ║
║                                                                ║
║ 【変数確認】                                                   ║
║   p <expr>         式の値を表示                                ║
║   pp <expr>        整形して表示                                ║
║   a, args          関数の引数を表示                            ║
║   display <expr>   ステップごとに式の値を表示                  ║
║   undisplay        display解除                                 ║
║                                                                ║
║ 【コード表示】                                                 ║
║   l, list          現在の行周辺を表示                          ║
║   ll, longlist     現在の関数全体を表示                        ║
║   w, where         スタックトレース表示                        ║
║                                                                ║
║ 【ブレークポイント】                                           ║
║   b                ブレークポイント一覧                        ║
║   b <line>         行番号でブレークポイント設定                ║
║   b <func>         関数名でブレークポイント設定                ║
║   cl <number>      ブレークポイント削除                        ║
║   disable <n>      ブレークポイント無効化                      ║
║   enable <n>       ブレークポイント有効化                      ║
║                                                                ║
║ 【スタック操作】                                               ║
║   u, up            スタックを1つ上へ                           ║
║   d, down          スタックを1つ下へ                           ║
║                                                                ║
║ 【便利機能】                                                   ║
║   !<statement>     Python文を実行（例: !x = 10）               ║
║   interact         対話モードに入る                            ║
║   alias            コマンドのエイリアス設定                    ║
╚═══════════════════════════════════════════════════════════════╝

【よく使うコマンド組み合わせ】
  p locals()          ローカル変数を全て表示
  p globals()         グローバル変数を全て表示
  p vars(obj)         オブジェクトの属性を全て表示
  p dir(obj)          オブジェクトのメソッド一覧
  pp <complex_obj>    複雑なオブジェクトを整形表示

【Tips】
  • Enter連打で前回のコマンドを繰り返し
  • 変数名とコマンドが被る場合は !変数名 で参照
  • 環境変数 PYTHONBREAKPOINT=0 で全breakpoint無効化
"""
    
    print(cheatsheet)


# ===================================================================
# メイン実行
# ===================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("Python breakpoint() 完全ガイド")
    print("=" * 70)
    
    print("\n各コードの breakpoint() のコメントアウトを外すと")
    print("実際にデバッガーを体験できます！\n")
    
    print("\n■ チートシート")
    print("-" * 70)
    print_cheatsheet()
    
    print("\n■ 例1: 基本的な使い方")
    print("-" * 70)
    example_1_basic_breakpoint()
    
    print("\n■ 例2: 条件付きbreakpoint")
    print("-" * 70)
    example_2_conditional_breakpoint()
    
    print("\n■ 例3: 関数内のデバッグ")
    print("-" * 70)
    example_3_function_debug()
    
    print("\n■ 例4: 例外時のデバッグ")
    print("-" * 70)
    example_4_exception_breakpoint()
    
    print("\n■ 例5: ループ内のデバッグ")
    print("-" * 70)
    example_5_loop_debug()
    
    print("\n■ 例6: クラス内のデバッグ")
    print("-" * 70)
    example_6_class_debug()
    
    print("\n■ 例7: pdbコマンド一覧")
    print("-" * 70)
    example_7_pdb_commands()
    
    print("\n■ 例8: カスタムデバッガー")
    print("-" * 70)
    example_8_custom_debug()
    
    print("\n■ 例9: リモートデバッグ")
    print("-" * 70)
    example_9_remote_debug()
    
    print("\n■ 例10: breakpointの無効化")
    print("-" * 70)
    example_10_disable_breakpoint()
    
    print("\n" + "=" * 70)
    print("すべての例を実行完了！")
    print("=" * 70)