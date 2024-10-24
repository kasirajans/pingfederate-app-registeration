To enable the "Require approval from code owners" option in your Git repository, you need to configure the CODEOWNERS file and set up branch protection rules. Here's a basic guide:

1. **Create a CODEOWNERS file**:
    Place a file named `CODEOWNERS` in the `.github`, `docs`, or root directory of your repository.

    ```markdown
    # Example of a CODEOWNERS file
    # This sets the code owner for all files in the repository
    * @your-github-username
    ```

2. **Set up branch protection rules**:
    Go to your repository on GitHub, then navigate to `Settings` > `Branches` > `Branch protection rules`.

    - Click on `Add rule`.
    - Specify the branch name pattern (e.g., `main`).
    - Check the box for `Require pull request reviews before merging`.
    - Check the box for `Require review from Code Owners`.

3. **Save the branch protection rule**.

This will ensure that any changes to the specified branch require approval from the code owners listed in the `CODEOWNERS` file.

For more detailed information, refer to the [GitHub documentation on CODEOWNERS](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-code-owners).
