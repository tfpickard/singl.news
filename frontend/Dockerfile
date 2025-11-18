FROM node:20-slim AS build
WORKDIR /app
COPY frontend/package*.json ./
RUN npm install
COPY frontend ./
RUN npm run build

FROM node:20-slim
WORKDIR /app
COPY --from=build /app/build ./build
RUN npm install -g serve
EXPOSE 4173
CMD ["serve", "-s", "build", "-l", "4173"]
