FROM pytorch/pytorch

WORKDIR /workspace
ADD . /workspace

RUN apt-get update && apt-get install -y python3-opencv
RUN pip install opencv-python

RUN pip install -r requirements.txt

CMD [ "python" , "/workspace/app.py" ]