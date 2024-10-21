Requirements
Python 3.7+
FastAPI
Uvicorn
NumPy

Clone the repository:
git clone <repository-url>
cd tic_tac_toe_api

Create a virtual environment (optional but recommended):
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
pip install -r requirements.txt

Running the API:
uvicorn main:app --reload