# frontend

## Prerequisiti
- [Node](https://nodejs.org/) e npm
- Installare le librerie necessarie:
  ```sh
  npm install
  ```

## Comandi utili
- Avvio server di sviluppo:
  ```sh
  npm run dev
  ```

- Build:
  ```sh
  npm run build
  ```

- Deploy:
  ```sh
  aws s3 rm s3://swe-bucket-bugsbunny-frontend --recursive    # rimuove versione precedente
  aws s3 cp dist/ s3://swe-bucket-bugsbunny-frontend --recursive
  ```
