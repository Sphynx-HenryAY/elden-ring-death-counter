# Elden Ring death counter

A simple death counter that is helping a newbie fighting Tree Sentinel.

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

