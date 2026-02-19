#!/bin/bash

# Ensure .streamlit directory exists (though Cloud Run mount usually handles this)
mkdir -p .streamlit

# Execute the application
exec streamlit run app.py --server.port=8080 --server.address=0.0.0.0
