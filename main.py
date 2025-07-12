'''
250707 ジュンソ：

    game_sceneはクラスではなく関数で実装されていたため、
    result_scene.pyも同じく関数型に変更しました。

    また、main.pyでは
        game_scene -> result_scene -> 
            ・restartを選択したら再びgame_scene
            ・homeを選択したらstart_scene
    という流れになるように修正しています。

    +) 斉藤君へお願い：
        下記のように、game_scene.pyからスコアと判定数をreturnする形に修正をお願いします！
            final_score, perfect_nums, miss_nums = run_game_scene(screen, clock)
        （この形式で返せるようgame_scene側を調整してもらえると助かります）
        →修正完了しました。画像や音楽を一元管理するasset_loaderファイルを新規作成しました。
        各ファイルで同じ読み込みコードを書かずに済ませる。ゲームロジックに集中させる目的で実装しました。

250708 ジュンソ :
    asset_loader.pyの実装ありがとうございます！おかげでresult_sceneで背景の読み取りのところがもっと簡単になりました
    また、option_sceneについてはclassで実装されていたのですが、前日のコメントで

    game_sceneはクラスではなく関数で実装されていたため、
    result_scene.pyも同じく関数型に変更しました。

    すべてのシーンを関数(def)として扱うことを前提にmain.pyのコードを作成していたので、defに扱えるようにコードを修正しました。
    明日はstart_scene.pyがマージされたら全体の画面が自然に流れるのかを確認する予定です！

    +) うたこさんへお願い :
        実装してくださったstart_scene.pyをmainのレポジトリにマージしてください！

    +) 斉藤君へ :
        game_sceneの実装が一番難しいと思いますのでもし一人で実装することが難しいもしくはこの機能は実装してほしい(音楽データの保存と譜面作成など)
        ことがあったら教えてください！！

250710 ジュンソ : 
    asset_loader.pyで、miss_effectがmiss_smokeとして宣言されていたためエラーが出ていたので、修正しました。
    また、うたこさんが作成してくれたスタート画面のコードをstart_scene.pyに移し、main.pyから正常に呼び出して操作できることを確認しました。
    start_sceneでは、start / quit / optionボタンを追加し、option_sceneにもquitボタンを追加しました。
    +) 斉藤君へ :
        game_sceneを実装しようとしたところ、レーンの宣言周りでバグがあって、今日はテストできませんでした。
        実装が完了したら教えてください！

    +) うたこさんへお願い :
        譜面データの作成をお願いしたいです!
        作成方法は、このリポジトリのmain.py、game_scene.pyをGPTに入力し、対話しながら進めてください！

        もし、開発のほうもやりたいと思ったら、option_sceneのスライダーを実際に動かして、ノーツの速さや音楽の音量を調整できるようにする部分もぜひ挑戦してみてください！

        譜面をやるか開発をやるか決まったら教えてください。残りのほうを自分が担当します！

250712 ジュンソ :
    以下の修正を行いました。
    1. フォントを追加
    2. result_sceneでスコアなどの表示を新しいフォントで統一
    3. option_sceneのスライダーをマウスでドラッグ操作できるように実装
    4. start_sceneでも選択したフォントを読み込んで表示できるように対応

    また、昨日game_sceneが起動しなかった原因として、
        164行目の
            if current_time - slash_timer < slash_duration:
        という条件が、
            current_laneがNoneのままでも実行され、
            TypeError: list indices must be integers or slices, not NoneType
        が発生していました。

    こちらを
        if current_lane is not None and current_time - slash_timer < slash_duration:
        に修正することで解消しました。

    +) うたこさんへ :
        UIプロンプトの「1番スライドの写真」を高解像度で.png化し、
        assets/imagesにTitle_imageという名前で保存しておいてください！
        どの写真かはこのあとチャットで指定します。
        さらに、7ページにある巻物風の写真も別ファイルで用意してくれると助かります。
        → start_sceneの「start」「option」「exit」ボタン周りの背景に使う予定です。

    +) 斉藤君へ :
        上記game_scene.pyの164行目の修正を一度チェックお願いします。

'''

import pygame
import sys
import os

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("RhythmGame")

clock = pygame.time.Clock()
FPS = 60

from scenes.start_scene import run_start_scene
from scenes.option_scene import run_option_scene
from scenes.game_scene import run_game_scene
from scenes.result_scene import run_result_scene
from scenes.run_start_screen import run_start_screen


def main():
    run_start_screen(screen, clock)
    while True:
        choice = run_start_scene(screen, clock)

        if choice == "start":
            while True:
                final_score, perfect_nums, miss_nums = run_game_scene(screen, clock)
                result_choice = run_result_scene(screen, clock, final_score, perfect_nums, miss_nums)

                if result_choice == "quit":
                    pygame.quit()
                    sys.exit()
                elif result_choice == "menu":
                    # メインメニューへ戻る
                    break
                elif result_choice == "start":
                    # もう一度ゲームを開始
                    continue

        elif choice == "option":
            run_option_scene(screen, clock)
            import asset_loader
            import importlib
            importlib.reload(asset_loader)

        elif choice == "quit":
            break

    pygame.quit()
    sys.exit()
    
if __name__ == "__main__":
    main()