from collections import defaultdict
from utils import get_f1_score

import json


def _get_distribution_key(cur_value, term, max_value):
    tmp_key = term * (cur_value // term)

    return min(max_value, tmp_key)


def get_numerical_data(data):
    passage_length_term = 500
    query_length_term = 5
    answer_length_term = 10
    qp_precision_term = 10

    numerical_data = {
        'number_of'
    }


    sample_value = defaultdict(float)
    sample_num = defaultdict(int)

    distributions = {
        'passage_length': {r: 0 for r in range(0, passage_length_term * 11, passage_length_term)},
        'query_length': {r: 0 for r in range(0, query_length_term * 11, query_length_term)},
        'answer_length': {r: 0 for r in range(0, answer_length_term * 11, answer_length_term)},
        'qp_precision': {r: 0 for r in range(0, qp_precision_term * 10, qp_precision_term)},
    }

    # for e in data.data:
    for e in data['data']:
        sample_num['passage'] += len(e['paragraphs'])
        for p in e['paragraphs']:
            passage_length = len(p['context'])
            sample_value['avg_passage_length'] += passage_length
            tmp_key = _get_distribution_key(passage_length, passage_length_term, passage_length_term * 10)
            distributions['passage_length'][tmp_key] += 1

            sample_num['all_queries'] += len(p['qas'])

            for qa in p['qas']:
                query_length = len(qa['question'])
                sample_value['avg_query_length'] += query_length
                tmp_key = _get_distribution_key(query_length, query_length_term, query_length_term * 10)
                distributions['query_length'][tmp_key] += 1

                if not qa.get('is_impossible', False):
                    sample_num['answerable_queries'] += 1

                    answer_length = len(qa['answers'][0]['text'])
                    sample_value['avg_answer_length'] += answer_length
                    tmp_key = _get_distribution_key(answer_length, answer_length_term, answer_length_term * 10)
                    distributions['answer_length'][tmp_key] += 1

                else:
                    sample_num['unanswerable_queries'] += 1

                qp_precision, _, _ = get_f1_score(qa['question'], p['context'], 'phrase')
                qp_precision *= 100
                sample_value['avg_qp_precision'] += qp_precision

                tmp_key = _get_distribution_key(qp_precision, qp_precision_term, qp_precision_term * 9)
                distributions['qp_precision'][tmp_key] += 1

    sample_value['avg_passage_length'] = sample_value['avg_passage_length'] / sample_num['passage']
    sample_value['avg_query_length'] = sample_value['avg_query_length'] / sample_num['all_queries']
    sample_value['avg_answer_length'] = sample_value['avg_answer_length'] / sample_num['answerable_queries']
    sample_value['avg_qp_precision'] = sample_value['avg_qp_precision'] / sample_num['all_queries']

    sample_value['']

    return sample_num


def main():
    with open('C:/Users/kstkc/Desktop/새 폴더/data/korquad1.0/KorQuAD_v1.0_dev.json') as j:
        test_data = json.load(j)

    ee = get_numerical_data(test_data)


if __name__ == '__main__':
    main()