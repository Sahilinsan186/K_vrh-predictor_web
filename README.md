# Bulk Modulus Prediction Using Machine Learning

## Overview
This project is a machine learning-based web application for predicting the bulk modulus (K_VRH) of crystalline materials. The application allows users to either enter a chemical formula or upload a CIF (Crystallographic Information File) and obtain a predicted bulk modulus value.
The project combines materials science tools such as Pymatgen and Matminer with machine learning models trained on data from the Materials Project elastic tensor dataset.

## Features
* Predict bulk modulus from a chemical formula
* Predict bulk modulus from a CIF structure file
* Automated feature extraction using Matminer
* Flask-based web interface
* Supports both composition-based and structure-based prediction pipelines
* Trained and optimized machine learning models with feature scaling

## Dataset
The models were trained using the Elastic Tensor 2015 dataset available through Matminer and derived from the Materials Project database.

## Target Property:
K_VRH (Bulk Modulus)


## Feature Engineering
### Composition-Based Features
Chemical formulas are converted into Pymatgen Composition objects and featurized using Matminer's Magpie descriptors.

Examples of extracted features:
* Atomic number statistics
* Electronegativity statistics
* Atomic radius statistics
* Melting temperature statistics
* Elemental property distributions

### Structure-Based Features
For CIF inputs, crystal structures are converted into Pymatgen Structure objects and featurized using:

#### Density Features
* Density
* Volume per atom
* Packing fraction

#### Global Symmetry Features
* Space group number
* Crystal system index
* Centrosymmetry information

#### Composition Features
Magpie descriptors are additionally extracted from the structure composition.


## Machine Learning Models Evaluated
The following regression models were tested:

* Decision Tree Regressor
* Random Forest Regressor
* Gradient Boosting Regressor
* Support Vector Regressor (SVR)
* AdaBoost Regressor

### Best Performing Model
Gradient Boosting Regressor

Performance:
* R² Score ≈ 0.94

Hyperparameter tuning was performed using GridSearchCV.


## Project Workflow
Formula Input:

Formula
→ Composition
→ Magpie Features
→ Feature Scaling
→ Trained ML Model
→ Predicted Bulk Modulus

Structure Input:
CIF File
→ Structure Parsing
→ Density Features
→ Symmetry Features
→ Magpie Features
→ Feature Scaling
→ Trained ML Model
→ Predicted Bulk Modulus


## Technology Stack

### Materials Science Libraries
* Pymatgen
* Matminer
* Materials Project API

### Machine Learning
* Scikit-learn
* Pandas
* NumPy
* Joblib

### Web Development
* Flask
* HTML
* Tailwind CSS

## Installation
Clone the repository:

```bash
git clone <repository-url>
cd bulk-modulus-predictor
```

Install dependencies:
```bash
pip install -r requirements.txt
```

Create a `.env` file:
```env
MP_API_KEY=your_materials_project_api_key
```

Run the application:
```bash
flask run
```

Open:
```text
http://127.0.0.1:5000
```


## Future Improvements
* Integration of Graph Neural Networks (CGCNN, MEGNet, M3GNet)
* Prediction of additional mechanical properties
* Larger and more diverse training datasets
* Explainable AI analysis for feature importance
* Cloud deployment and public API support

## Author
Sahil Insan

B.Tech, Metallurgical and Materials Engineering

Indian Institute of Technology Roorkee
