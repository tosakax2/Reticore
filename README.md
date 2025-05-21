# Reticore

**Windows 11 向けの常時表示クロスヘアツール**  
Python + PyQt6 製の軽量アプリケーションで、画面中央にシンプルな照準を表示します。

---

## 主な機能

- **サイズ調整**：10 / 14 / 18 / 22 / 26 / 30（ピクセル単位で中央に整列）
- **太さ調整**：1 / 2 / 3 px
- **色変更**：カラーピッカーで任意の色を選択（デフォルトはシアン）
- **最前面オーバーレイ**：他ウィンドウより前に透明表示
- **マウス透過**：ゲーム・作業の邪魔になりません
- **GUIで簡単操作**：有効化／無効化はワンクリック

---

## 動作環境

- OS：**Windows 11**
- Python：**3.13 以降**
- ライブラリ：
  ```bash
  pip install PyQt6
  ```

---

## 実行方法

```bash
python main.py
```

---

## EXEファイル化（PyInstaller）

以下コマンドで単体の `.exe` を作成可能です：

```bash
pyinstaller --noconsole --onefile --icon=cyber_crosshair.ico --name Reticore main.py
```

生成後の実行ファイル：

```
dist/crosshair_tool.exe
```

- Python や PyQt がインストールされていない環境でもそのまま起動可能です。
