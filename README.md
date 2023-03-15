# Telugu-POS-Tagger
This is a repository for CRF based Telugu POS tagger.
## Install CRF++ from this link https://taku910.github.io/crfpp/, download and install the latest version
## How to run the code
Involves 2 steps
## 1. Create features for CRF
python create_features_for_crf_from_raw_tokenized_data.py --input input_file --output output_file
### The format of the input file: One sentence per line
### If you need a tokenizer for Indian Languages, use this repository
https://github.com/Pruthwik/Tokenizer_for_Indian_Languages 
## 2. Run the CRF model to predict tags on the features file
### crf_test -m model_path features_file > predicted_outputs
### cut -f1,14 predicted_outputs > token_predicted_pos.txt
