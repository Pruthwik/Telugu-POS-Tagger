"""Create features for CRF from raw tokenized data."""
import argparse
import os


# input is the folder containing the SSF files


def read_lines_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file_read:
        return [line.strip() for line in file_read.readlines() if line.strip()]


def read_file_and_find_features_from_sentences(file_path):
    features_string = ''
    lines = read_lines_from_file(file_path)
    sentences_found = lines
    features_string = find_features_from_sentences(sentences_found)
    return features_string


def find_features_from_sentences(sentences):
    '''
    :param sentences: Sentences read from file
    :return features: Features of all tokens for each sentence combined for all the sentences
    '''
    prefix_len = 4
    suffix_len = 7
    features = ''
    for sentence in sentences:
        sentence_features = ''
        for token in sentence.split():
            token = token.strip()
            if token:
                sentence_features += token + '\t'
                for i in range(1, prefix_len + 1):
                    sentence_features += affix_feats(token, i, 0) + '\t'
                for i in range(1, suffix_len + 1):
                    sentence_features += affix_feats(token, i, 1) + '\t'
                sentence_features = sentence_features + 'LESS\n' if len(token) <= 4 else sentence_features + 'MORE\n'
        if sentence_features.strip():
            features += sentence_features + '\n'
    return features


def affix_feats(token, length, type_aff):
    '''
    :param line: extract the token and its corresponding suffix list depending on its length
    :param token: the token in the line
    :param length: length of affix
    :param type: 0 for prefix and 1 for suffix
    :return suffix: returns the suffix
    '''
    if len(token) < length:
        return 'NULL'
    else:
        if type_aff == 0:
            return token[:length]
        else:
            return token[len(token) - length:]


def write_text_to_file(out_path, data):
    '''
    :param out_path: Enter the path of the output file
    :param data: Enter the token features of sentence separated by a blank line
    :return: None
    '''
    with open(out_path, 'w', encoding='utf-8') as fout:
        fout.write(data)


def main():
    '''
    Pass arguments and call functions here.
    :param: None
    :return: None
    '''
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', dest='inp', help="Add the input path from where tokens and its features will be extracted")
    parser.add_argument('--output', dest='out', help="Add the output file where the features will be saved")
    args = parser.parse_args()
    if not os.path.isdir(args.inp):
        features_extracted = read_file_and_find_features_from_sentences(args.inp)
        write_text_to_file(args.out, features_extracted)
    else:
        if not os.path.isdir(args.out):
            os.makedirs(args.out)
        for root, dirs, files in os.walk(args.inp):
            for fl in files:
                file_name = fl[: fl.rfind('.')]
                input_path = os.path.join(root, fl)
                output_path = os.path.join(args.out, file_name + '-features-for-pos.txt')
                features_extracted = read_file_and_find_features_from_sentences(input_path)
                write_text_to_file(output_path, features_extracted)


if __name__ == '__main__':
    main()
