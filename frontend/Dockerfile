# Estágio de build
FROM node:18-alpine as builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Estágio de produção (servir com Nginx)
FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
# Opcional: Copiar config do Nginx se precisar de proxy_pass para a API
# COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
