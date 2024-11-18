FROM python:3.12-slim


WORKDIR /jup

RUN pip install jupyter -U && pip install jupyterlab

EXPOSE 1010

ENTRYPOINT ["jupyter", "lab","--ip=0.0.0.0","--allow-root"]