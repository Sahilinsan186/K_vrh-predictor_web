from flask import render_template, request, url_for
from app import app
from app.utils import predict_from_formula, predict_from_cif

@app.route("/", methods=["GET", "POST"])
def index():
    prediction = None
    error = None
    if request.method == "POST":
        formula = request.form.get("formula", "").strip()
        cif = request.files.get("cif")
        cif_content = cif.read().decode('utf-8')

        # Check if formula is provided and not empty
        if formula:
            prediction, error = predict_from_formula(formula)
        # Check if cif is provided and not empty
        elif cif:
            prediction, error = predict_from_cif(cif_content)
        else:
            error = "Please provide either a formula or a CIF input."

    return render_template("index.html", prediction=prediction, error=error)