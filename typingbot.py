from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

def auto_typing_benesse(url: str, delay: float = 0.07):
    """
    Benesse マナビジョンのタイピング練習（日本語編）を自動入力するスクリプト。
    url: タイピング練習のページ URL（例 “https://manabi.benesse.ne.jp/gakushu/typing/”）
    delay: 文字入力間隔（秒単位、0.05～0.1 程度が実用的）
    """
    # WebDriver を起動（ChromeDriver のパスは環境に合わせて）
    driver = webdriver.Chrome()
    driver.get(url)

    # ページ読み込み待ち
    time.sleep(2)

    # “設定 → タイピング開始” ボタンをクリックする
    # HTML に “button.typingButton” があるようなので、まずそれを探す
    try:
        start_btn = driver.find_element(By.CSS_SELECTOR, "button.typingButton")
        start_btn.click()
        time.sleep(1)
    except Exception as e:
        print("typingButton ボタンをクリックできません:", e)

    # スペースキーで開始する画面に遷移しているなら、スペースキーを送る
    body = driver.find_element(By.TAG_NAME, "body")
    body.send_keys(Keys.SPACE)
    time.sleep(0.5)

    # JavaScript 側で “残り文字列” を取得するスクリプト
    # あなたの HTML にあった id 要素 (“remaining3”, “remaining2”, “remaining”) を参照する
    get_remaining_js = """
    () => {
      let parts = [];
      for (let id of ['remaining3','remaining2','remaining']) {
        let el = document.getElementById(id);
        if (el && el.innerText) {
          parts.push(el.innerText);
        }
      }
      return parts.join('');
    }
    """

    # 入力ループ
    while True:
        try:
            remaining = driver.execute_script(get_remaining_js)
        except Exception as e:
            print("JS 実行でエラー:", e)
            break

        # 残り文字が空または None ならループ終了
        if not remaining:
            print("残り文字なし、ループを抜けます")
            break

        # 最初の1文字を取ってキー入力
        ch = remaining[0]
        # body に送信（JavaScript 側で keydown / keypress / keyup を捕捉している想定）
        body.send_keys(ch)
        time.sleep(delay)

    # 余裕を持って終了待機
    time.sleep(2)
    driver.quit()

if __name__ == "__main__":
    target = "https://manabi.benesse.ne.jp/gakushu/typing/"
    auto_typing_benesse(target, delay=0.08)
