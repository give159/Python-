"""
実務で使えるロギングデコレーター集

このモジュールをインポートして、関数に @log_call を付けるだけで
ロギング機能を追加できます。

使い方:
    from logging_decorators import log_call, log_time, log_errors
    
    @log_call
    def my_function():
        pass

作成者: 2025
"""

import logging
import time
import functools
from datetime import datetime
from typing import Any, Callable
import traceback
import json


# ===================================================================
# ロガーの基本設定
# ===================================================================

# モジュールレベルのロガーを作成
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# コンソールハンドラーの設定
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# フォーマッターの設定
formatter = logging.Formatter(
    '[%(asctime)s] %(levelname)-8s [%(name)s:%(funcName)s:%(lineno)d] %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
console_handler.setFormatter(formatter)

# ハンドラーをロガーに追加（重複防止）
if not logger.handlers:
    logger.addHandler(console_handler)


# ===================================================================
# デコレーター1: 関数呼び出しをログ出力
# ===================================================================

def log_call(func: Callable) -> Callable:
    """
    関数の呼び出しをログに記録するデコレーター
    
    機能:
    - 関数の開始をログ出力
    - 引数の値をログ出力
    - 戻り値をログ出力
    
    使用例:
        @log_call
        def add(a, b):
            return a + b
        
        result = add(3, 5)  # ログが自動で出力される
    
    Args:
        func: デコレートする関数
    
    Returns:
        ラップされた関数
    """
    @functools.wraps(func)  # 元の関数の情報を保持
    def wrapper(*args, **kwargs):
        # 関数名を取得
        func_name = func.__name__
        
        # 引数をフォーマット
        args_repr = [repr(a) for a in args]  # 位置引数
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]  # キーワード引数
        signature = ", ".join(args_repr + kwargs_repr)
        
        # 関数開始のログ
        logger.info(f"→ 呼び出し: {func_name}({signature})")
        
        # 実際の関数を実行
        result = func(*args, **kwargs)
        
        # 関数終了のログ（戻り値付き）
        logger.info(f"← 完了: {func_name}() → {result!r}")
        
        return result
    
    return wrapper


# ===================================================================
# デコレーター2: 実行時間を計測
# ===================================================================

def log_time(func: Callable) -> Callable:
    """
    関数の実行時間を計測してログに記録するデコレーター
    
    機能:
    - 関数の実行時間を自動計測
    - ミリ秒単位で表示
    - 遅い関数を簡単に特定できる
    
    使用例:
        @log_time
        def slow_function():
            time.sleep(1)
        
        slow_function()  # "実行時間: 1000.5ms" とログ出力
    
    Args:
        func: デコレートする関数
    
    Returns:
        ラップされた関数
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        
        # 開始時刻を記録
        start_time = time.time()
        
        # 実際の関数を実行
        result = func(*args, **kwargs)
        
        # 終了時刻を記録
        end_time = time.time()
        
        # 実行時間を計算（ミリ秒）
        elapsed_time = (end_time - start_time) * 1000
        
        # ログ出力
        logger.info(f"⏱ {func_name}() の実行時間: {elapsed_time:.2f}ms")
        
        return result
    
    return wrapper


# ===================================================================
# デコレーター3: エラーをキャッチしてログ出力
# ===================================================================

def log_errors(func: Callable) -> Callable:
    """
    関数内のエラーをキャッチしてログに記録するデコレーター
    
    機能:
    - 例外が発生したらログに記録
    - スタックトレースも出力
    - 例外は再送出（上位で処理可能）
    
    使用例:
        @log_errors
        def risky_function():
            return 10 / 0  # エラーが自動でログに記録される
    
    Args:
        func: デコレートする関数
    
    Returns:
        ラップされた関数
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        
        try:
            # 実際の関数を実行
            return func(*args, **kwargs)
        
        except Exception as e:
            # エラー情報をログ出力
            logger.error(f"❌ {func_name}() でエラー発生: {type(e).__name__}: {e}")
            
            # スタックトレースをログ出力
            logger.error(f"スタックトレース:\n{traceback.format_exc()}")
            
            # 例外を再送出（上位で処理できるように）
            raise
    
    return wrapper


# ===================================================================
# デコレーター4: 実行回数をカウント
# ===================================================================

def count_calls(func: Callable) -> Callable:
    """
    関数の呼び出し回数をカウントするデコレーター
    
    機能:
    - 関数が何回呼ばれたかカウント
    - 関数オブジェクトに .call_count 属性を追加
    
    使用例:
        @count_calls
        def my_function():
            pass
        
        my_function()
        my_function()
        print(my_function.call_count)  # 2
    
    Args:
        func: デコレートする関数
    
    Returns:
        ラップされた関数
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        # 呼び出し回数をカウント
        wrapper.call_count += 1
        
        func_name = func.__name__
        logger.debug(f"📊 {func_name}() 呼び出し回数: {wrapper.call_count}回")
        
        # 実際の関数を実行
        return func(*args, **kwargs)
    
    # call_count 属性を初期化
    wrapper.call_count = 0
    
    return wrapper


# ===================================================================
# デコレーター5: 引数と戻り値を詳細にログ出力
# ===================================================================

def log_detailed(func: Callable) -> Callable:
    """
    引数と戻り値を詳細にログ出力するデコレーター
    
    機能:
    - 引数の型と値を詳細に表示
    - 戻り値の型と値を詳細に表示
    - デバッグ時に便利
    
    使用例:
        @log_detailed
        def calculate(x, y):
            return x + y
    
    Args:
        func: デコレートする関数
    
    Returns:
        ラップされた関数
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        func_name = func.__name__
        
        # 引数の詳細情報を作成
        logger.debug(f"{'='*60}")
        logger.debug(f"関数: {func_name}()")
        logger.debug(f"{'='*60}")
        
        # 位置引数の詳細
        if args:
            logger.debug("位置引数:")
            for i, arg in enumerate(args):
                logger.debug(f"  [{i}] {type(arg).__name__}: {arg!r}")
        
        # キーワード引数の詳細
        if kwargs:
            logger.debug("キーワード引数:")
            for key, value in kwargs.items():
                logger.debug(f"  {key}: {type(value).__name__} = {value!r}")
        
        # 実際の関数を実行
        result = func(*args, **kwargs)
        
        # 戻り値の詳細
        logger.debug(f"戻り値: {type(result).__name__} = {result!r}")
        logger.debug(f"{'='*60}")
        
        return result
    
    return wrapper


# ===================================================================
# デコレーター6: リトライ機能（失敗時に再実行）
# ===================================================================

def retry(max_attempts: int = 3, delay: float = 1.0):
    """
    失敗時に自動でリトライするデコレーター（パラメータ付き）
    
    機能:
    - 指定回数まで自動で再実行
    - 各試行の間に待機時間を設定
    - 失敗の履歴をログに記録
    
    使用例:
        @retry(max_attempts=3, delay=1.0)
        def unstable_api_call():
            # 不安定なAPI呼び出し
            pass
    
    Args:
        max_attempts: 最大試行回数
        delay: 試行間の待機時間（秒）
    
    Returns:
        デコレーター関数
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            
            # 指定回数まで試行
            for attempt in range(1, max_attempts + 1):
                try:
                    logger.info(f"🔄 {func_name}() 試行 {attempt}/{max_attempts}")
                    
                    # 実際の関数を実行
                    result = func(*args, **kwargs)
                    
                    # 成功したらログを出して返す
                    if attempt > 1:
                        logger.info(f"✅ {func_name}() 成功（{attempt}回目で成功）")
                    
                    return result
                
                except Exception as e:
                    # 最後の試行でもない場合
                    if attempt < max_attempts:
                        logger.warning(
                            f"⚠️ {func_name}() 失敗（{attempt}/{max_attempts}）: "
                            f"{type(e).__name__}: {e}"
                        )
                        logger.info(f"⏳ {delay}秒待機後に再試行...")
                        time.sleep(delay)
                    else:
                        # 最後の試行も失敗
                        logger.error(
                            f"❌ {func_name}() 全ての試行が失敗しました "
                            f"（{max_attempts}回試行）"
                        )
                        raise
        
        return wrapper
    
    return decorator


# ===================================================================
# デコレーター7: 実行結果をキャッシュ（メモ化）
# ===================================================================

def cache_result(func: Callable) -> Callable:
    """
    関数の実行結果をキャッシュするデコレーター
    
    機能:
    - 同じ引数での呼び出しは結果を再利用
    - 計算時間を大幅に短縮
    - キャッシュのヒット率をログ出力
    
    注意:
    - 引数がハッシュ可能である必要がある
    - 副作用のある関数には使用不可
    
    使用例:
        @cache_result
        def expensive_calculation(n):
            time.sleep(1)  # 重い処理
            return n * n
        
        expensive_calculation(5)  # 1秒かかる
        expensive_calculation(5)  # 即座に返る（キャッシュ）
    
    Args:
        func: デコレートする関数
    
    Returns:
        ラップされた関数
    """
    # キャッシュ用の辞書
    cache = {}
    cache_hits = 0
    cache_misses = 0
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        nonlocal cache_hits, cache_misses
        
        func_name = func.__name__
        
        # 引数からキャッシュキーを作成
        # kwargs を sorted して順序に依存しないようにする
        cache_key = (args, tuple(sorted(kwargs.items())))
        
        # キャッシュにあるかチェック
        if cache_key in cache:
            cache_hits += 1
            logger.debug(
                f"💾 {func_name}() キャッシュヒット "
                f"（ヒット率: {cache_hits}/{cache_hits + cache_misses}）"
            )
            return cache[cache_key]
        
        # キャッシュにない場合は実行
        cache_misses += 1
        logger.debug(f"🔍 {func_name}() キャッシュミス（新規計算）")
        
        result = func(*args, **kwargs)
        
        # 結果をキャッシュに保存
        cache[cache_key] = result
        
        return result
    
    # キャッシュクリア用のメソッドを追加
    def clear_cache():
        cache.clear()
        logger.info(f"🗑️ {func.__name__}() のキャッシュをクリアしました")
    
    wrapper.clear_cache = clear_cache
    
    return wrapper


# ===================================================================
# デコレーター8: 引数の検証
# ===================================================================

def validate_args(**validators):
    """
    関数の引数を検証するデコレーター（パラメータ付き）
    
    機能:
    - 引数の型や値を検証
    - 不正な引数で呼ばれたらエラー
    
    使用例:
        @validate_args(
            age=lambda x: isinstance(x, int) and x >= 0,
            name=lambda x: isinstance(x, str) and len(x) > 0
        )
        def register_user(name, age):
            pass
    
    Args:
        **validators: 引数名と検証関数の辞書
    
    Returns:
        デコレーター関数
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            func_name = func.__name__
            
            # 関数のシグネチャを取得
            import inspect
            sig = inspect.signature(func)
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            # 各引数を検証
            for arg_name, validator in validators.items():
                if arg_name in bound_args.arguments:
                    value = bound_args.arguments[arg_name]
                    
                    # 検証関数を実行
                    if not validator(value):
                        error_msg = (
                            f"{func_name}() の引数 '{arg_name}' が不正です: "
                            f"{value!r}"
                        )
                        logger.error(f"❌ {error_msg}")
                        raise ValueError(error_msg)
                    
                    logger.debug(f"✅ {arg_name}={value!r} 検証OK")
            
            # 実際の関数を実行
            return func(*args, **kwargs)
        
        return wrapper
    
    return decorator


# ===================================================================
# デコレーター9: デバッグ情報を出力
# ===================================================================

def debug(func: Callable) -> Callable:
    """
    デバッグ情報を詳細に出力するデコレーター
    
    機能:
    - 関数の全情報を出力
    - ソースコードの場所
    - 実行コンテキスト
    
    使用例:
        @debug
        def my_function():
            pass
    
    Args:
        func: デコレートする関数
    
    Returns:
        ラップされた関数
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        import inspect
        
        func_name = func.__name__
        
        # 関数の情報を取得
        logger.debug(f"{'🐛 DEBUG INFO ':=^60}")
        logger.debug(f"関数名: {func_name}")
        logger.debug(f"モジュール: {func.__module__}")
        
        # ソースコードの場所
        try:
            source_file = inspect.getfile(func)
            source_line = inspect.getsourcelines(func)[1]
            logger.debug(f"定義場所: {source_file}:{source_line}")
        except:
            pass
        
        # 引数情報
        logger.debug(f"引数: args={args}, kwargs={kwargs}")
        
        # 実行
        logger.debug("実行開始...")
        result = func(*args, **kwargs)
        logger.debug(f"実行完了: 戻り値={result!r}")
        logger.debug(f"{'='*60}")
        
        return result
    
    return wrapper


# ===================================================================
# デコレーター10: 複数のデコレーターを組み合わせ
# ===================================================================

def log_all(func: Callable) -> Callable:
    """
    よく使うデコレーターを全部適用する便利デコレーター
    
    機能:
    - エラーハンドリング
    - 実行時間計測
    - 関数呼び出しログ
    
    使用例:
        @log_all
        def important_function():
            pass
    
    Args:
        func: デコレートする関数
    
    Returns:
        ラップされた関数
    """
    # 複数のデコレーターを適用
    # 適用順序: 下から上に適用される
    func = log_errors(func)  # まずエラーハンドリング
    func = log_time(func)    # 次に時間計測
    func = log_call(func)    # 最後に呼び出しログ
    
    return func


# ===================================================================
# 使用例デモ
# ===================================================================

if __name__ == "__main__":
    print("=" * 70)
    print("ロギングデコレーターのデモ")
    print("=" * 70)
    
    # 例1: 基本的な関数呼び出しログ
    print("\n■ 例1: @log_call")
    print("-" * 70)
    
    @log_call
    def add(a, b):
        return a + b
    
    result = add(3, 5)
    print(f"結果: {result}")
    
    # 例2: 実行時間の計測
    print("\n■ 例2: @log_time")
    print("-" * 70)
    
    @log_time
    def slow_function():
        time.sleep(0.1)
        return "完了"
    
    slow_function()
    
    # 例3: エラーハンドリング
    print("\n■ 例3: @log_errors")
    print("-" * 70)
    
    @log_errors
    def risky_function(x):
        return 10 / x
    
    try:
        risky_function(2)  # 正常
        risky_function(0)  # エラー
    except ZeroDivisionError:
        print("エラーをキャッチしました")
    
    # 例4: 呼び出し回数のカウント
    print("\n■ 例4: @count_calls")
    print("-" * 70)
    
    @count_calls
    def counter_test():
        return "実行"
    
    counter_test()
    counter_test()
    counter_test()
    print(f"呼び出し回数: {counter_test.call_count}")
    
    # 例5: リトライ
    print("\n■ 例5: @retry")
    print("-" * 70)
    
    attempt_count = 0
    
    @retry(max_attempts=3, delay=0.5)
    def unstable_function():
        global attempt_count
        attempt_count += 1
        if attempt_count < 2:
            raise Exception("一時的なエラー")
        return "成功"
    
    result = unstable_function()
    print(f"結果: {result}")
    
    # 例6: キャッシュ
    print("\n■ 例6: @cache_result")
    print("-" * 70)
    
    @cache_result
    @log_time
    def expensive_calc(n):
        time.sleep(0.1)  # 重い処理の模擬
        return n ** 2
    
    print("1回目の呼び出し:")
    expensive_calc(5)
    
    print("2回目の呼び出し（キャッシュ）:")
    expensive_calc(5)
    
    # 例7: 全部盛り
    print("\n■ 例7: @log_all")
    print("-" * 70)
    
    @log_all
    def important_function(x, y):
        time.sleep(0.05)
        return x * y
    
    important_function(7, 8)
    
    print("\n" + "=" * 70)
    print("デモ完了！")
    print("=" * 70)