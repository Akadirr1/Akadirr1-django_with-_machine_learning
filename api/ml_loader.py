import os
import joblib
from django.conf import settings

MODEL_FILES = {
    'knn': 'model_knn.pkl',
    'svm': 'model_svm.pkl',
    'dt':  'model_dt.pkl'
}
LOADED_MODELS={}

base_path= os.path.join(settings.BASE_DIR,'api','ml_models')
for model_key,filename in MODEL_FILES.items():
    full_path=os.path.join(base_path,filename)
    if os.path.exists(full_path):
        try:
            LOADED_MODELS[model_key]=joblib.load(full_path)
        except Exception as e:
            print(f"{e} hatası!")
    else:
        print("yol bulunamadı")        

print("yükleme tamamlandı dostum")