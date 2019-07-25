FROM ml-base

RUN pip install pyhdfs
RUN pip install tensorflow==1.7.0

ADD src/model.py /
# ADD data /tmp/data/

ENTRYPOINT ["python", "/model.py"]