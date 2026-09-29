curl -X POST http://127.0.0.1:5000/step_03__build_the_exclusion_map_and_exclude \
  -F "project_name=pampa.15x15" \
  -F "iteration_number=2" \
  -F "prior_threshold=0.6" \
  -F "posterior_threshold=0.6" \
  -F "column_key=id" \
  -F "category_column=label" \
  -F "with_indexes=true" \
  -F "indexes_font=8" 
