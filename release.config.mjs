/** @type {import('semantic-release').GlobalConfig} */
export default {
  branches: ["main"],
  // biome-ignore lint/suspicious/noTemplateCurlyInString: semantic-release template
  tagFormat: "v${version}",
  plugins: [
    ["@semantic-release/commit-analyzer", { preset: "conventionalcommits" }],
    [
      "@semantic-release/release-notes-generator",
      { preset: "conventionalcommits" },
    ],
    [
      "@semantic-release/exec",
      {
        // biome-ignore lint/suspicious/noTemplateCurlyInString: semantic-release template
        prepareCmd: "pnpm version ${nextRelease.version} --no-git-tag-version",
        successCmd:
          // biome-ignore lint/suspicious/noTemplateCurlyInString: semantic-release template
          'gh workflow run publish.yaml --ref "${nextRelease.gitTag}"',
      },
    ],
    ["@semantic-release/changelog", { changelogTitle: "# Changelog" }],
    [
      "@semantic-release/git",
      {
        assets: ["package.json", "CHANGELOG.md"],
        // biome-ignore lint/suspicious/noTemplateCurlyInString: semantic-release template
        message: "chore(release): ${nextRelease.version} [skip ci]",
      },
    ],
    [
      "@semantic-release/github",
      {
        draftRelease: true,
        failComment: false,
        failTitle: false,
        labels: false,
        releasedLabels: false,
        successComment: false,
      },
    ],
  ],
};
