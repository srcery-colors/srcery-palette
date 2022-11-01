Srcery palette
==============

Srcery palette, hopefully we can move more and more projects over to reading
from this repo. Not quite there yet though.

You can clone and use the JSON here for whatever, or you can use the npm
package, that simply exports the palette to js object.



## Package

To install package go
[here](https://github.com/srcery-colors/srcery-palette/pkgs/npm/srcery-palette)
and follow instructions.

To install said package you need to authenticate with Github packages even
though the package is public, just setup a personal access token with package
read permissions, and save it to `~/.npmrc` if you haven't done so already.

- [Authenticating to github packages - GitHub Docs](https://docs.github.com/en/packages/learn-github-packages/introduction-to-github-packages#authenticating-to-github-packages)
- [Installing a package - GitHub Docs](https://docs.github.com/en/packages/learn-github-packages/installing-a-package)

You also need to tell `npm` about this registry (srcery-colors), create an
`.npmrc` file in project root and copy paste this:

```
@srcery-colors:registry=https://npm.pkg.github.com/
```

Then you should be all good to run `npm install`
