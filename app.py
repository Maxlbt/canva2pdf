from flask import Flask, request, send_file, jsonify
from flask_cors import CORS
import uuid
import os
from canva_to_pdf_and_ppt import generate_pdf_and_ppt

app = Flask(__name__)
CORS(app)

@app.route("/convert", methods=["POST"])
def convert():
    data = request.json
    url = data.get("canva_url")
    num_slides = data.get("num_slides", 30)
    output = data.get("output", "pdf")
    pdf_filename = data.get("pdf_filename", "output.pdf")
    ppt_filename = data.get("ppt_filename", "output.pptx")

    if not url:
        return jsonify({"error": "Lien Canva manquant"}), 400

    job_id = str(uuid.uuid4())
    output_folder = f"/tmp/{job_id}"
    os.makedirs(output_folder, exist_ok=True)

    pdf_file = os.path.join(output_folder, pdf_filename)
    ppt_file = os.path.join(output_folder, ppt_filename)

    try:
        # Appel à la fonction avec les bons arguments
        generate_pdf_and_ppt(
            canva_url=url,
            num_slides=int(num_slides),
            output_folder=output_folder,
            pdf_path=pdf_file,
            pptx_path=ppt_file
        )
        return send_file(pdf_file if output == "pdf" else ppt_file, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
