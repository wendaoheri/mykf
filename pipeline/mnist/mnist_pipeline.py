# Copyright 2019 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
Kubeflow Pipelines MNIST example

Run this script to compile pipeline
"""


import kfp.dsl as dsl

@dsl.pipeline(
  name='MNIST',
  description='A pipeline to train and serve the MNIST example.'
)
def mnist_pipeline(webhdfs_hosts='',
                   tf_data_dir='/tmp/data/mnist',
                   model_export_dir='/tmp/model/mnist',
                   train_steps='200',
                   learning_rate='0.01',
                   batch_size='100'):
  """
  Pipeline with three stages:
    1. train an MNIST classifier
    2. deploy a tf-serving instance to the cluster
  """
  ## 定义训练
  train = dsl.ContainerOp(
      name='train',
      image='registry.cn-hangzhou.aliyuncs.com/mykf/ml-mnist',
      arguments=[
          "--webhdfs-hosts", webhdfs_hosts,
          "--tf-data-dir", tf_data_dir,
          "--tf-export-dir", model_export_dir,
          "--tf-train-steps", train_steps,
          "--tf-batch-size", batch_size,
          "--tf-learning-rate", learning_rate
          ]
  )

  ## 定义服务
  server = dsl.ContainerOp(
      name='tf-serving',
      image='registry.cn-hangzhou.aliyuncs.com/mykf/ml-tfserving',
      arguments=[
          "--webhdfs-hosts", webhdfs_hosts,
          "--tf-export-dir", model_export_dir,
          "--model-name", 'mnist',
          "--model-base-path", '/model'
          ]
  )

  ## 让服务在训练之后执行
  server.after(train)

if __name__ == '__main__':
  import kfp.compiler as compiler
  compiler.Compiler().compile(mnist_pipeline, __file__ + '.tar.gz')
