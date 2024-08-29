## How to use?

```
cd 0.Listen/C3
```

### Dictation

Chapter 1: https://www.bilibili.com/video/BV1QG411a7fy

```
vim 1/xxx # format like test_sample
```

### Check
```
./check.py 1/1 1/xxx
```

### Practice the incorrecr words

```
./practice.py # load incorrect_words.json
```


## Comments


https://github.com/RealKai42/qwerty-learner/blob/master/public/dicts/IELTS_WANG_3.json


```
jq '.[0:112] |' IELTS_WANG_3.json > C3_1

jq '.[112:255]' IELTS_WANG_3.json > C3_2

```


