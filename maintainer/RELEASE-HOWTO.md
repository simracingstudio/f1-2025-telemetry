Step-by-step release procedure
==============================

1. Bump the version number with `bump2version <part>`

    Example: `bump2version minor` to go from `x.y.z` to `x.y+1.0`

    See `.bumpversion.cfg` and [bump2version](https://github.com/c4urself/bump2version)'s documentation for more help.

2. Verify that a local build of the documentation succeeds, by running `maintainer/make-docs.sh`.

3. Double-check that the previous version number isn't found in the project directories.

4. Push the commit and tag created by bump2version

   Merge upstream's master into the stable branch.

5. Go to Read the Docs and trigger a rebuild of the documentation.

   If this fails, fix the problem and go back to step 2.

6. Run `maintainer/make-dist.sh` to create the Python distribution.

7. Run `maintainer/upload-dist.sh` to upload it to PyPi.
