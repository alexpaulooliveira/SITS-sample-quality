curl -X POST http://127.0.0.1:5000/statistical_summary \
  -F "project_name=ssf.25x25" \
  -F "rotate_titles_in_the_matrix_of_confusion=true" \
  -F "category_column=Cultura" \
  -F "rd_ss_csv_folder_path=/home/alex/Downloads/github/SITS-sample-quality/api/v.0.0.1/projs/ssf.25x25/00_preprocessing/original_data/" \
  -F "it_csv_folder_path=/home/alex/Downloads/github/SITS-sample-quality/api/v.0.0.1/projs/ssf.25x25/12_method/data/"
