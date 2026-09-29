curl -X POST http://127.0.0.1:5000/som_hyperparameters_summary \
    -F "project_name=pampa.15x15" \
    -F "file=@/home/alex/Downloads/github/SITS-sample-quality/api/v.0.0.1/projs/pampa.15x15/07_rna_hyperparameters/pampa_hyperparameters_test.csv" 
