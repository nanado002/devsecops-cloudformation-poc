FROM nginxinc/nginx-unprivileged:1.31-alpine

# Temporarily become root to upgrade OS packages for security patches,
# then switch back to the non-root nginx user for runtime.
USER root
RUN apk upgrade --no-cache
USER nginx

COPY nginx.conf /etc/nginx/conf.d/default.conf
COPY index.html /usr/share/nginx/html/index.html

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD wget -qO- http://127.0.0.1:8080/ >/dev/null || exit 1
