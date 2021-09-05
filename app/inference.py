import io
from PIL import Image

from commons import get_model

model = get_model()


def get_prediction(img_bytes, model):
    img = Image.open(io.BytesIO(img_bytes))
    # inference
    results = model(img, size=640)
    return results
