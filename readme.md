# RFP QA

This repo is an coding assignment for the SWE role at Scribble Data.

The webapp is a streamlit app which allows users to ingest any docs, in this case, a PDF and HTML file.

# Ingestor approach:

Since the end user might be using a different set of docs, the best approach to use is the simpledirectoryloader, which allows to index multiple file types at once. 
This is also useful from an deployment POV, where pre-ingestion we can create a S3 bucket for temp storage and upload of the docs. 

For the MVP, I will be using my local directory.

