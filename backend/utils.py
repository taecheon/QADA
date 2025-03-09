from __future__ import print_function
from collections import Counter
import string
import re


'''KorQuAD v1.0에 대한 공식 평가 스크립트 '''
'''본 스크립트는 SQuAD v1.1 평가 스크립트 https://rajpurkar.github.io/SQuAD-explorer/ 를 바탕으로 작성됨.'''


def _get_tokens(s):
    if not s:
        return []
    return _normalize_answer(s).split()


def _normalize_answer(s):
    def remove_(text):
        ''' 불필요한 기호 제거 '''
        try:
            text = re.sub("'", " ", text)
            text = re.sub('"', " ", text)
            text = re.sub('《', " ", text)
            text = re.sub('》', " ", text)
            text = re.sub('<', " ", text)
            text = re.sub('>', " ", text)
            text = re.sub('〈', " ", text)
            text = re.sub('〉', " ", text)
            text = re.sub("\(", " ", text)
            text = re.sub("\)", " ", text)
            text = re.sub("‘", " ", text)
            text = re.sub("’", " ", text)
        except TypeError:
            print(f'**** {text} ****')
        return text

    def white_space_fix(text):
        return ' '.join(text.split())

    def remove_punc(text):
        exclude = set(string.punctuation)
        return ''.join(ch for ch in text if ch not in exclude)

    def lower(text):
        return text.lower()

    return white_space_fix(remove_punc(lower(remove_(s))))


def get_f1_score(prediction, ground_truth, option):
    if prediction == ground_truth and ground_truth == '':
        return 1.0, 1.0, 1.0

    ground_truth_tokens = _get_tokens(ground_truth)
    prediction_tokens = _get_tokens(prediction)

    if option == 'character':
        ground_truth_char = []
        for tok in ground_truth_tokens:
            now = [a for a in tok]
            ground_truth_char.extend(now)

        prediction_char = []
        for tok in prediction_tokens:
            now = [a for a in tok]
            prediction_char.extend(now)

        ground_truth = ground_truth_char
        prediction = prediction_char
    else:
        ground_truth = ground_truth_tokens
        prediction = prediction_tokens

    common = Counter(ground_truth) & Counter(prediction)
    num_same = sum(common.values())
    if num_same == 0:
        return 0.0, 0.0, 0.0

    precision = 1.0 * num_same / len(prediction)
    recall = 1.0 * num_same / len(ground_truth)
    f1 = (2 * precision * recall) / (precision + recall)

    return precision, recall, f1