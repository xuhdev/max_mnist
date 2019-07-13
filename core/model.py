#
# Copyright 2018-2019 IBM Corp. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

from maxfw.model import MAXModelWrapper
from keras.models import load_model
from keras.preprocessing.image import img_to_array
from PIL import Image
import numpy as np
import io

import logging
from config import DEFAULT_MODEL_PATH

logger = logging.getLogger()


class ModelWrapper(MAXModelWrapper):

    MODEL_META_DATA = {
        'id': 'Image Classification',
        'name': 'MAX-MNIST',
        'description': 'Classify digits',
        'type': 'Keras model',
        'source': 'Keras',
        'license': 'Apache 2.0'
    }

    def __init__(self, path=DEFAULT_MODEL_PATH):
        logger.info('Loading model from: {}...'.format(path))
        # Load the graph
        self.model = load_model(path)
        self.model._make_predict_function()
        logger.info('Loaded model')

    def _pre_process(self, inp):
        img = Image.open(io.BytesIO(inp))
        print('reading image..', img.size)
        image = img_to_array(img)
        print('image array shape..', image.shape)
        image = np.expand_dims(image, axis=0)
        return image

    def _post_process(self, result):
        return [result['probability'][0][
                    np.argmax(result['probability'])],
                np.argmax(result['output'])]

    def _predict(self, x):
        predict_dict = {'output': self.model.predict(x),
                        'probability': self.model.predict_proba(x)
                        }
        return predict_dict
