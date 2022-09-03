module.exports = {
  collectCoverage: true,
  verbose: true,
  setupFiles: [
    "./jest.environment.js"
  ],
  collectCoverageFrom: ["./src/models/*", "./src/presenters/*", "./src/utils.ts", "./src/models.ts"]
};