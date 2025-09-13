gcloud auth login

gcloud config set project YOUR_PROJECT_ID  
gcloud config set project thermal-proton-456700-r3

gcloud config set run/region us-central1 # O la región más cercana a tus usuarios

gcloud services enable run.googleapis.com cloudbuild.googleapis.com

gcloud run deploy YOUR_SERVICE_NAME \
    --image gcr.io/YOUR_PROJECT_ID/your-django-app:latest \
    --platform managed \
    --allow-unauthenticated \
    --region YOUR_REGION \
    --project YOUR_PROJECT_ID \
    --port 8080 # Importante: Cloud Run espera que tu app escuche en 8080


gcloud run deploy mapviewer-django --image gcr.io/thermal-proton-456700-r3/your-django-app:latest --platform managed --allow-unauthenticated --region us-central1 --project thermal-proton-456700-r3 --port 8080

---------------
gcloud builds submit --tag gcr.io/thermal-proton-456700-r3/mapviewer-django

gcloud run deploy mapviewer-django --image gcr.io/thermal-proton-456700-r3/django-app --platform managed --region us-central1 --allow-unauthenticated
gcloud run deploy mapviewer-django --image gcr.io/thermal-proton-456700-r3/mapviewer-django --platform managed --region us-central1 --allow-unauthenticated
