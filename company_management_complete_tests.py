"""
会社管理システムの完全テストスイート

このモジュールは、company_management.pyの全機能をテストします。

Test Classes:
    TestGender: Gender列挙型のテスト
    TestPost: Post列挙型のテスト
    TestHuman: Humanクラスのテスト
    TestEmployee: Employeeクラスのテスト
    TestPresident: Presidentクラスのテスト
    TestCompany: Companyクラスのテスト
    TestIntegration: 統合テスト

実行方法:
    pytest test_company_management.py -v
    pytest test_company_management.py -v --cov=company_management
"""

import pytest
from company_management import Gender, Post, Human, Employee, President, Company


# ============================================================
# テストクラス1: Gender列挙型のテスト
# ============================================================

class TestGender:
    """
    Gender列挙型のテストクラス
    
    テスト項目:
    - 各性別の値が正しいか
    - 列挙型として正しく動作するか
    """
    
    def test_gender_man_value(self):
        """
        男性の値が正しいことを確認
        """
        # Gender.MANの値を取得
        gender = Gender.MAN
        
        # 値が"男性"であることを確認
        assert gender.value == "男性"
        # gender.valueで列挙型の値を取得できる
    
    def test_gender_woman_value(self):
        """
        女性の値が正しいことを確認
        """
        # Gender.WOMANの値を取得
        gender = Gender.WOMAN
        
        # 値が"女性"であることを確認
        assert gender.value == "女性"
    
    def test_gender_other_value(self):
        """
        その他の値が正しいことを確認
        """
        # Gender.OTHERの値を取得
        gender = Gender.OTHER
        
        # 値が"その他"であることを確認
        assert gender.value == "その他"
    
    def test_gender_enum_members(self):
        """
        すべてのメンバーが存在することを確認
        """
        # Gender列挙型のすべてのメンバーを取得
        members = list(Gender)
        
        # メンバー数が3つであることを確認
        assert len(members) == 3
        
        # 各メンバーが存在することを確認
        assert Gender.MAN in members
        assert Gender.WOMAN in members
        assert Gender.OTHER in members


# ============================================================
# テストクラス2: Post列挙型のテスト
# ============================================================

class TestPost:
    """
    Post列挙型のテストクラス
    
    テスト項目:
    - 各役職の値が正しいか
    - 役職の順序が正しいか
    """
    
    def test_post_hira_value(self):
        """
        平社員の値が正しいことを確認
        """
        # Post.HIRAの値を取得
        post = Post.HIRA
        
        # 値が"ヒラ"であることを確認
        assert post.value == "ヒラ"
    
    def test_post_syunin_value(self):
        """
        主任の値が正しいことを確認
        """
        # Post.SYUNINの値を取得
        post = Post.SYUNIN
        
        # 値が"主任"であることを確認
        assert post.value == "主任"
    
    def test_post_katyo_value(self):
        """
        課長の値が正しいことを確認
        """
        # Post.KATYOの値を取得
        post = Post.KATYO
        
        # 値が"課長"であることを確認
        assert post.value == "課長"
    
    def test_post_yaruin_value(self):
        """
        役員の値が正しいことを確認
        """
        # Post.YARUINの値を取得
        post = Post.YARUIN
        
        # 値が"役員"であることを確認
        assert post.value == "役員"
    
    def test_post_order(self):
        """
        役職の順序が正しいことを確認（昇進順）
        """
        # 昇進順の役職リストを定義
        post_order = [Post.HIRA, Post.SYUNIN, Post.KATYO, Post.YARUIN]
        
        # リストの順序が正しいことを確認
        assert post_order[0] == Post.HIRA    # 1番目: 平社員
        assert post_order[1] == Post.SYUNIN  # 2番目: 主任
        assert post_order[2] == Post.KATYO   # 3番目: 課長
        assert post_order[3] == Post.YARUIN  # 4番目: 役員


# ============================================================
# テストクラス3: Humanクラスのテスト
# ============================================================

class TestHuman:
    """
    Humanクラスのテストクラス
    
    テスト項目:
    - インスタンスの作成
    - プロパティの取得
    - 自己紹介機能
    """
    
    def test_human_initialization(self):
        """
        Humanインスタンスが正しく初期化されることを確認
        """
        # Humanインスタンスを作成
        human = Human("太郎", Gender.MAN, 25)
        # 名前="太郎", 性別=男性, 年齢=25で初期化
        
        # 名前が正しく設定されているか確認
        assert human.name == "太郎"
        # human.nameでnameプロパティを取得
        
        # 性別が正しく設定されているか確認
        assert human.gender == Gender.MAN
        # human.genderでgenderプロパティを取得
        
        # 年齢が正しく設定されているか確認
        assert human.age == 25
        # human.ageでageプロパティを取得
    
    def test_human_name_property_readonly(self):
        """
        nameプロパティが読み取り専用であることを確認
        """
        # Humanインスタンスを作成
        human = Human("太郎", Gender.MAN, 25)
        
        # nameプロパティへの代入を試みる
        with pytest.raises(AttributeError):
            # プロパティは読み取り専用なので、代入するとエラー
            human.name = "花子"
            # AttributeError: can't set attribute が発生
    
    def test_human_self_introduction(self, capsys):
        """
        自己紹介が正しく表示されることを確認
        
        Args:
            capsys: pytestの標準出力キャプチャフィクスチャ
        """
        # Humanインスタンスを作成
        human = Human("太郎", Gender.MAN, 25)
        
        # 自己紹介を実行
        human.do_self_introduction()
        # 標準出力にメッセージが表示される
        
        # 標準出力をキャプチャ
        captured = capsys.readouterr()
        # capsys.readouterr()で出力を取得
        
        # 出力内容を確認
        assert "太郎" in captured.out        # 名前が含まれる
        assert "男性" in captured.out        # 性別が含まれる
        assert "25歳" in captured.out        # 年齢が含まれる


# ============================================================
# テストクラス4: Employeeクラスのテスト
# ============================================================

class TestEmployee:
    """
    Employeeクラスのテストクラス
    
    テスト項目:
    - インスタンスの作成
    - 継承の確認
    - 給与の計算
    - 昇進・降格機能
    - 社員IDの生成
    """
    
    def test_employee_initialization(self):
        """
        Employeeインスタンスが正しく初期化されることを確認
        """
        # Employeeインスタンスを作成
        employee = Employee("太郎", Gender.MAN, 25, Post.HIRA)
        # 名前="太郎", 性別=男性, 年齢=25, 役職=平社員
        
        # 基本属性の確認
        assert employee.name == "太郎"        # 名前
        assert employee.gender == Gender.MAN  # 性別
        assert employee.age == 25             # 年齢
        assert employee.post == Post.HIRA     # 役職
        
        # 社員IDが生成されているか確認
        assert employee.id is not None        # IDが存在
        assert len(employee.id) == 4          # 4桁
        assert employee.id.isdigit()          # 数字のみ
    
    def test_employee_inherits_human(self):
        """
        EmployeeがHumanを継承していることを確認
        """
        # Employeeインスタンスを作成
        employee = Employee("太郎", Gender.MAN, 25, Post.HIRA)
        
        # Humanのインスタンスであることを確認
        assert isinstance(employee, Human)
        # isinstance()で継承関係を確認
        
        # Humanのメソッドが使えることを確認
        assert hasattr(employee, 'do_self_introduction')
        # hasattr()でメソッドの存在を確認
    
    def test_employee_salary_calculation(self):
        """
        役職ごとの給与が正しく計算されることを確認
        """
        # 各役職の社員を作成
        hira = Employee("太郎", Gender.MAN, 25, Post.HIRA)
        syunin = Employee("花子", Gender.WOMAN, 30, Post.SYUNIN)
        katyo = Employee("次郎", Gender.MAN, 35, Post.KATYO)
        yaruin = Employee("四郎", Gender.MAN, 40, Post.YARUIN)
        
        # 各役職の給与を確認
        assert hira.salary == 200000      # 平社員: 200,000円
        assert syunin.salary == 300000    # 主任: 300,000円
        assert katyo.salary == 450000     # 課長: 450,000円
        assert yaruin.salary == 600000    # 役員: 600,000円
    
    def test_employee_promote(self, capsys):
        """
        昇進機能が正しく動作することを確認
        """
        # 平社員を作成
        employee = Employee("太郎", Gender.MAN, 25, Post.HIRA)
        
        # 初期状態の確認
        assert employee.post == Post.HIRA
        # 平社員からスタート
        
        # 1回目の昇進（平社員 → 主任）
        employee.promote()
        # promoteメソッドを呼び出す
        
        assert employee.post == Post.SYUNIN
        # 主任に昇進
        
        # 標準出力を確認
        captured = capsys.readouterr()
        assert "主任に昇進しました" in captured.out
        # メッセージが表示される
        
        # 2回目の昇進（主任 → 課長）
        employee.promote()
        assert employee.post == Post.KATYO
        # 課長に昇進
        
        # 3回目の昇進（課長 → 役員）
        employee.promote()
        assert employee.post == Post.YARUIN
        # 役員に昇進
        
        # 4回目の昇進（役員 → 昇進できない）
        employee.promote()
        assert employee.post == Post.YARUIN
        # 役員のまま（最高役職）
        
        captured = capsys.readouterr()
        assert "すでに最高役職です" in captured.out
        # エラーメッセージが表示される
    
    def test_employee_demote(self, capsys):
        """
        降格機能が正しく動作することを確認
        """
        # 役員を作成
        employee = Employee("太郎", Gender.MAN, 40, Post.YARUIN)
        
        # 初期状態の確認
        assert employee.post == Post.YARUIN
        # 役員からスタート
        
        # 1回目の降格（役員 → 課長）
        employee.demote()
        assert employee.post == Post.KATYO
        # 課長に降格
        
        # 標準出力を確認
        captured = capsys.readouterr()
        assert "課長に降格しました" in captured.out
        # メッセージが表示される
        
        # 2回目の降格（課長 → 主任）
        employee.demote()
        assert employee.post == Post.SYUNIN
        # 主任に降格
        
        # 3回目の降格（主任 → 平社員）
        employee.demote()
        assert employee.post == Post.HIRA
        # 平社員に降格
        
        # 4回目の降格（平社員 → 降格できない）
        employee.demote()
        assert employee.post == Post.HIRA
        # 平社員のまま（最低役職）
        
        captured = capsys.readouterr()
        assert "すでに最低役職です" in captured.out
        # エラーメッセージが表示される
    
    def test_employee_salary_changes_with_promotion(self):
        """
        昇進すると給与が変わることを確認
        """
        # 平社員を作成
        employee = Employee("太郎", Gender.MAN, 25, Post.HIRA)
        
        # 初期給与を確認
        assert employee.salary == 200000
        # 平社員の給与: 200,000円
        
        # 昇進
        employee.promote()
        
        # 給与が変わったことを確認
        assert employee.salary == 300000
        # 主任の給与: 300,000円
    
    def test_employee_id_is_unique(self):
        """
        社員IDが（おそらく）ユニークであることを確認
        """
        # 複数の社員を作成
        employees = [
            Employee(f"社員{i}", Gender.MAN, 25, Post.HIRA)
            for i in range(10)
        ]
        # 10人の社員を作成
        
        # すべての社員IDを取得
        ids = [emp.id for emp in employees]
        
        # IDがすべて異なることを確認（高確率で）
        # 注: ランダム生成なので、まれに重複する可能性あり
        assert len(set(ids)) >= 8
        # 少なくとも8個は異なるIDであることを確認


# ============================================================
# テストクラス5: Presidentクラスのテスト
# ============================================================

class TestPresident:
    """
    Presidentクラスのテストクラス
    
    テスト項目:
    - インスタンスの作成
    - 会社との関連
    - 社員管理機能
    - 辞任機能
    """
    
    def test_president_initialization(self):
        """
        Presidentインスタンスが正しく初期化されることを確認
        """
        # Presidentインスタンスを作成
        president = President("倍井 杉蔵", Gender.MAN, 88)
        # 名前="倍井 杉蔵", 性別=男性, 年齢=88
        
        # 基本属性の確認
        assert president.name == "倍井 杉蔵"  # 名前
        assert president.gender == Gender.MAN # 性別
        assert president.age == 88            # 年齢
        
        # 社長固有の属性
        assert president.salary == 1000000    # 給与: 1,000,000円
        assert president.company is None      # 初期状態では会社なし
    
    def test_president_inherits_human(self):
        """
        PresidentがHumanを継承していることを確認
        """
        # Presidentインスタンスを作成
        president = President("倍井 杉蔵", Gender.MAN, 88)
        
        # Humanのインスタンスであることを確認
        assert isinstance(president, Human)
        # isinstance()で継承関係を確認
    
    def test_president_company_property(self):
        """
        companyプロパティが正しく動作することを確認
        """
        # 社長と会社を作成
        president = President("倍井 杉蔵", Gender.MAN, 88)
        company = Company()
        
        # 初期状態ではNone
        assert president.company is None
        
        # 会社を設定
        president.company = company
        # companyプロパティのsetterを使用
        
        # 会社が設定されたことを確認
        assert president.company is not None
        assert president.company == company
        # 同じCompanyオブジェクト
    
    def test_president_add_employee(self, capsys):
        """
        社長が社員を追加できることを確認
        """
        # 社長と会社を作成
        president = President("倍井 杉蔵", Gender.MAN, 88)
        company = Company()
        president.company = company
        
        # 社員を追加
        president.add_employee("太郎", Gender.MAN, 25, Post.HIRA)
        # add_employeeメソッドを呼び出す
        
        # 社員が追加されたことを確認
        assert company.current_number == 1
        # 社員数が1人
        
        # 標準出力を確認
        captured = capsys.readouterr()
        assert "太郎さん" in captured.out
        assert "採用しました" in captured.out
    
    def test_president_add_employee_without_company(self, capsys):
        """
        会社が設定されていない場合のエラー処理を確認
        """
        # 社長を作成（会社なし）
        president = President("倍井 杉蔵", Gender.MAN, 88)
        
        # 社員を追加しようとする
        president.add_employee("太郎", Gender.MAN, 25, Post.HIRA)
        
        # エラーメッセージが表示される
        captured = capsys.readouterr()
        assert "会社が設定されていません" in captured.out
    
    def test_president_get_personnel_by_name(self):
        """
        名前で社員を検索できることを確認
        """
        # 社長、会社、社員を準備
        president = President("倍井 杉蔵", Gender.MAN, 88)
        company = Company()
        president.company = company
        
        # 社員を追加
        president.add_employee("太郎", Gender.MAN, 25, Post.HIRA)
        president.add_employee("花子", Gender.WOMAN, 30, Post.SYUNIN)
        
        # 名前で検索
        found = president.get_personnel_by_name("太郎")
        # get_personnel_by_nameメソッドを呼び出す
        
        # 検索結果を確認
        assert found is not None        # 見つかった
        assert found.name == "太郎"     # 名前が一致
        assert found.post == Post.HIRA  # 役職も確認
        
        # 存在しない名前で検索
        not_found = president.get_personnel_by_name("存在しない人")
        assert not_found is None        # 見つからない
    
    def test_president_get_personnel_by_id(self):
        """
        IDで社員を検索できることを確認
        """
        # 社長、会社、社員を準備
        president = President("倍井 杉蔵", Gender.MAN, 88)
        company = Company()
        president.company = company
        
        # 社員を追加
        president.add_employee("太郎", Gender.MAN, 25, Post.HIRA)
        
        # 追加した社員を取得
        employee = company.employees[0]
        employee_id = employee.id
        # 社員IDを取得
        
        # IDで検索
        found = president.get_personnel_by_id(employee_id)
        # get_personnel_by_idメソッドを呼び出す
        
        # 検索結果を確認
        assert found is not None         # 見つかった
        assert found.id == employee_id   # IDが一致
        assert found.name == "太郎"      # 名前も確認
    
    def test_president_delete_employee(self, capsys):
        """
        社長が社員を削除できることを確認
        """
        # 社長、会社、社員を準備
        president = President("倍井 杉蔵", Gender.MAN, 88)
        company = Company()
        president.company = company
        
        # 社員を追加
        president.add_employee("太郎", Gender.MAN, 25, Post.HIRA)
        
        # 初期状態の確認
        assert company.current_number == 1
        # 社員数が1人
        
        # 社員を取得
        employee = company.employees[0]
        
        # 社員を削除
        president.delete_employee(employee)
        # delete_employeeメソッドを呼び出す
        
        # 削除されたことを確認
        assert company.current_number == 0
        # 社員数が0人
        
        # 標準出力を確認
        captured = capsys.readouterr()
        assert "削除しました" in captured.out
    
    def test_president_resignation_success(self, capsys):
        """
        社長が正常に辞任できることを確認
        """
        # 社長と会社を作成
        president = President("倍井 杉蔵", Gender.MAN, 88)
        company = Company()
        president.company = company
        
        # 社員を追加（次期社長候補）
        president.add_employee("太郎", Gender.MAN, 40, Post.YARUIN)
        president.add_employee("花子", Gender.WOMAN, 30, Post.HIRA)
        
        # 初期状態の確認
        assert company.current_number == 2
        # 社員数が2人
        
        # 辞任
        new_president = president.resignation()
        # resignationメソッドを呼び出す
        
        # 新社長が選出されたことを確認
        assert new_president is not None
        # 新社長が存在
        
        assert isinstance(new_president, President)
        # Presidentクラスのインスタンス
        
        assert new_president.name == "太郎"
        # 役員が社長になった
        
        # 社員数が減ったことを確認
        assert company.current_number == 1
        # 太郎が社長になったので、社員は花子だけ
        
        # 標準出力を確認
        captured = capsys.readouterr()
        assert "辞任はだいた" in captured.out
    
    def test_president_resignation_no_employees(self, capsys):
        """
        社員がいない場合は辞任できないことを確認
        """
        # 社長と会社を作成（社員なし）
        president = President("倍井 杉蔵", Gender.MAN, 88)
        company = Company()
        president.company = company
        
        # 辞任しようとする
        new_president = president.resignation()
        
        # 辞任できないことを確認
        assert new_president is None
        # 新社長はNone
        
        # エラーメッセージを確認
        captured = capsys.readouterr()
        assert "存在しません" in captured.out
    
    def test_company_get_personnel_by_name(self):
        """
        名前で社員を検索できることを確認
        """
        # Companyインスタンスを作成
        company = Company()
        
        # 社員を追加
        company.add_employee("太郎", Gender.MAN, 25, Post.HIRA)
        company.add_employee("花子", Gender.WOMAN, 30, Post.SYUNIN)
        company.add_employee("次郎", Gender.MAN, 35, Post.KATYO)
        
        # 名前で検索
        found = company.get_personnel_by_name("花子")
        # get_personnel_by_nameメソッドを呼び出す
        
        # 検索結果を確認
        assert found is not None           # 見つかった
        assert found.name == "花子"        # 名前が一致
        assert found.gender == Gender.WOMAN # 性別も確認
        assert found.post == Post.SYUNIN   # 役職も確認
        
        # 存在しない名前で検索
        not_found = company.get_personnel_by_name("存在しない人")
        assert not_found is None           # 見つからない
    
    def test_company_get_personnel_by_id(self):
        """
        IDで社員を検索できることを確認
        """
        # Companyインスタンスを作成
        company = Company()
        
        # 社員を追加
        company.add_employee("太郎", Gender.MAN, 25, Post.HIRA)
        
        # 追加した社員のIDを取得
        employee = company.employees[0]
        employee_id = employee.id
        
        # IDで検索
        found = company.get_personnel_by_id(employee_id)
        # get_personnel_by_idメソッドを呼び出す
        
        # 検索結果を確認
        assert found is not None          # 見つかった
        assert found.id == employee_id    # IDが一致
        assert found.name == "太郎"       # 名前も確認
        
        # 存在しないIDで検索
        not_found = company.get_personnel_by_id("9999")
        assert not_found is None          # 見つからない
    
    def test_company_select_president_with_executives(self):
        """
        役員がいる場合、最年長の役員が選出されることを確認
        """
        # Companyインスタンスを作成
        company = Company()
        
        # 役員を複数追加
        company.add_employee("太郎", Gender.MAN, 40, Post.YARUIN)
        company.add_employee("花子", Gender.WOMAN, 50, Post.YARUIN)  # 最年長
        company.add_employee("次郎", Gender.MAN, 30, Post.HIRA)
        
        # 次期社長を選出
        next_president = company.select_president()
        # select_presidentメソッドを呼び出す
        
        # 最年長の役員が選ばれることを確認
        assert next_president is not None
        assert next_president.name == "花子"  # 50歳の役員
        assert next_president.age == 50
        assert next_president.post == Post.YARUIN
    
    def test_company_select_president_without_executives(self):
        """
        役員がいない場合、最年長の社員が選出されることを確認
        """
        # Companyインスタンスを作成
        company = Company()
        
        # 役員以外の社員を追加
        company.add_employee("太郎", Gender.MAN, 40, Post.HIRA)
        company.add_employee("花子", Gender.WOMAN, 35, Post.SYUNIN)
        company.add_employee("次郎", Gender.MAN, 50, Post.KATYO)  # 最年長
        
        # 次期社長を選出
        next_president = company.select_president()
        # select_presidentメソッドを呼び出す
        
        # 最年長の社員が選ばれることを確認
        assert next_president is not None
        assert next_president.name == "次郎"  # 50歳の課長
        assert next_president.age == 50
        assert next_president.post == Post.KATYO
    
    def test_company_select_president_no_employees(self):
        """
        社員がいない場合、Noneが返されることを確認
        """
        # Companyインスタンスを作成（社員なし）
        company = Company()
        
        # 次期社長を選出しようとする
        next_president = company.select_president()
        
        # Noneが返されることを確認
        assert next_president is None
    
    def test_company_display_all_employees_with_employees(self, capsys):
        """
        社員一覧が正しく表示されることを確認
        """
        # Companyインスタンスを作成
        company = Company()
        
        # 社員を追加
        company.add_employee("太郎", Gender.MAN, 25, Post.HIRA)
        company.add_employee("花子", Gender.WOMAN, 30, Post.SYUNIN)
        
        # 標準出力をクリア
        capsys.readouterr()
        
        # 社員一覧を表示
        company.display_all_employees()
        # display_all_employeesメソッドを呼び出す
        
        # 標準出力を確認
        captured = capsys.readouterr()
        
        # 表示内容を確認
        assert "社員一覧" in captured.out      # タイトル
        assert "太郎" in captured.out          # 社員1の名前
        assert "花子" in captured.out          # 社員2の名前
        assert "合計: 2名" in captured.out     # 合計人数
    
    def test_company_display_all_employees_no_employees(self, capsys):
        """
        社員がいない場合のメッセージが表示されることを確認
        """
        # Companyインスタンスを作成（社員なし）
        company = Company()
        
        # 社員一覧を表示
        company.display_all_employees()
        
        # 標準出力を確認
        captured = capsys.readouterr()
        assert "社員がいません" in captured.out
    
    def test_company_current_number_property(self):
        """
        current_numberプロパティが正しく動作することを確認
        """
        # Companyインスタンスを作成
        company = Company()
        
        # 初期状態
        assert company.current_number == 0
        
        # 社員を追加
        company.add_employee("太郎", Gender.MAN, 25, Post.HIRA)
        assert company.current_number == 1
        
        # さらに追加
        company.add_employee("花子", Gender.WOMAN, 30, Post.SYUNIN)
        assert company.current_number == 2
        
        # 削除
        employee = company.employees[0]
        company.delete_employee(employee)
        assert company.current_number == 1
    
    def test_company_number_of_employee_property(self):
        """
        number_of_employeeプロパティが正しく動作することを確認
        """
        # Companyインスタンスを作成
        company = Company()
        
        # 初期状態
        assert company.number_of_employee == 0
        
        # 社員を追加
        company.add_employee("太郎", Gender.MAN, 25, Post.HIRA)
        assert company.number_of_employee == 1
        
        # current_numberと同じ値を返すことを確認
        assert company.number_of_employee == company.current_number


# ============================================================
# テストクラス7: 統合テスト
# ============================================================

class TestIntegration:
    """
    統合テストクラス
    
    複数のクラスを組み合わせた実際の使用シナリオをテスト
    """
    
    def test_complete_workflow(self, capsys):
        """
        完全なワークフローをテスト
        
        シナリオ:
        1. 社長と会社を作成
        2. 社員を追加
        3. 社員を検索
        4. 社員を昇進
        5. 次期社長を選出
        6. 社長が辞任
        """
        # ステップ1: 社長と会社を作成
        president = President("倍井 杉蔵", Gender.MAN, 88)
        company = Company()
        president.company = company
        
        # 会社が設定されたことを確認
        assert president.company is not None
        assert company.current_number == 0
        
        # ステップ2: 社員を追加
        president.add_employee("太郎", Gender.MAN, 30, Post.HIRA)
        president.add_employee("花子", Gender.WOMAN, 40, Post.YARUIN)
        president.add_employee("次郎", Gender.MAN, 35, Post.SYUNIN)
        
        # 社員が追加されたことを確認
        assert company.current_number == 3
        
        # ステップ3: 社員を検索
        found_employee = president.get_personnel_by_name("太郎")
        
        # 検索結果を確認
        assert found_employee is not None
        assert found_employee.name == "太郎"
        assert found_employee.post == Post.HIRA
        
        # ステップ4: 社員を昇進
        initial_salary = found_employee.salary  # 初期給与を記録
        found_employee.promote()
        
        # 昇進したことを確認
        assert found_employee.post == Post.SYUNIN
        assert found_employee.salary > initial_salary  # 給与が増えた
        
        # ステップ5: 次期社長を選出
        next_president_candidate = company.select_president()
        
        # 役員の花子が選ばれることを確認
        assert next_president_candidate is not None
        assert next_president_candidate.name == "花子"
        
        # ステップ6: 社長が辞任
        new_president = president.resignation()
        
        # 新社長が就任したことを確認
        assert new_president is not None
        assert new_president.name == "花子"
        assert isinstance(new_president, President)
        
        # 花子は社員リストから削除されている
        assert company.current_number == 2  # 太郎と次郎のみ
        
        # 花子は社員リストにいない
        employee_names = [emp.name for emp in company.employees]
        assert "花子" not in employee_names
    
    def test_salary_map_shared_across_employees(self):
        """
        給与マップがすべての社員で共有されていることを確認
        （クラス変数のテスト）
        """
        # 複数の社員を作成
        employee1 = Employee("太郎", Gender.MAN, 25, Post.HIRA)
        employee2 = Employee("花子", Gender.WOMAN, 30, Post.HIRA)
        
        # 同じ役職なので同じ給与
        assert employee1.salary == employee2.salary
        assert employee1.salary == 200000
        
        # クラス変数であることを確認
        assert employee1._salary_map is employee2._salary_map
        # 同じオブジェクト（クラス変数）を参照している
    
    def test_multiple_companies_independent(self):
        """
        複数の会社が独立していることを確認
        （インスタンス変数のテスト）
        """
        # 2つの会社を作成
        company1 = Company()
        company2 = Company()
        
        # 会社1に社員を追加
        company1.add_employee("太郎", Gender.MAN, 25, Post.HIRA)
        
        # 会社2に社員を追加
        company2.add_employee("花子", Gender.WOMAN, 30, Post.SYUNIN)
        
        # 各会社の社員数を確認
        assert company1.current_number == 1
        assert company2.current_number == 1
        
        # 各会社の社員リストは独立している
        assert company1.employees[0].name == "太郎"
        assert company2.employees[0].name == "花子"
        
        # 社員リストは異なるオブジェクト
        assert company1.employees is not company2.employees
    
    def test_max_number_of_people_is_class_variable(self):
        """
        MAX_NUMBER_OF_PEOPLEがクラス変数であることを確認
        """
        # 2つの会社を作成
        company1 = Company()
        company2 = Company()
        
        # 両方とも同じ最大人数
        assert company1.MAX_NUMBER_OF_PEOPLE == 10
        assert company2.MAX_NUMBER_OF_PEOPLE == 10
        
        # クラス変数であることを確認
        assert Company.MAX_NUMBER_OF_PEOPLE == 10
        
        # クラス変数を変更すると、すべてのインスタンスに影響する
        # （実運用では推奨されないが、テストとして確認）
        original_max = Company.MAX_NUMBER_OF_PEOPLE
        Company.MAX_NUMBER_OF_PEOPLE = 5
        
        assert company1.MAX_NUMBER_OF_PEOPLE == 5
        assert company2.MAX_NUMBER_OF_PEOPLE == 5
        
        # 元に戻す
        Company.MAX_NUMBER_OF_PEOPLE = original_max
    
    def test_employee_promotion_and_salary_change(self):
        """
        昇進に伴う給与変更の完全なフローをテスト
        """
        # 平社員を作成
        employee = Employee("太郎", Gender.MAN, 25, Post.HIRA)
        
        # 各段階での給与を記録
        salaries = [employee.salary]  # 初期給与
        
        # 主任に昇進
        employee.promote()
        salaries.append(employee.salary)
        
        # 課長に昇進
        employee.promote()
        salaries.append(employee.salary)
        
        # 役員に昇進
        employee.promote()
        salaries.append(employee.salary)
        
        # 給与が昇順であることを確認
        assert salaries == [200000, 300000, 450000, 600000]
        
        # 給与が常に増加していることを確認
        for i in range(len(salaries) - 1):
            assert salaries[i] < salaries[i + 1]


# ============================================================
# テストクラス8: エッジケースとエラーハンドリング
# ============================================================

class TestEdgeCases:
    """
    エッジケースとエラーハンドリングのテスト
    
    テスト項目:
    - 境界値テスト
    - 異常系のテスト
    - 例外処理のテスト
    """
    
    def test_employee_with_empty_name(self):
        """
        空の名前で社員を作成（現在は許可されている）
        """
        # 空の名前で社員を作成
        employee = Employee("", Gender.MAN, 25, Post.HIRA)
        
        # 作成できることを確認
        assert employee.name == ""
        # 注: 実運用ではバリデーションが必要
    
    def test_employee_with_zero_age(self):
        """
        年齢0で社員を作成（現在は許可されている）
        """
        # 年齢0で社員を作成
        employee = Employee("太郎", Gender.MAN, 0, Post.HIRA)
        
        # 作成できることを確認
        assert employee.age == 0
        # 注: 実運用ではバリデーションが必要
    
    def test_company_add_exactly_max_employees(self):
        """
        ちょうど最大人数まで社員を追加できることを確認
        """
        # Companyインスタンスを作成
        company = Company()
        
        # 最大人数（10人）まで追加
        for i in range(Company.MAX_NUMBER_OF_PEOPLE):
            company.add_employee(f"社員{i}", Gender.MAN, 25, Post.HIRA)
        
        # ちょうど10人追加できることを確認
        assert company.current_number == Company.MAX_NUMBER_OF_PEOPLE
    
    def test_president_resignation_with_one_employee(self):
        """
        社員が1人だけの場合の辞任をテスト
        """
        # 社長と会社を作成
        president = President("倍井 杉蔵", Gender.MAN, 88)
        company = Company()
        president.company = company
        
        # 社員を1人だけ追加
        president.add_employee("太郎", Gender.MAN, 40, Post.HIRA)
        
        # 辞任
        new_president = president.resignation()
        
        # 唯一の社員が社長になる
        assert new_president is not None
        assert new_president.name == "太郎"
        
        # 社員は0人になる
        assert company.current_number == 0
    
    def test_search_in_empty_company(self):
        """
        空の会社で検索した場合の動作を確認
        """
        # 空の会社を作成
        company = Company()
        
        # 名前で検索
        found_by_name = company.get_personnel_by_name("太郎")
        assert found_by_name is None
        
        # IDで検索
        found_by_id = company.get_personnel_by_id("1234")
        assert found_by_id is None
    
    def test_delete_same_employee_twice(self, capsys):
        """
        同じ社員を2回削除しようとした場合の動作を確認
        """
        # Companyインスタンスを作成
        company = Company()
        
        # 社員を追加
        company.add_employee("太郎", Gender.MAN, 25, Post.HIRA)
        employee = company.employees[0]
        
        # 1回目の削除
        company.delete_employee(employee)
        assert company.current_number == 0
        
        # 標準出力をクリア
        capsys.readouterr()
        
        # 2回目の削除（すでにリストにいない）
        company.delete_employee(employee)
        
        # エラーメッセージが表示される
        captured = capsys.readouterr()
        assert "存在しません" in captured.out


# ============================================================
# テストクラス9: プロパティのテスト
# ============================================================

class TestProperties:
    """
    プロパティの動作をテストするクラス
    """
    
    def test_human_properties_are_readonly(self):
        """
        Humanの各プロパティが読み取り専用であることを確認
        """
        # Humanインスタンスを作成
        human = Human("太郎", Gender.MAN, 25)
        
        # nameプロパティが読み取り専用
        with pytest.raises(AttributeError):
            human.name = "花子"
        
        # genderプロパティが読み取り専用
        with pytest.raises(AttributeError):
            human.gender = Gender.WOMAN
        
        # ageプロパティが読み取り専用
        with pytest.raises(AttributeError):
            human.age = 30
    
    def test_employee_properties_are_readonly(self):
        """
        Employeeの各プロパティが読み取り専用であることを確認
        """
        # Employeeインスタンスを作成
        employee = Employee("太郎", Gender.MAN, 25, Post.HIRA)
        
        # postプロパティが読み取り専用
        with pytest.raises(AttributeError):
            employee.post = Post.SYUNIN
        
        # salaryプロパティが読み取り専用
        with pytest.raises(AttributeError):
            employee.salary = 500000
        
        # idプロパティが読み取り専用
        with pytest.raises(AttributeError):
            employee.id = "9999"
    
    def test_president_company_property_can_be_set(self):
        """
        Presidentのcompanyプロパティはsetterがあることを確認
        """
        # Presidentインスタンスを作成
        president = President("倍井 杉蔵", Gender.MAN, 88)
        
        # 初期状態ではNone
        assert president.company is None
        
        # 設定できる（setterがある）
        company = Company()
        president.company = company
        
        # 設定されたことを確認
        assert president.company is company


# ============================================================
# フィクスチャ（共通のテストデータ）
# ============================================================

@pytest.fixture
def sample_company():
    """
    テスト用の会社を作成するフィクスチャ
    
    Returns:
        Company: 社員が3人いる会社
    """
    # 会社を作成
    company = Company()
    
    # 社員を追加
    company.add_employee("太郎", Gender.MAN, 25, Post.HIRA)
    company.add_employee("花子", Gender.WOMAN, 30, Post.SYUNIN)
    company.add_employee("次郎", Gender.MAN, 35, Post.KATYO)
    
    # 会社を返す
    return company


@pytest.fixture
def sample_president_with_company():
    """
    テスト用の社長と会社を作成するフィクスチャ
    
    Returns:
        tuple: (President, Company)のタプル
    """
    # 社長を作成
    president = President("倍井 杉蔵", Gender.MAN, 88)
    
    # 会社を作成
    company = Company()
    
    # 社長に会社を設定
    president.company = company
    
    # タプルで返す
    return president, company


# ============================================================
# フィクスチャを使ったテスト
# ============================================================

class TestWithFixtures:
    """
    フィクスチャを使ったテストクラス
    """
    
    def test_with_sample_company(self, sample_company):
        """
        sample_companyフィクスチャを使ったテスト
        
        Args:
            sample_company: テスト用の会社（フィクスチャ）
        """
        # フィクスチャから会社を取得
        company = sample_company
        
        # 社員が3人いることを確認
        assert company.current_number == 3
        
        # 各社員の存在を確認
        names = [emp.name for emp in company.employees]
        assert "太郎" in names
        assert "花子" in names
        assert "次郎" in names
    
    def test_with_president_and_company(self, sample_president_with_company):
        """
        sample_president_with_companyフィクスチャを使ったテスト
        
        Args:
            sample_president_with_company: 社長と会社のタプル（フィクスチャ）
        """
        # フィクスチャから社長と会社を取得
        president, company = sample_president_with_company
        
        # 社長が会社に所属していることを確認
        assert president.company is company
        
        # 社長が社員を追加できることを確認
        president.add_employee("四郎", Gender.MAN, 40, Post.YARUIN)
        assert company.current_number == 1


# ============================================================
# パラメータ化テスト
# ============================================================

class TestParametrized:
    """
    パラメータ化テストのクラス
    """
    
    @pytest.mark.parametrize("name, gender, age, post", [
        ("太郎", Gender.MAN, 25, Post.HIRA),
        ("花子", Gender.WOMAN, 30, Post.SYUNIN),
        ("次郎", Gender.MAN, 35, Post.KATYO),
        ("四郎", Gender.OTHER, 40, Post.YARUIN),
    ])
    def test_employee_creation_with_various_data(self, name, gender, age, post):
        """
        さまざまなデータで社員を作成できることを確認
        
        Args:
            name: 名前
            gender: 性別
            age: 年齢
            post: 役職
        """
        # 社員を作成
        employee = Employee(name, gender, age, post)
        
        # 各属性が正しく設定されていることを確認
        assert employee.name == name
        assert employee.gender == gender
        assert employee.age == age
        assert employee.post == post
    
    @pytest.mark.parametrize("post, expected_salary", [
        (Post.HIRA, 200000),
        (Post.SYUNIN, 300000),
        (Post.KATYO, 450000),
        (Post.YARUIN, 600000),
    ])
    def test_salary_for_each_post(self, post, expected_salary):
        """
        各役職の給与が正しいことを確認
        
        Args:
            post: 役職
            expected_salary: 期待される給与
        """
        # 指定された役職で社員を作成
        employee = Employee("テスト", Gender.MAN, 30, post)
        
        # 給与が正しいことを確認
        assert employee.salary == expected_salary


# ============================================================
# 実行コマンド例
# ============================================================

"""
【基本的な実行】
pytest test_company_management.py

【詳細表示】
pytest test_company_management.py -v

【カバレッジ測定】
pytest test_company_management.py --cov=company_management --cov-report=html

【特定のテストクラスだけ実行】
pytest test_company_management.py::TestEmployee -v

【特定のテストメソッドだけ実行】
pytest test_company_management.py::TestEmployee::test_employee_promote -v

【失敗したテストだけ再実行】
pytest test_company_management.py --lf

【並列実行（pytest-xdistが必要）】
pytest test_company_management.py -n auto

【マーカーで絞り込み】
pytest test_company_management.py -m "not slow"
"""r()
        assert "辞任しないでください" in captured.out


# ============================================================
# テストクラス6: Companyクラスのテスト
# ============================================================

class TestCompany:
    """
    Companyクラスのテストクラス
    
    テスト項目:
    - インスタンスの作成
    - 社員の追加・削除
    - 社員の検索
    - 次期社長の選出
    """
    
    def test_company_initialization(self):
        """
        Companyインスタンスが正しく初期化されることを確認
        """
        # Companyインスタンスを作成
        company = Company()
        
        # 初期状態の確認
        assert company.current_number == 0
        # 社員数が0人
        
        assert len(company.employees) == 0
        # 社員リストが空
        
        assert Company.MAX_NUMBER_OF_PEOPLE == 10
        # 最大社員数が10人（クラス変数）
    
    def test_company_add_employee(self, capsys):
        """
        社員を追加できることを確認
        """
        # Companyインスタンスを作成
        company = Company()
        
        # 社員を追加
        company.add_employee("太郎", Gender.MAN, 25, Post.HIRA)
        # add_employeeメソッドを呼び出す
        
        # 社員が追加されたことを確認
        assert company.current_number == 1
        # 社員数が1人
        
        assert len(company.employees) == 1
        # 社員リストに1人
        
        # 追加された社員を確認
        employee = company.employees[0]
        assert employee.name == "太郎"
        assert employee.post == Post.HIRA
        
        # 標準出力を確認
        captured = capsys.readouterr()
        assert "採用しました" in captured.out
    
    def test_company_add_employee_max_limit(self, capsys):
        """
        最大社員数に達すると追加できないことを確認
        """
        # Companyインスタンスを作成
        company = Company()
        
        # 最大人数まで社員を追加
        for i in range(Company.MAX_NUMBER_OF_PEOPLE):
            company.add_employee(f"社員{i}", Gender.MAN, 25, Post.HIRA)
        # MAX_NUMBER_OF_PEOPLE = 10なので、10人追加
        
        # 社員数を確認
        assert company.current_number == 10
        # 10人追加された
        
        # 11人目を追加しようとする
        company.add_employee("11人目", Gender.MAN, 25, Post.HIRA)
        
        # 追加されないことを確認
        assert company.current_number == 10
        # 社員数は10人のまま
        
        # エラーメッセージを確認
        captured = capsys.readouterr()
        assert "上限" in captured.out
        assert "達しています" in captured.out
    
    def test_company_delete_employee(self, capsys):
        """
        社員を削除できることを確認
        """
        # Companyインスタンスを作成
        company = Company()
        
        # 社員を追加
        company.add_employee("太郎", Gender.MAN, 25, Post.HIRA)
        company.add_employee("花子", Gender.WOMAN, 30, Post.SYUNIN)
        
        # 初期状態の確認
        assert company.current_number == 2
        # 社員数が2人
        
        # 1人目を削除
        employee_to_delete = company.employees[0]
        company.delete_employee(employee_to_delete)
        # delete_employeeメソッドを呼び出す
        
        # 削除されたことを確認
        assert company.current_number == 1
        # 社員数が1人
        
        assert employee_to_delete not in company.employees
        # 削除された社員はリストにいない
        
        # 標準出力を確認
        captured = capsys.readouterr()
        assert "削除しました" in captured.out
    
    def test_company_delete_nonexistent_employee(self, capsys):
        """
        存在しない社員を削除しようとした場合のエラー処理を確認
        """
        # Companyインスタンスを作成
        company = Company()
        
        # 別の会社の社員を作成
        other_employee = Employee("太郎", Gender.MAN, 25, Post.HIRA)
        
        # 削除しようとする
        company.delete_employee(other_employee)
        
        # エラーメッセージを確認
        captured = capsys.readouter