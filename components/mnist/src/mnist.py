import argparse
import logging
import os

import pyhdfs

def main(argv=None):
    parser = argparse.ArgumentParser()
    parser.add_argument('--webhdfs_host', type=str, help='webhdfs endpoint')
    parser.add_argument('--input_path', type=str, help='hdfs input path')
    parser.add_argument('--output_path', type=str, help='hdfs output path')
    args = parser.parse_args()

    client = pyhdfs.HdfsClient(hosts = args.webhdfs_host)
    
    # 此处可以直接从hdfs读取文件加载到内存，tensorflow也有相应的hdfs数据源
    # 方便起见就直接把数据get到本地文件夹了
    os.makedirs('/data')
    for h_f in client.listdir(args.input_path):
        client.copy_to_local(args.input_path + '/' + h_f, '/data/' + h_f)
    
    

if __name__ == "__main__":
    main()