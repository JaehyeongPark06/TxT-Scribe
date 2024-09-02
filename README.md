# TxT-Scribe

![TxTScribe Sample Use](https://user-images.githubusercontent.com/78674944/236726857-b2feb3d5-40bd-4377-ab2a-5f8a326311e6.gif)

## About

A rudimentary OCR - image reader that can extract text from images and copy it to the user's clipboard. Features a snipping tool, notification popups and programmable hotkeys. 

## Libraries and Tools Used
- [PySide6 (Qt)](https://pypi.org/project/PySide6/) 
- [pytesseract, OCR](https://pypi.org/project/pytesseract/)
- [Pillow, PIL](https://github.com/python-pillow/Pillow/) 
- [pynput, keyboard](https://pypi.org/project/pynput/) 
- [pyperclip](https://pypi.org/project/pyperclip/) 
- [pynotifier](https://pypi.org/project/py-notifier/) 

## Getting Started
1. Download all the packages using pip or conda
2. Run the program and press the default hotkey (ctrl + alt + g) or adjust it to your liking

## Possible Improvements
- Packaging it into a system tray background app (like [lightshot](https://app.prntscr.com/en/index.html))
- Customizable hotkey menu when a user right clicks the icon in the system tray
- Using a better OCR model

## License
See [License](https://github.com/JaehyeongPark06/TxT-Scribe/blob/main/LICENSE)
