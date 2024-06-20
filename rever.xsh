# Check that we are on the master branch
branch=$(git branch --show-current)
if branch.strip() != "master":
  raise Exception("You must be on the master branch to release.")
git diff --exit-code
git diff --cached --exit-code

$PROJECT = 'ipyvue-flatsurf'

$ACTIVITIES = [
    'version_bump',
    'changelog',
    'tag',
    'push_tag',
    'pypi',
    'ghrelease'
]

$VERSION_BUMP_PATTERNS = [
    ('ipyvue_flatsurf/__init__.py', r'__version__ = ', r'__version__ = "$VERSION"'),
    ('ipyvue_flatsurf/__init__.py', r'version_info =', f'version_info = ' + str(tuple(int(x) for x in $VERSION.split(".")))),
    ('setup.py', r'    version=', r'    version="$VERSION",'),
    ('README.md', r'\[!\[Binder\]\(https://mybinder.org/badge_logo.svg\)\]\(https://mybinder.org/v2/gh/flatsurf/ipyvue-flatsurf/', r'[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/flatsurf/ipyvue-flatsurf/$VERSION?filepath=%2Fexamples)'),
    ('binder/environment.yml', '    - ipyvue-flatsurf==', '    - ipyvue-flatsurf==$VERSION'),
]

$CHANGELOG_FILENAME = 'ChangeLog'
$CHANGELOG_TEMPLATE = 'TEMPLATE.rst'
$CHANGELOG_NEWS = 'news'
$CHANGELOG_CATEGORIES = ('Added', 'Changed', 'Removed', 'Fixed')
$PUSH_TAG_REMOTE = 'git@github.com:flatsurf/ipyvue-flatsurf.git'

$PYPI_BUILD_COMMANDS = ['sdist', 'bdist_wheel']

$GITHUB_ORG = 'flatsurf'
$GITHUB_REPO = 'ipyvue-flatsurf'
