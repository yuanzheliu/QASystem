# Ubuntu Linux as the base image
FROM ubuntu:16.04
# Set UTF-8 encoding
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
# Install packages, you should modify this based on your program
RUN apt-get -y update && \
apt-get -y upgrade && \
apt-get -y install python3-pip python3-dev && \
pip3 install --upgrade pip && \
pip3 install thinc && \
pip3 install spacy && \
python3 -m spacy download en_core_web_lg

RUN pip3 install fuzzywuzzy
RUN pip3 install singledispatch
RUN pip3 install nltk && \
python3 -c "import nltk; nltk.download(['punkt', 'averaged_perceptron_tagger', 'maxent_ne_chunker', 'words'])"

RUN pip3 install python-Levenshtein 

RUN mkdir docker
ADD answer /docker/
ADD ask /docker/
ADD ask_sentence.py /docker/
ADD english.muc.7class.distsim.crf.ser.gz /docker/
ADD parse.py /docker/
ADD question_type.py /docker/
ADD stanford-ner.jar /docker/
ADD top_k_sentences.py /docker/
ADD wh.py /docker/
ADD yes_no.py /docker/

CMD ["chmod 777 ask"]
CMD ["chmod 777 answer"]
# Set working dir as /docker
WORKDIR /docker
ENTRYPOINT ["/bin/bash", "-c"]
