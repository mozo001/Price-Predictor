Demo LINK =  https://price-predictor-tkmk.onrender.com
# README.md content
readme_content = """# Laptop Price Predictor

A full-stack Machine Learning application built with **Django** and **Scikit-Learn** that predicts the market price of a laptop based on its hardware specifications.

##  Features
- **Dynamic Predictions:** Uses a Random Forest Regressor pipeline (trained to ~88% R² score).
- **Smart UI:** Interactive web interface with Bootstrap 5.
- **Automated Insights:** Automatically identifies "Gaming" laptops and highlights expensive predictions.
- **Optimized Data Pipeline:** Custom feature engineering including PPI (Pixels Per Inch) calculation and CPU/GPU brand extraction.

##  Tech Stack
- **Backend:** Python, Django
- **Machine Learning:** Scikit-Learn, Pandas, NumPy
- **Frontend:** HTML5, CSS3, Bootstrap 5
- **Environment:** Developed on Fedora Workstation (Hyprland WM)
📊 Model Information
The project utilizes an ensemble learning approach. We transitioned from Linear Regression to a Random Forest Regressor to better capture the non-linear relationships between hardware specs (like specialized GPUs) and price.

##  Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/mozo001/Price-Predictor.git
   cd Price-Predictor
Create a virtual environment:

Bash
python -m venv .venv
source .venv/bin/activate  # On Linux/macOS
Install dependencies:

Bash
pip install -r requirements.txt
Run the application:

Bash
python manage.py runserver
Open http://127.0.0.1:8000 in your browser.
