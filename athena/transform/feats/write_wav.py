# Copyright (C) 2017 Beijing Didi Infinity Technology and Development Co.,Ltd.
# All rights reserved.
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
# ==============================================================================
"""The model write audio sample to wav file."""

import tensorflow as tf
from athena.utils.hparam import HParams
from athena.transform.feats.base_frontend import BaseFrontend


class WriteWav(BaseFrontend):
  """
  Encode audio data (input) using sample rate (input),
  return a write wav opration.
  """

  def __init__(self, config: dict):
    super().__init__(config)

  @classmethod
  def params(cls, config=None):
    """
      Set params.
       :param config: contains one optional parameters:sample_rate(int, default=16000).
       :return: An object of class HParams, which is a set of hyperparameters as
                name-value pairs.
       """

    sample_rate = 16000

    hparams = HParams(cls=cls)
    hparams.add_hparam('sample_rate', sample_rate)

    if config is not None:
      hparams.override_from_dict(config)

    return hparams

  def call(self, filename, audio_data, sample_rate):
    """
    Write wav using audio_data[tensor].
    :param filename: filepath of wav.
    :param audio_data: a tensor containing data of a wav.
    :param sample_rate: the samplerate of the signal we working with.
    :return: write wav opration.
    """
    filename = tf.constant(filename)

    with tf.name_scope('writewav'):
      audio_data = tf.cast(audio_data, dtype=tf.float32)
      contents = tf.audio.encode_wav(
          tf.expand_dims(audio_data, 1), tf.cast(sample_rate, dtype=tf.int32))
      w_op = tf.io.write_file(filename, contents)

    return w_op
