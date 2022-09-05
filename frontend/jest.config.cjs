module.exports = {
  verbose: true,
  setupFiles: [
    "./jest.environment.js"
  ],
  collectCoverage: true,
  collectCoverageFrom: ["./src/models/*", "./src/presenters/*", "./src/utils.ts", "./src/models.ts"]
};