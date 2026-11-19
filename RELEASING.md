# Releasing

Successful CI on `main` runs semantic-release. It determines the version,
updates `package.json` with native `pnpm version`, generates `CHANGELOG.md`,
and commits both files before creating a `vX.Y.Z` tag and a draft GitHub
release. It then starts `publish.yaml` at the new tag, which stages the
package on npm. A maintainer approves the staged version on npmjs.com before
it goes live.

The Conventional Commits preset determines releases from commit messages:

| Message | Release |
| --- | --- |
| `fix(palette): correct bright black` | Patch |
| `perf: simplify the CSS build` | Patch |
| `feat(palette): add a new color` | Minor |
| A commit with a `BREAKING CHANGE:` footer | Major |
| `chore`, `ci`, `docs`, `build`, `refactor`, `style`, or `test` | None, unless breaking |

Use a descriptive Conventional Commits PR title and squash merge it. The
repository uses the PR title as the squash commit title, so the PR title is
what semantic-release reads. Both `feat!:` and a `BREAKING CHANGE:` footer
declare a breaking change; keep the marker in the squashed commit.

Do not manually edit new changelog sections or bump the version. Release notes
come from the merged commits. Release commits use `[skip ci]` to avoid loops.

## Publication

The `release` job in `ci.yaml` runs semantic-release with a token for the
srcery-colors GitHub App (Contents and Actions write). It pushes the release
commit and tag, creates the draft release, and uses the exec plugin's
`successCmd` to dispatch `publish.yaml` at the new tag. `publish.yaml` is the
tag run only.

`publish.yaml` has three jobs:

1. `verify` checks that the tag has the form `vX.Y.Z`, matches
   `package.json`, and is on `main`. It then reads the public npm registry
   to see whether the version is live, and the GitHub release to see whether
   it is still a draft. It reads the registry with `curl` because
   `devEngines` requires pnpm, so `npm view` refuses to run in the checkout.
2. `publish` runs only when the version is not live. It waits for approval of
   the `publish` environment, runs `pnpm build` to generate `srcery.css`, and
   runs `pnpm stage publish` with npm trusted publishing (OIDC). The version
   is now staged: it is not installable until a maintainer approves it.
3. `release` waits for the version to go live, checking the registry every 30
   seconds for up to 2 hours, then publishes the GitHub release. The GitHub
   release therefore never goes public before npm has the version.

To finish a release:

1. Approve the `publish` environment on the workflow run.
2. Approve the staged version on npmjs.com, under **Staged Packages** in your
   account settings, with 2FA. Do this within 2 hours to let `release` finish
   on its own.

The trusted publisher only accepts staged publishes, so the workflow can never
make a version live by itself. Approving needs an interactive login with 2FA;
OIDC tokens cannot approve, list or reject staged versions. See npm's
[staged publishing](https://docs.npmjs.com/staged-publishing/) and
[`npm stage`](https://docs.npmjs.com/cli/v12/commands/npm-stage/) docs.

`verify` needs `contents: write` to read draft releases but installs no
dependencies. `publish` has `contents: read` and `id-token: write` for trusted
publishing, which also signs npm provenance. `release` has `contents: write`
to publish the draft.

The CI `release` job and `publish.yaml` set `cache-mode: none`, and their
pnpm setup steps set `cache: false`, so release jobs neither restore nor save
any cache. Ordinary CI keeps its cache.

## Retry a failed publication

Dispatch the workflow at the existing tag, without running another release:

```sh
gh workflow run publish.yaml --ref vX.Y.Z
```

It skips whatever is already done:

| State | What runs |
| --- | --- |
| Not staged (dispatch failed, approval rejected, or staging failed) | `publish`, then `release` waits |
| Staged, still waiting for approval on npm | `publish` fails, because npm won't stage a version that is already staged. Approve it on npmjs.com, then run the workflow again |
| Live on npm, GitHub release still a draft | `release` only |
| Live on npm, GitHub release published | Nothing |

If `release` times out, approve the version on npmjs.com, wait 5 minutes for
the registry cache, then run the workflow again. If the staged version was
rejected, release a new version instead: rejecting removes it permanently.

If the CI `release` job failed after pushing the release commit but before
creating the tag or draft, complete those missing steps from that exact
commit. Use its package version and generated changelog notes; avoid
rerunning the `release` job and duplicating the changelog entry. To recreate
a missing draft for an existing tag:

```sh
gh release create vX.Y.Z --draft --verify-tag --title vX.Y.Z --notes-file release-notes.md
gh workflow run publish.yaml --ref vX.Y.Z
```

Populate `release-notes.md` with that version's generated changelog section.
Do not delete published release tags.

## Setup

One-off setup, already done; recreate it if the repository or the npm
package settings are replaced:

- GitHub environment `publish`, limited to `v*` tags, with required
  reviewers and a 5-minute wait timer.
- An npm trusted publisher for this repository's `publish.yaml`, set to
  accept staged publishes only.
- GitHub environment `release`, limited to `main`, with the variable
  `RELEASE_APP_CLIENT_ID` and the secret `RELEASE_APP_PRIVATE_KEY` of the
  srcery-colors App. Only the CI `release` job uses them.
- The srcery-colors App, with Contents and Actions write. Its key can create
  a token for any repository the App is installed on, so treat the key as
  covering all of them. It is the only bypass actor on the default branch
  ruleset, so it can push release commits to `main`.

To rotate the key, generate a new private key in the App's settings, replace
the `RELEASE_APP_PRIVATE_KEY` secret, then delete the old key.

## Validate locally

Use the declared Node runtime and the pnpm version recorded in the lockfile:

```sh
pnpm install --frozen-lockfile
pnpm release --dry-run
```

Dry runs analyze commits and generate notes without updating files, creating
commits, tags or releases, or dispatching publication. Authentication and a
current checkout of `main` may be required to verify remote access.
