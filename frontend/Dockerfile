FROM node:22-alpine

WORKDIR /app

RUN addgroup -S -g 1000 app && \
    adduser -S -u 1000 -G app app

RUN corepack enable && corepack prepare pnpm@latest --activate

COPY package.json pnpm-lock.yaml ./
ENV CI=true
RUN pnpm install

COPY . .

RUN chown -R app:app /app

USER app

EXPOSE 3000

CMD ["pnpm", "dev", "--host", "0.0.0.0"]
