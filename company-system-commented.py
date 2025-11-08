"""
会社管理システム

このモジュールは、社員、社長、会社を管理するためのクラスを提供します。

Classes:
    Gender: 性別を表す列挙型
    Post: 役職を表す列挙型
    Human: 人間の基底クラス
    President: 社長クラス
    Employee: 社員クラス
    Company: 会社クラス
"""

# ===================================================================
# モジュールのインポート
# ===================================================================

from enum import Enum  # 列挙型（Enum）を使うためのクラスをインポート
from typing import List, Optional  # 型ヒント用：List（リスト型）、Optional（None許可型）
import random  # ランダムな数値を生成するためのモジュール


# ===================================================================
# 列挙型クラス（Enum）の定義
# ===================================================================

class Gender(Enum):
    """
    性別を表す列挙型
    
    列挙型は固定された選択肢を定義する時に使う
    Gender.MAN のようにアクセスして、値の間違いを防ぐ

    Attributes:
        MAN: 男性
        WOMAN: 女性
        OTHER: その他
    """

    MAN = "男性"      # Gender.MAN で "男性" という文字列にアクセス
    WOMAN = "女性"    # Gender.WOMAN で "女性" という文字列にアクセス
    OTHER = "その他"  # Gender.OTHER で "その他" という文字列にアクセス


class Post(Enum):
    """
    役職を表す列挙型
    
    社員の役職を管理するための列挙型
    昇進・降格の順序も暗黙的に定義される

    Attributes:
        HIRA: 平社員
        SYUNIN: 主任
        KATYO: 課長
        YARUIN: 役員
    """

    HIRA = "ヒラ"    # Post.HIRA で "ヒラ" という文字列にアクセス
    SYUNIN = "主任"  # Post.SYUNIN で "主任" という文字列にアクセス
    KATYO = "課長"   # Post.KATYO で "課長" という文字列にアクセス
    YARUIN = "役員"  # Post.YARUIN で "役員" という文字列にアクセス


# ===================================================================
# 基底クラス：Human（人間）
# ===================================================================

class Human:
    """
    人間を表す基底クラス
    
    社員（Employee）と社長（President）の共通部分を定義
    継承元となるスーパークラス

    Attributes:
        name (str): 名前
        gender (Gender): 性別
        age (int): 年齢
    """

    def __init__(self, name: str, gender: Gender, age: int):
        """
        Humanクラスのコンストラクタ
        
        オブジェクト生成時に呼ばれる初期化メソッド
        引数で受け取った値をインスタンス変数に保存

        Args:
            name (str): 名前
            gender (Gender): 性別（Gender列挙型）
            age (int): 年齢
        """
        # 引数 name を protected属性 _name に保存
        # _name の _ は「外部から直接アクセスしないで」という慣例
        self._name = name
        
        # 引数 gender を protected属性 _gender に保存
        self._gender = gender
        
        # 引数 age を protected属性 _age に保存
        self._age = age

    @property  # デコレータ：このメソッドをプロパティ（属性のように使える）にする
    def name(self) -> str:
        """
        名前を取得するプロパティ（getter）
        
        obj.name でアクセス可能（メソッドだが括弧不要）
        読み取り専用（setterがないので変更不可）

        Returns:
            str: 名前
        """
        return self._name  # 内部の _name を返す

    @property  # プロパティ化
    def gender(self) -> Gender:
        """
        性別を取得するプロパティ（getter）
        
        読み取り専用

        Returns:
            Gender: 性別（Gender列挙型）
        """
        return self._gender  # 内部の _gender を返す

    @property  # プロパティ化
    def age(self) -> int:
        """
        年齢を取得するプロパティ（getter）
        
        読み取り専用

        Returns:
            int: 年齢
        """
        return self._age  # 内部の _age を返す

    def do_self_introduction(self) -> None:
        """
        自己紹介を行うメソッド
        
        継承先のクラスでオーバーライド（上書き）される
        基本的な自己紹介の形式を提供

        Returns:
            None: 戻り値なし（画面出力のみ）
        """
        # f-string（フォーマット文字列）で変数を埋め込み
        # self.name はプロパティ経由で _name にアクセス
        # self.gender.value で Gender列挙型の値（"男性"等）を取得
        print(
            f"私の名前は{self.name}です。性別は{self.gender.value}で、年齢は{self.age}歳です。"
        )


# ===================================================================
# 継承クラス：Employee（社員）
# ===================================================================

class Employee(Human):
    """
    社員を表すクラス
    
    Humanクラスを継承し、役職・給与・IDなどの社員特有の情報を追加

    Attributes:
        post (Post): 役職
        id (str): 社員ID
        _salary_map (dict): 役職と給与のマッピング（クラス変数）
    """

    # クラス変数：全てのEmployeeインスタンスで共有される辞書
    # 役職（Post列挙型）をキー、給与（int）を値とする
    _salary_map = {
        Post.HIRA: 200000,    # ヒラ社員：20万円
        Post.SYUNIN: 300000,  # 主任：30万円
        Post.KATYO: 450000,   # 課長：45万円
        Post.YARUIN: 600000,  # 役員：60万円
    }

    def __init__(self, name: str, gender: Gender, age: int, post: Post):
        """
        Employeeクラスのコンストラクタ
        
        親クラス（Human）のコンストラクタも呼び出す

        Args:
            name (str): 名前
            gender (Gender): 性別
            age (int): 年齢
            post (Post): 役職
        """
        # super() で親クラス（Human）のコンストラクタを呼び出し
        # name, gender, age を親クラスに渡して初期化
        super().__init__(name, gender, age)
        
        # 引数 post を protected属性 _post に保存
        self._post = post
        
        # _generate_id() メソッドを呼び出して社員IDを生成
        # 生成されたIDを _id に保存
        self._id = self._generate_id()

    def _generate_id(self) -> str:
        """
        社員IDを生成するプライベートメソッド
        
        _で始まるメソッド名は「内部実装用」という慣例
        ランダムな4桁の数字を生成して文字列として返す

        Returns:
            str: 社員ID（例："1234"）
        """
        # random.randint(1000, 9999) で 1000〜9999 のランダムな整数を生成
        # str() で文字列に変換して返す
        return str(random.randint(1000, 9999))

    @property  # プロパティ化
    def post(self) -> Post:
        """
        役職を取得するプロパティ（getter）
        
        読み取り専用（setterなし）
        ※昇進・降格は promote(), demote() メソッドで行う

        Returns:
            Post: 役職（Post列挙型）
        """
        return self._post  # 内部の _post を返す

    @property  # プロパティ化
    def salary(self) -> int:
        """
        給与を取得するプロパティ（getter）
        
        現在の役職に応じた給与を _salary_map から取得
        読み取り専用（給与は役職で自動決定）

        Returns:
            int: 給与額
        """
        # クラス変数 _salary_map を参照
        # self._post をキーにして対応する給与を取得
        return self._salary_map[self._post]

    @property  # プロパティ化
    def id(self) -> str:
        """
        社員IDを取得するプロパティ（getter）
        
        読み取り専用（IDは生成時に固定）

        Returns:
            str: 社員ID
        """
        return self._id  # 内部の _id を返す

    def do_self_introduction(self) -> None:
        """
        自己紹介を行うメソッド（オーバーライド）
        
        親クラス（Human）のメソッドを上書き
        社員版の自己紹介（役職情報を追加）

        Returns:
            None: 戻り値なし
        """
        # 親クラスとほぼ同じだが、役職情報を追加
        # self.post.value で Post列挙型の値（"ヒラ"等）を取得
        print(
            f"私の名前は{self.name}です。性別は{self.gender.value}で、"
            f"年齢は{self.age}歳、役職は{self.post.value}です。"
        )

    def promote(self) -> None:
        """
        昇進するメソッド
        
        現在の役職から1つ上の役職に昇進
        すでに最高役職（役員）の場合は昇進しない

        Returns:
            None: 戻り値なし
        """
        # 役職の昇進順序をリストで定義（低い順）
        post_order = [Post.HIRA, Post.SYUNIN, Post.KATYO, Post.YARUIN]
        
        # list.index() で現在の役職のインデックスを取得
        # 例：Post.HIRA なら 0、Post.SYUNIN なら 1
        current_index = post_order.index(self._post)

        # 現在のインデックスがリストの最後より前かチェック
        if current_index < len(post_order) - 1:
            # 1つ上の役職に昇進（インデックスを+1）
            self._post = post_order[current_index + 1]
            # 昇進メッセージを表示
            print(f"{self.name}さんが{self.post.value}に昇進しました！")
        else:
            # すでに最高役職の場合
            print(f"{self.name}さんはすでに最高役職です。")

    def demote(self) -> None:
        """
        降格するメソッド
        
        現在の役職から1つ下の役職に降格
        すでに最低役職（ヒラ）の場合は降格しない

        Returns:
            None: 戻り値なし
        """
        # 役職の順序リスト（promote() と同じ）
        post_order = [Post.HIRA, Post.SYUNIN, Post.KATYO, Post.YARUIN]
        
        # 現在の役職のインデックスを取得
        current_index = post_order.index(self._post)

        # 現在のインデックスが0より大きいかチェック
        if current_index > 0:
            # 1つ下の役職に降格（インデックスを-1）
            self._post = post_order[current_index - 1]
            # 降格メッセージを表示
            print(f"{self.name}さんが{self.post.value}に降格しました。")
        else:
            # すでに最低役職の場合
            print(f"{self.name}さんはすでに最低役職です。")


# ===================================================================
# 継承クラス：President（社長）
# ===================================================================

class President(Human):
    """
    社長を表すクラス
    
    Humanクラスを継承し、給与・会社情報などの社長特有の情報を追加
    会社の管理機能（社員の追加・削除・検索など）を持つ

    Attributes:
        _salary (int): 社長の給与
        company (Company): 所属する会社
    """

    def __init__(self, name: str, gender: Gender, age: int):
        """
        Presidentクラスのコンストラクタ
        
        親クラス（Human）のコンストラクタも呼び出す

        Args:
            name (str): 名前
            gender (Gender): 性別
            age (int): 年齢
        """
        # 親クラス（Human）のコンストラクタを呼び出し
        super().__init__(name, gender, age)
        
        # 社長の給与を100万円に設定
        self._salary = 1000000
        
        # 会社は後から設定されるので、最初はNoneで初期化
        # Optional["Company"] は「Companyクラスまたはnone」という型ヒント
        # 文字列 "Company" は前方参照（クラスがまだ定義されていないため）
        self._company: Optional["Company"] = None

    @property  # プロパティ化
    def salary(self) -> int:
        """
        給与を取得するプロパティ（getter）
        
        読み取り専用

        Returns:
            int: 給与額（100万円固定）
        """
        return self._salary  # 内部の _salary を返す

    @property  # プロパティ化
    def company(self) -> Optional["Company"]:
        """
        会社を取得するプロパティ（getter）
        
        社長が所属する会社オブジェクトを返す

        Returns:
            Optional[Company]: 所属する会社（未設定の場合はNone）
        """
        return self._company  # 内部の _company を返す

    @company.setter  # companyプロパティのsetter
    def company(self, company: "Company") -> None:
        """
        会社を設定するプロパティ（setter）
        
        president.company = some_company のように代入時に呼ばれる

        Args:
            company (Company): 所属する会社

        Returns:
            None: 戻り値なし
        """
        # 引数で受け取った会社オブジェクトを _company に保存
        self._company = company

    def do_self_introduction(self) -> None:
        """
        自己紹介を行うメソッド（オーバーライド）
        
        親クラス（Human）のメソッドを上書き
        社長版の自己紹介

        Returns:
            None: 戻り値なし
        """
        # 社長であることを明示した自己紹介
        print(
            f"私の名前は{self.name}です。性別は{self.gender.value}で、"
            f"年齢は{self.age}歳、社長です。"
        )

    def get_personnel_by_id(self, id: str) -> Optional[Employee]:
        """
        IDで社員を検索するメソッド
        
        社員IDを指定して該当する社員オブジェクトを取得

        Args:
            id (str): 社員ID

        Returns:
            Optional[Employee]: 見つかった社員、見つからない場合はNone
        """
        # 会社が設定されていない場合はNoneを返す
        if self._company is None:
            return None

        # 会社の全社員をループで検索
        for employee in self._company.employees:
            # 社員のIDが一致するかチェック
            if employee.id == id:
                # 見つかったらその社員を返す
                return employee
        
        # 見つからなければNoneを返す
        return None

    def get_personnel_by_name(self, name: str) -> Optional[Employee]:
        """
        名前で社員を検索するメソッド
        
        社員名を指定して該当する社員オブジェクトを取得

        Args:
            name (str): 社員名

        Returns:
            Optional[Employee]: 見つかった社員、見つからない場合はNone
        """
        # 会社が設定されていない場合はNoneを返す
        if self._company is None:
            return None

        # 会社の全社員をループで検索
        for employee in self._company.employees:
            # 社員の名前が一致するかチェック
            if employee.name == name:
                # 見つかったらその社員を返す
                return employee
        
        # 見つからなければNoneを返す
        return None

    def add_employee(self, name: str, gender: Gender, age: int, post: Post) -> None:
        """
        社員を追加するメソッド
        
        新しい社員を会社に採用する
        実際の追加処理は Company クラスに委譲

        Args:
            name (str): 名前
            gender (Gender): 性別
            age (int): 年齢
            post (Post): 役職

        Returns:
            None: 戻り値なし
        """
        # 会社が設定されていない場合はエラーメッセージを表示
        if self._company is None:
            print("会社が設定されていません。")
            return  # メソッドを終了

        # 会社の add_employee() メソッドを呼び出して社員を追加
        self._company.add_employee(name, gender, age, post)

    def delete_employee(self, person: Employee) -> None:
        """
        社員を削除するメソッド
        
        指定した社員を会社から退職させる
        実際の削除処理は Company クラスに委譲

        Args:
            person (Employee): 削除する社員オブジェクト

        Returns:
            None: 戻り値なし
        """
        # 会社が設定されていない場合はエラーメッセージを表示
        if self._company is None:
            print("会社が設定されていません。")
            return  # メソッドを終了

        # 会社の delete_employee() メソッドを呼び出して社員を削除
        self._company.delete_employee(person)

    def resignation(self) -> Optional["President"]:
        """
        辞任するメソッド（追加課題）
        
        現社長が辞任し、次期社長を選出する
        次期社長は社員の中から選ばれる

        Returns:
            Optional[President]: 新しい社長、社員がいない場合はNone
        """
        # 会社が設定されていない場合
        if self._company is None:
            print("会社が設定されていません。")
            return None  # Noneを返してメソッド終了

        # 社員が0人の場合は辞任できない
        if len(self._company.employees) == 0:
            print("いいえ、私以外に社員がいない場合は辞任しないでください")
            return None  # Noneを返してメソッド終了

        # 会社の select_president() メソッドで次期社長候補を選出
        # 役員がいれば役員の最年長、いなければ全社員の最年長
        next_president_employee = self._company.select_president()

        # 候補が見つからなかった場合（通常は発生しない）
        if next_president_employee is None:
            print("次期社長候補が見つかりません。")
            return None  # Noneを返してメソッド終了

        # 次期社長は社員から昇格するので、社員リストから削除
        self._company.delete_employee(next_president_employee)

        # 選ばれた社員の情報を使って新しいPresidentオブジェクトを作成
        new_president = President(
            next_president_employee.name,    # 名前を引き継ぐ
            next_president_employee.gender,  # 性別を引き継ぐ
            next_president_employee.age,     # 年齢を引き継ぐ
        )

        # 新社長に会社を設定（setter経由）
        new_president.company = self._company

        # 辞任メッセージを表示
        print(f"{self.name}は{new_president.name}、辞任はだいた！")

        # 新しい社長オブジェクトを返す
        return new_president


# ===================================================================
# クラス：Company（会社）
# ===================================================================

class Company:
    """
    会社を表すクラス
    
    社員の管理（追加・削除・検索）を行う
    社員リストを保持し、次期社長の選出も担当

    Attributes:
        MAX_NUMBER_OF_PEOPLE (int): 最大社員数（クラス変数）
        current_number (int): 現在の社員数
        employees (List[Employee]): 社員リスト
    """

    # クラス変数：最大社員数を10名に設定
    # 全てのCompanyインスタンスで共有される
    MAX_NUMBER_OF_PEOPLE = 10

    def __init__(self):
        """
        Companyクラスのコンストラクタ
        
        空の社員リストで初期化
        """
        # 空のリストで初期化
        # List[Employee] は「Employeeオブジェクトのリスト」という型ヒント
        self._employees: List[Employee] = []

    @property  # プロパティ化
    def current_number(self) -> int:
        """
        現在の社員数を取得するプロパティ（getter）
        
        社員リストの長さを返す

        Returns:
            int: 社員数
        """
        # len() 関数でリストの要素数を取得
        return len(self._employees)

    @property  # プロパティ化
    def employees(self) -> List[Employee]:
        """
        社員リストを取得するプロパティ（getter）
        
        全社員のリストを返す

        Returns:
            List[Employee]: 社員リスト
        """
        return self._employees  # 内部の _employees を返す

    @property  # プロパティ化
    def number_of_employee(self) -> int:
        """
        社員数を取得するプロパティ（getter）
        
        current_number と同じ（互換性のため残されている）

        Returns:
            int: 社員数
        """
        return len(self._employees)  # リストの長さを返す

    def get_personnel_by_id(self, id: str) -> Optional[Employee]:
        """
        IDで社員を検索するメソッド
        
        社員IDを指定して該当する社員を検索

        Args:
            id (str): 社員ID

        Returns:
            Optional[Employee]: 見つかった社員、見つからない場合はNone
        """
        # 社員リストをループで検索
        for employee in self._employees:
            # 社員のIDが一致するかチェック
            if employee.id == id:
                # 見つかったらその社員を返す
                return employee
        
        # 見つからなければNoneを返す
        return None

    def get_personnel_by_name(self, name: str) -> Optional[Employee]:
        """
        名前で社員を検索するメソッド
        
        社員名を指定して該当する社員を検索

        Args:
            name (str): 社員名

        Returns:
            Optional[Employee]: 見つかった社員、見つからない場合はNone
        """
        # 社員リストをループで検索
        for employee in self._employees:
            # 社員の名前が一致するかチェック
            if employee.name == name:
                # 見つかったらその社員を返す
                return employee
        
        # 見つからなければNoneを返す
        return None

    def add_employee(self, name: str, gender: Gender, age: int, post: Post) -> None:
        """
        社員を追加するメソッド
        
        新しい社員を作成して社員リストに追加
        最大社員数を超える場合は追加しない

        Args:
            name (str): 名前
            gender (Gender): 性別
            age (int): 年齢
            post (Post): 役職

        Returns:
            None: 戻り値なし
        """
        # 現在の社員数が最大数以上かチェック
        if self.current_number >= self.MAX_NUMBER_OF_PEOPLE:
            # 上限に達している場合はエラーメッセージを表示
            print(f"社員数が上限（{self.MAX_NUMBER_OF_PEOPLE}名）に達しています。")
            return  # メソッドを終了（追加しない）

        # 新しいEmployeeオブジェクトを作成
        # コンストラクタに名前・性別・年齢・役職を渡す
        new_employee = Employee(name, gender, age, post)
        
        # 社員リストに新しい社員を追加
        self._employees.append(new_employee)
        
        # 採用メッセージを表示
        print(f"{name}さん（ID: {new_employee.id}）を採用しました。")

    def delete_employee(self, person: Employee) -> None:
        """
        社員を削除するメソッド
        
        指定された社員を社員リストから削除

        Args:
            person (Employee): 削除する社員オブジェクト

        Returns:
            None: 戻り値なし
        """
        # 社員がリストに存在するかチェック（in演算子）
        if person in self._employees:
            # 存在する場合はリストから削除
            self._employees.remove(person)
            # 削除メッセージを表示
            print(f"{person.name}さんを削除しました。")
        else:
            # 存在しない場合はエラーメッセージを表示
            print(f"{person.name}さんは社員リストに存在しません。")

    def select_president(self) -> Optional[Employee]:
        """
        次期社長を選出するメソッド（追加課題）
        
        次期社長選出基準:
        1. 役員がいる場合：役員の中で最年長の人
        2. 役員がいない場合：全社員の中で最年長の人

        Returns:
            Optional[Employee]: 次期社長候補、社員がいない場合はNone
        """
        # 社員が0人の場合はNoneを返す
        if len(self._employees) == 0:
            return None

        # リスト内包表記で役員のみを抽出
        # [条件に合う要素 for 要素 in リスト if 条件]
        executives = [emp for emp in self._employees if emp.post == Post.YARUIN]

        # 役員リストが空でないかチェック
        if executives:
            # max() 関数で最年長の役員を選出
            # key=lambda e: e.age で「年齢を比較基準にする」という意味
            return max(executives, key=lambda e: e.age)
        else:
            # 役員がいない場合は全社員から最年長を選出
            return max(self._employees, key=lambda e: e.age)

    def display_all_employees(self) -> None:
        """
        全社員の情報を表示するメソッド
        
        社員一覧を表形式で見やすく表示

        Returns:
            None: 戻り値なし
        """
        # 社員が0人の場合
        if len(self._employees) == 0:
            print("社員がいません。")
            return  # メソッドを終了

        # ヘッダー部分を表示
        # "=" * 60 で "=" を60個繰り返した文字列を作成（区切り線）
        print(f"\n{'='*60}")
        
        # タイトルを中央揃えで表示
        # ^54 は「54文字幅で中央揃え」という意味
        print(f"{'社員一覧':^54}")
        
        # 区切り線を表示
        print(f"{'='*60}")
        
        # テーブルのヘッダー行を表示
        # <15 は「15文字幅で左揃え」という意味
        print(f"{'名前':<15} {'性別':<10} {'年齢':<5} {'役職':<10} {'ID':<10}")
        
        # ヘッダーとデータの区切り線
        # "-" * 60 で "-" を60個繰り返した文字列を作成
        print(f"{'-'*60}")

        # 社員リストをループで表示
        for emp in self._employees:
            # 各社員の情報を1行ずつ表示
            # emp.name で名前、emp.gender.value で性別の文字列、など
            print(
                f"{emp.name:<15} {emp.gender.value:<10} {emp.age:<5} {emp.post.value:<10} {emp.id:<10}"
            )

        # フッター部分を表示
        print(f"{'='*60}")
        
        # 合計人数を表示
        # self.current_number でプロパティ経由で社員数を取得
        print(f"合計: {self.current_number}名\n")


# ===================================================================
# メイン関数（テストプログラム）
# ===================================================================

def main():
    """
    メイン関数 - テスト実施
    
    会社管理システムの各機能をテストする
    プログラムのエントリーポイント

    Returns:
        None: 戻り値なし
    """
    # タイトル表示
    print("=" * 60)  # 区切り線（60個の "="）
    print(" 会社管理システム - テストプログラム")
    print("=" * 60)  # 区切り線

    # ===================================================================
    # 1. 社長の作成
    # ===================================================================
    print("\n■ 1. 社長の作成")  # セクションタイトル（\n は改行）
    
    # Presidentオブジェクトを作成
    # 名前："倍井 杉蔵"、性別：男性、年齢：88歳
    president = President("倍井 杉蔵", Gender.MAN, 88)
    
    # 社長の自己紹介メソッドを呼び出し
    president.do_self_introduction()

    # ===================================================================
    # 2. 会社の作成
    # ===================================================================
    print("\n■ 2. 会社の作成")  # セクションタイトル
    
    # Companyオブジェクトを作成（空の会社）
    company = Company()
    
    # 社長に会社を設定（プロパティのsetter経由）
    president.company = company
    
    # 会社設立メッセージを表示
    # Company.MAX_NUMBER_OF_PEOPLE でクラス変数にアクセス
    print(f"会社を設立しました。最大社員数: {Company.MAX_NUMBER_OF_PEOPLE}名")

    # ===================================================================
    # 3. 社員の採用
    # ===================================================================
    print("\n■ 3. 社員の採用")  # セクションタイトル
    
    # 採用する社員のデータをタプルのリストで定義
    # (名前, 性別, 年齢, 役職) の形式
    employees_data = [
        ("佐藤 太郎", Gender.MAN, 22, Post.HIRA),           # ヒラ社員
        ("鈴木 二郎", Gender.MAN, 44, Post.YARUIN),         # 役員
        ("高橋 三郎", Gender.MAN, 33, Post.SYUNIN),         # 主任
        ("田中 しょうこ", Gender.WOMAN, 42, Post.KATYO),    # 課長
        ("渡辺中小路 五郎左衛門", Gender.MAN, 60, Post.HIRA), # ヒラ社員（最年長）
        ("篠崎 六郎", Gender.OTHER, 18, Post.SYUNIN),       # 主任
        ("那奈南波 菜々美", Gender.WOMAN, 19, Post.HIRA),   # ヒラ社員
        ("周 八郎", Gender.MAN, 21, Post.YARUIN),           # 役員
    ]

    # リストの各要素（タプル）をループで取り出す
    # for 変数1, 変数2, 変数3, 変数4 in リスト: でアンパック
    for name, gender, age, post in employees_data:
        # 社長のadd_employeeメソッドを呼び出して社員を追加
        president.add_employee(name, gender, age, post)

    # ===================================================================
    # 4. 社員一覧の表示
    # ===================================================================
    print("\n■ 4. 社員一覧")  # セクションタイトル
    
    # 会社のdisplay_all_employeesメソッドを呼び出し
    # 全社員の情報を表形式で表示
    company.display_all_employees()

    # ===================================================================
    # 5. 検索機能のテスト
    # ===================================================================
    print("\n■ 5. 社員検索")  # セクションタイトル
    
    # 検索する社員の名前を変数に保存
    search_name = "佐藤 太郎"
    
    # 社長のget_personnel_by_nameメソッドで名前検索
    # 戻り値は Employee オブジェクトまたは None
    found_employee = president.get_personnel_by_name(search_name)
    
    # 見つかったかチェック（None でなければ True）
    if found_employee:
        # 見つかった場合：情報を表示
        print(f"名前検索: {search_name}さんが見つかりました（ID: {found_employee.id}）")
        # 見つかった社員の自己紹介メソッドを呼び出し
        found_employee.do_self_introduction()

    # ===================================================================
    # 6. 昇進・降格のテスト
    # ===================================================================
    print("\n■ 6. 昇進・降格テスト")  # セクションタイトル
    
    # found_employee が None でないかチェック
    if found_employee:
        # 1回目の昇進（ヒラ → 主任）
        found_employee.promote()
        
        # 2回目の昇進（主任 → 課長）
        found_employee.promote()
        
        # 1回降格（課長 → 主任）
        found_employee.demote()

    # ===================================================================
    # 7. 追加課題: 次期社長の選出
    # ===================================================================
    print("\n■ 7. 次期社長の選出テスト")  # セクションタイトル
    
    # 会社のselect_presidentメソッドで次期社長候補を選出
    # 役員がいれば役員の最年長、いなければ全社員の最年長
    next_president_candidate = company.select_president()
    
    # 候補が見つかったかチェック
    if next_president_candidate:
        # 候補の情報を表示
        print(
            f"次期社長候補: {next_president_candidate.name}さん "
            f"（年齢: {next_president_candidate.age}歳、役職: {next_president_candidate.post.value}）"
        )

    # ===================================================================
    # 8. 追加課題: 辞任機能のテスト
    # ===================================================================
    print("\n■ 8. 社長の辞任テスト")  # セクションタイトル
    
    # 社長のresignationメソッドを呼び出し
    # 戻り値は新しいPresidentオブジェクトまたはNone
    new_president = president.resignation()

    # 新社長が選出されたかチェック
    if new_president:
        # 新社長の就任メッセージ
        print(f"\n新社長の就任:")
        # 新社長の自己紹介メソッドを呼び出し
        new_president.do_self_introduction()
        # 現在の社員数を表示（次期社長が社員から昇格したので1人減る）
        print(f"現在の社員数: {company.current_number}名")

    # ===================================================================
    # 9. 社員削除のテスト
    # ===================================================================
    print("\n■ 9. 社員削除テスト")  # セクションタイトル
    
    # 社員が1人以上いるかチェック
    if len(company.employees) > 0:
        # 社員リストの最初の社員を取得
        # インデックス[0]で最初の要素にアクセス
        employee_to_delete = company.employees[0]
        
        # 新社長のdelete_employeeメソッドで社員を削除
        new_president.delete_employee(employee_to_delete)

    # ===================================================================
    # 10. 最終的な社員一覧
    # ===================================================================
    print("\n■ 10. 最終的な社員一覧")  # セクションタイトル
    
    # 削除後の全社員情報を表示
    company.display_all_employees()

    # テスト完了メッセージ
    print("\n" + "=" * 60)  # 区切り線
    print(" テスト完了")
    print("=" * 60)  # 区切り線


# ===================================================================
# プログラムのエントリーポイント
# ===================================================================

# このファイルが直接実行された場合のみmain()を呼び出す
# 他のファイルからimportされた場合は実行されない
if __name__ == "__main__":
    # main関数を呼び出してプログラムを開始
    main()