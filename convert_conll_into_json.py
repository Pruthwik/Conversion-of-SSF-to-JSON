"""Convert SSF format into JSON."""
from argparse import ArgumentParser
from json import dump
import os


def read_lines_from_file(file_path):
    """Read the line of a text file."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readlines()


def find_sentences_from_conll_lines(lines):
    """Extract sentences from CONLL lines."""
    sentences = []
    current_sentence = []
    for line in lines:
        line = line.strip()
        if line:
            current_sentence.append(line)
        else:
            if current_sentence:
                sentences.append(current_sentence)
                current_sentence = []
    if current_sentence:
        sentences.append(current_sentence)
    return sentences


def convert_conll_to_json(conll_sentences):
    """Convert SSF sentences to a JSON-like structure."""
    json_data = []
    for sentence in conll_sentences:
        sentence_data = []
        for index_token, token in enumerate(sentence):
            parts = token.split('\t')
            if len(parts) == 3:
                lex, pos, chunk = parts
                morph = ''
            elif len(parts) == 4:
                lex, pos, chunk, morph = parts
            else:
                continue
            token_data = {
                'index': index_token + 1,  # Indexing starts from 1
                'token': lex,
                'pos': pos,
                'chunk': chunk,
                'morph': morph
            }
            sentence_data.append(token_data)
        json_data.append(sentence_data)
    return json_data


def convert_conll_into_json_for_file(input_folder_path, output_folder_path):
    """Convert CONLL files in the input folder to JSON format in the output folder."""
    for file_name in os.listdir(input_folder_path):
        input_file_path = os.path.join(input_folder_path, file_name)
        lines = read_lines_from_file(input_file_path)
        conll_sentences = find_sentences_from_conll_lines(lines)
        json_data = convert_conll_to_json(conll_sentences)
        file_root_name = file_name[:file_name.rfind('.')]
        output_file_path = os.path.join(output_folder_path, file_root_name + '.json')
        with open(output_file_path, 'w', encoding='utf-8') as json_file:
            dump(json_data, json_file, ensure_ascii=False, indent=4)


def main():
    """Main function to parse arguments and call conversion function."""
    parser = ArgumentParser(description="Convert CONLL files to JSON format.")
    parser.add_argument('--input', dest='input_folder', required=True, help="Input folder containing CONLL files")
    parser.add_argument('--output', dest='output_folder', required=True, help="Output folder for JSON files")
    
    args = parser.parse_args()
    
    input_folder_path = args.input_folder
    output_folder_path = args.output_folder
    
    if not os.path.exists(output_folder_path):
        os.makedirs(output_folder_path)
    
    convert_conll_into_json_for_file(input_folder_path, output_folder_path)


if __name__ == '__main__':
    main()
