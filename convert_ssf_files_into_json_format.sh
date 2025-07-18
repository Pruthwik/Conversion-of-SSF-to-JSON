# Convert SSF files into JSON format
# Usage: bash convert_ssf_files_into_json_format.sh <input_directory> <output_directory> <level>
#!/bin/bash
input_directory=$1
output_directory=$2
level=$3
# for POS, Chunk files use level 3
# for POS, Chunk, and morph files use level 4
if [ "$#" -ne 3 ]; then
    echo "Usage: $0 <input_directory> <output_directory> <level>"
    exit 1
fi
if [ ! -d $output_directory ]; then
    echo "Output directory does not exist: $output_directory"
    mkdir -p $output_directory
fi
python3 extract_data_from_ssf_in_conll_format_for_folder.py --input $input_directory --output $input_directory"-CONLL" --level $level
python3 convert_conll_into_json.py --input $input_directory"-CONLL" --output $output_directory
rm -rf $input_directory"-CONLL"
echo "Conversion completed. All the JSON files are saved in $output_directory"
exit 0