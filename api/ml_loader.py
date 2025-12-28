import os
import joblib
from django.conf import settings

MODEL_FILES = {
    'knn': 'model_knn.pkl',
    'svm': 'model_svm.pkl',
    'dt':  'model_dt.pkl'
}
LOADED_MODELS={}
