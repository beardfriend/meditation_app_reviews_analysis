import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import urllib.request
from collections import Counter
from kiwipiepy import Kiwi
from kiwipiepy.utils import Stopwords
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences


def tokenizing(sentence):
    try:
        if not sentence:
            raise ValueError
        words = [
            token[0] for token in kiwi.tokenize(sentence) if token[0] not in stopwords
        ]
    except ValueError as e:
        print(e)

    return words


def main():
    # 데이터 로드
    urllib.request.urlretrieve(
        "https://raw.githubusercontent.com/bab2min/corpus/master/sentiment/naver_shopping.txt",
        filename="ratings_total.txt",
    )

    total_data = pd.read_table("ratings_total.txt", names=["ratings", "reviews"])
    total_data["label"] = np.select([total_data.ratings > 3], [1], default=0)

    # # 중복제거
    total_data.drop_duplicates(subset=["reviews"], inplace=True)

    # # 데이터 정제
    total_data["reviews"] = total_data["reviews"].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]", "")
    total_data["reviews"].replace("", np.nan, inplace=True)

    # # 토큰화
    print(total_data)
    total_data["tokenized"] = total_data["reviews"].apply(tokenizing)

    # print(total_data)
    # 부정 긍정 체크
    negative_words = np.hstack(total_data[total_data.label == 0]["tokenized"].values)
    positive_words = np.hstack(total_data[total_data.label == 1]["tokenized"].values)
    negative_word_count = Counter(negative_words)
    print(negative_word_count.most_common(20))
    positive_word_count = Counter(positive_words)
    print(positive_word_count.most_common(20))


main()
