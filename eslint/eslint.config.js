export default [
    {
      files: ["**/*.js"],
      languageOptions: {
        ecmaVersion: "latest",
      },
      rules: {
        semi: ["error", "always"],
        quotes: ["error", "double"],
      },
    },
  ];