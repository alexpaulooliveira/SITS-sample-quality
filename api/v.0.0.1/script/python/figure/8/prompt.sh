curl -X POST http://127.0.0.1:5000/statistical_summary \
  -F "project_name=pampa.25x50" \
  -F "category_column=label" \
  -F "rd_ss_csv_folder_path=/home/alex/Downloads/github/SITS-sample-quality/api/v.0.0.1/projs/pampa.25x50/00_preprocessing/original_data/" \
  -F "lof_csv_folder_path=/home/alex/Downloads/github/SITS-sample-quality/api/v.0.0.1/projs/pampa.25x50/03_lof/" \
  -F "it_csv_folder_path=/home/alex/Downloads/github/SITS-sample-quality/api/v.0.0.1/projs/pampa.25x50/12_method/data/"
