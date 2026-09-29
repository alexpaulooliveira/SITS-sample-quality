curl -X POST http://127.0.0.1:5000/statistical_summary \
  -F "project_name=cerrado.50x75" \
  -F "rotate_titles_in_the_matrix_of_confusion=true" \
  -F "category_column=label" \
  -F "rd_ss_csv_folder_path=/home/alex/Downloads/github/SITS-sample-quality/api/v.0.0.1/projs/cerrado.50x75/00_preprocessing/original_data/" \
  -F "it_csv_folder_path=/home/alex/Downloads/github/SITS-sample-quality/api/v.0.0.1/projs/cerrado.50x75/12_method/data/"
