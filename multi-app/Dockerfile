FROM openfabric/tee-python-gpu:experimental
COPY . .
ENV CODE_PASSWORD=dev

COPY pyproject.toml poetry.lock ./

RUN python3 -m pip install --upgrade pip && \
    python3 -m pip install --upgrade poetry && \
    python3 -m pip uninstall --yes openfabric-pysdk && \
    python3 -m pip install --no-cache-dir --extra-index-url https://repo.node2.openfabric.network/index openfabric-pysdk==0.2.9 && \
    python3 -m poetry install --only main && \
    rm -rf ~/.cache/pypoetry/{cache,artifacts}




RUN poetry install -vvv --no-dev



EXPOSE  5000

CMD ["sh","start.sh"]