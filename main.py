from flask import Flask, request, jsonify, render_template, redirect, url_for
import os
from helpers import process_docs, setup_qa_chain, getanswer
import logging
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv("OPENAI_API_KEY")

logger = logging.getLogger(__name__)

vectordb = None

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "OK"}), 200

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    global vectordb
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return jsonify({"status": "Failure", "message": "No file part in the request"}), 400

        files = request.files.getlist('files[]')

        if not os.path.exists('docs'):
            os.makedirs('docs')

        filenames = []
        for file in files:
            if file.filename == '':
                return jsonify({"status": "Failure", "message": "No selected file"}), 400
            file.save(os.path.join('docs', file.filename))
            filenames.append(file.filename)
        
        vectordb = process_docs()  # this will now setup vectordb for each upload
        logger.info(f"Files {filenames} uploaded successfully.")
        return jsonify({"status": "Success", "redirect_url": url_for('processclaim')})
    else:
        return render_template('upload.html')


@app.route('/docqna', methods=['GET', 'POST'])
def processclaim():
    global vectordb
    if request.method == 'POST':
        chain = setup_qa_chain()
        try:
            query = request.form.get("query")
            if not query:
                return jsonify({"status": "Failure", "message": "No query provided"}), 400
            output = getanswer(vectordb, chain, query)
            logger.info(f"Query processed successfully.")
            return jsonify(output)
        except Exception as e:
            logger.error(f"Error while processing query: {str(e)}")
            return jsonify({"status": "Failure", "message": str(e)})
    else:
        return render_template('docqna.html')

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
