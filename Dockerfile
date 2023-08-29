FROM python:3.11-alpine AS base


FROM base AS builder

WORKDIR /tmp/build
RUN pip install --no-cache-dir build

COPY pyproject.toml *.py ./
RUN python -m build --wheel --no-isolation


FROM base AS runner

COPY --from=builder /tmp/build/dist/*.whl /tmp/
RUN apk add --no-cache gcc musl-dev && \
    pip install --no-cache-dir /tmp/*.whl && \
    rm /tmp/*.whl && \
    apk del gcc musl-dev

COPY *.session /var/pyrogram/
VOLUME ["/var/pyrogram/"]
ENV PYROGRAM_WORKDIR=/var/pyrogram/

ENTRYPOINT ["goodmorninguserbot"]
STOPSIGNAL SIGINT
