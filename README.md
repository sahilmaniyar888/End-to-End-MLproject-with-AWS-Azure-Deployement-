# ML End-to-End Student Performance Project

Flask app that predicts student `math_score` from profile and test inputs.

## Project Structure

- `app.py`: Flask routes and form handling
- `wsgi.py`: production WSGI entrypoint
- `src/pipeline/train_pipeline.py`: full train pipeline
- `src/pipeline/prediction_pipeline.py`: inference pipeline
- `artifacts/`: trained model and preprocessor files

## Setup

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

## Train Model

```bash
python -m src.pipeline.train_pipeline
```

This generates/updates:

- `artifacts/model.pkl`
- `artifacts/preprocessor.pkl`

## Run App (Local)

```bash
python app.py
```

Open:

- `http://127.0.0.1:5000/`

## Run App (Production Style)

```bash
gunicorn wsgi:app --bind 0.0.0.0:5000
```

## Deployment Notes

- Ensure `artifacts/model.pkl` and `artifacts/preprocessor.pkl` exist before deploy.
- If your platform does not support `gunicorn` on Windows, use it in Linux-based hosting (Render, Railway, Azure Web App Linux, etc.).
