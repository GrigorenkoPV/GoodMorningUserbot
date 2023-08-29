FROM python:3.11-alpine AS base


FROM base AS builder

WORKDIR /tmp/build
RUN pip install --no-cache-dir build

COPY pyproject.toml *.py ./
RUN python -m build --wheel --no-isolation


FROM base AS runner

# Pre-install tgcrypto before copying over the built package,
# because tgcrypto has no aarch64 wheels for musl,
# so you end up having to build it every time.
RUN uname -m | grep 86 || \
    apk add --no-cache gcc musl-dev && \
    pip install --no-cache-dir tgcrypto && \
    apk del gcc musl-dev

COPY --from=builder /tmp/build/dist/*.whl /tmp/
RUN pip install --no-cache-dir /tmp/*.whl && rm /tmp/*.whl

COPY *.session /var/pyrogram/
VOLUME ["/var/pyrogram/"]
ENV PYROGRAM_WORKDIR=/var/pyrogram/

ENTRYPOINT ["goodmorninguserbot"]
STOPSIGNAL SIGINT
