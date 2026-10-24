# Contributing

Thanks for contributing! Everyone on this team works with their own AI agent, so we keep the process simple and consistent. AI agents should also follow [`AGENTS.md`](AGENTS.md).

## Getting started

```bash
git clone https://github.com/OxHacks-26/test.git
cd test
```

## Making a change

1. Update `main`: `git checkout main && git pull origin main`
2. Create a branch for your task: `git checkout -b <your-name>/<short-description>`
3. Make your changes in small, focused commits.
4. Before pushing, sync with `main`: `git fetch origin && git rebase origin/main`
5. Push your branch: `git push -u origin <branch-name>`
6. Open a pull request against `main` and fill in the PR template.

## Pull requests

- **Small PRs.** One task per PR. If it's getting big, split it.
- **Never push directly to `main`.** `main` is protected; every change goes through a PR.
- **Reviews.** At least one other teammate must approve before merging. Code owners (see `.github/CODEOWNERS`) are requested automatically.
- **Keep it green.** Make sure tests/builds pass (once we have them) before requesting review.
- **Merge.** Prefer "Squash and merge" to keep `main` history clean. Delete your branch after merging.

## Branch naming

`<your-name>/<short-description>` — e.g. `nidhi/fix-navbar`, `rachel/add-api-route`. Agent-created branches (e.g. `devin/...`) are fine too.

## Commit messages

Short, imperative summary: `Add signup form`, `Fix crash on empty input`.

## Using AI agents

- Point your agent at `AGENTS.md` before it starts working.
- Review what your agent produces before opening the PR — you're responsible for it.
- Never paste secrets or credentials into prompts that end up in commits.
