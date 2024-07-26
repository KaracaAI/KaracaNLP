import os
import joblib
from .normalize import Normalize
karaca_path = os.path.dirname(os.path.abspath(__file__))
class Emotion:
    def __init__(self):
        self.name = "Emotion"
    @classmethod
    def guess(cls, text):
        model_dosya_adi = karaca_path + '/datas/emotionDatas/emotionModel.joblib'
        egitilmis_model = joblib.load(model_dosya_adi)

        vektorizer_dosya_adi = karaca_path + '/datas/emotionDatas/emotionVektorizer.joblib'
        yuklenmis_vektorizer = joblib.load(vektorizer_dosya_adi)

        label_encoder_dosya_adi = karaca_path + '/datas/emotionDatas/emotionLabelEncoder.joblib'
        yuklenmis_label_encoder = joblib.load(label_encoder_dosya_adi)
        text = Normalize.remove_punc(Normalize.remove_stopwords(Normalize.lower_text(text)))
        new_text = [text]

        new_text_transformed = yuklenmis_vektorizer.transform(new_text).toarray()

        predicted_proba = egitilmis_model.predict_proba(new_text_transformed)
        predicted_label = egitilmis_model.predict(new_text_transformed)
        predicted_duygu = yuklenmis_label_encoder.inverse_transform(predicted_label)

        predicted_probability = predicted_proba[0][predicted_label[0]] * 100

        return (f"Tahmin Edilen Duygu: {predicted_duygu[0]} % {predicted_probability:.2f}")


