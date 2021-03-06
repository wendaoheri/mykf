from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import argparse
import pyhdfs
import subprocess
import os
import sys

def download_data_from_hdfs(client, input_data_dir, dest_dir):
  if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)
  for data_file in client.listdir(input_data_dir):
    src_path = input_data_dir + '/' + data_file
    dest_path = dest_dir + '/' + data_file
    status = client.get_file_status(src_path)
    if status.type == 'DIRECTORY':
      download_data_from_hdfs(client, src_path, dest_path)
    else:
      client.copy_to_local(src_path, dest_path)

def main(argv=None):
    parser = argparse.ArgumentParser(description='tf serving')
    parser.add_argument('--webhdfs-hosts', type=str, help='webhdfs hosts')
    parser.add_argument('--tf-export-dir', type=str, help='hdfs path ')
    parser.add_argument('--port', type=int, default=8500, help='server port')
    parser.add_argument('--rest-api-port', type=int, default=8501, help='rest api port')
    parser.add_argument('--model-name', type=str, help='model name')
    parser.add_argument('--model-base-path', type=str, default='/model',help='model base path')
    args = parser.parse_args()

    client = pyhdfs.HdfsClient(hosts = args.webhdfs_hosts)

    download_data_from_hdfs(client, args.tf_export_dir,args.model_base_path)
    
    cmd = [
        'tensorflow_model_server',
        '--port=' + str(args.port),
        '--rest_api_port=' + str(args.rest_api_port),
        '--model_name=' + args.model_name,
        '--model_base_path=' + args.model_base_path
    ]
    print(cmd)
    popen = subprocess.Popen(cmd,
                         stdout = subprocess.PIPE,
                         stderr = subprocess.PIPE,
                         bufsize=1)
    
    for line in iter(popen.stdout.readline, b''):
        print(line)
    popen.stdout.close()
    popen.wait()

if __name__ == '__main__':
    main()