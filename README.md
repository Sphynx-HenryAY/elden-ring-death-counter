# Elden Ring death counter
A simple death counter that is helping a newbie fighting Tree Sentinel.

# OCR
This counter is using the [tesseract](https://github.com/tesseract-ocr/tesseract) OCR engine.

Installer shortcut:
- [Windows 64 bit](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w64-setup-v5.0.1.20220118.exe)
- [Windows 32 bit](https://digi.bib.uni-mannheim.de/tesseract/tesseract-ocr-w32-setup-v5.0.1.20220118.exe)

# Detection flow
1. read centre of screenshot
2. convert coloured screenshot into gray graded
3. ocr to detect string from gray graded screenshot
4. fuzzy match detected string with "YOU DIED" with default threshold 80%
5. add 1 to counter if matched

## Tree Sentinel Progress
Will be keep updated until Tree Sentinel fall. 🥲
- game time: 4:30
- death count: 159
- best hit: 70%

# Future plan
- Simplify detection mechanism.
- Add web ui for easy configuration.
- Create web page to show counter on green background, to be used in live streaming.
- See if display overlay possible.
- BEAT THAT TREE SENTINEL.
