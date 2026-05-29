import os
import joblib
import pandas as pd
from dotenv import load_dotenv
from flask import render_template, request, url_for
from app import app
from mp_api.client import MPRester
from matminer.featurizers.structure import DensityFeatures, GlobalSymmetryFeatures
from matminer.featurizers.composition import ElementProperty
from pymatgen.core import Composition, Structure

import json

def find_duplicates(lst):
    seen = set()
    duplicates = set()
    for item in lst:
        if item in seen:
            duplicates.add(item)
        else:
            seen.add(item)
    return list(duplicates)


with open("models/structure_feature_cols2.json") as f:
    structure_feature_cols = json.load(f)

print(find_duplicates(structure_feature_cols))  
# Load environment variables
load_dotenv()
MP_API_KEY = os.getenv("MP_API_KEY")

# Load models and scalers
MODEL_PATH1 = "models/best_structure_model4.pkl"
SCALER_PATH1 = "models/best_structure_scaler4.pkl"
structure_model = joblib.load(MODEL_PATH1)
structure_scaler = joblib.load(SCALER_PATH1)

MODEL_PATH2 = "models/best_formula_model2.pkl"
SCALER_PATH2 = "models/best_formula_scaler2.pkl"
formula_model = joblib.load(MODEL_PATH2)
formula_scaler = joblib.load(SCALER_PATH2)


def predict_from_formula(formula):
    try:
        # Validate and convert formula to Composition
        composition = Composition(formula)

        # Query Materials Project for stable structures
        with MPRester(MP_API_KEY) as m:
            data = m.materials.summary.search(
                formula=formula, fields=["bulk_modulus", "energy_above_hull"]
            )

        if not data:
            return None, "Formula not found in Materials Project."

        # Filter stable structures (energy_above_hull == 0)
        stable = [d for d in data if d.energy_above_hull == 0]
        if stable and stable[0].bulk_modulus is not None:
            bulk_modulus = stable[0].bulk_modulus
        else:
            # Fallback to the most stable structure
            most_stable = sorted(data, key=lambda d: d.energy_above_hull or float("inf"))[0]
            if most_stable.bulk_modulus is None:
                return None, "No bulk modulus data available for the formula."
            bulk_modulus = most_stable.bulk_modulus

        # Featurize composition using magpie
        comp_featurizer = ElementProperty.from_preset("magpie")
        formula_features = comp_featurizer.featurize(composition)
        df_formula_feats = pd.DataFrame([formula_features], columns=comp_featurizer.feature_labels())
        print(df_formula_feats.columns)
        # Scale features and predict
        X = formula_scaler.transform(df_formula_feats)
        print("Expected formula features:", formula_scaler.feature_names_in_)
        prediction = formula_model.predict(X)[0]
        return round(prediction, 3), None

    except Exception as e:
        return None, f"Prediction error: {str(e)}"

def predict_from_cif(cif_content):
    print()
    try:
        # Convert CIF content to pymatgen Structure
        structure = Structure.from_str(cif_content, fmt="cif")

        # Create a dataframe with the structure and composition
        df = pd.DataFrame({"structure": [structure], "composition": [structure.composition]})

        # Featurize structure using DensityFeatures and GlobalSymmetryFeatures
        df_structure_feats = DensityFeatures().featurize_dataframe(df, "structure")
        df_structure_feats = GlobalSymmetryFeatures().featurize_dataframe(df_structure_feats, "structure")

        # Featurize composition using magpie
        comp_featurizer = ElementProperty.from_preset("magpie")
        comp_features = pd.DataFrame(
            [comp_featurizer.featurize(df["composition"].iloc[0])],
            columns=comp_featurizer.feature_labels()
        )

        # Concatenate structure and composition features
        df_structure_feats = pd.concat([df_structure_feats, comp_features], axis=1)

        # Drop unnecessary columns if they exist
        columns_to_drop = [
            col for col in ["structure", "composition", "crystal_system", "is_centrosymmetric"]
            if col in df_structure_feats.columns
        ]
        df_structure_feats = df_structure_feats.drop(columns=columns_to_drop, errors="ignore")
        for col in structure_feature_cols :
            if col not in df_structure_feats.columns:
                print(col)


        # Scale features and predict
        X = structure_scaler.transform(df_structure_feats)
        prediction = structure_model.predict(X)[0]
        return round(prediction, 3), None

    except Exception as e:
        return None, f"Prediction error: {str(e)}"