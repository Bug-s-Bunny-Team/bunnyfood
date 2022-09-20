module.exports = {
  testEnvironment: 'jsdom',
  verbose: true,
  setupFiles: [
    "./jest.environment.js"
  ],
  transform: {
    '^.+\\.svelte$': ['svelte-jester', {preprocess: true}],
    '^.+\\.(ts|js)$': 'babel-jest',
  },
  moduleFileExtensions: ['js', 'ts', 'svelte'],
  transformIgnorePatterns: ["node_modules/(?!(svelte-star-rating)/)"],
  collectCoverage: true,
  collectCoverageFrom: ['./src/models/*', './src/presenters/*', './src/utils.ts', './src/models.ts']
};
