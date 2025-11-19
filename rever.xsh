# ********************************************************************
#  This file is part of ipyvue-flatsurf.
#
#        Copyright (C) 2025 Julian Rüth
#
#  ipyvue-flatsurf is free software: you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the Free
#  Software Foundation, either version 3 of the License, or (at your option)
#  any later version.
#
#  ipyvue-flatsurf is distributed in the hope that it will be useful, but
#  WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
#  or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for
#  more details.
#
#  You should have received a copy of the GNU General Public License along with
#  ipyvue-flatsurf. If not, see <https://www.gnu.org/licenses/>.
# ********************************************************************

# Check that we are on the master branch
branch=$(git branch --show-current)
if branch.strip() != "master":
  raise Exception("You must be on the master branch to release.")
git diff --exit-code
git diff --cached --exit-code

from rever.activities.command import command

command('build', 'python -m build')
command('twine', 'twine upload dist/*')

$PROJECT = 'ipyvue-flatsurf'

$ACTIVITIES = [
    'version_bump',
    'changelog',
    'build',
    'twine',
    'tag',
    'push_tag',
    'ghrelease'
]

$VERSION_BUMP_PATTERNS = [
    ('ipyvue_flatsurf/__init__.py', r'__version__ = ', r'__version__ = "$VERSION"'),
    ('ipyvue_flatsurf/__init__.py', r'version_info =', f'version_info = ' + str(tuple(int(x) for x in $VERSION.split(".")))),
    ('pyproject.toml', r'version = ', r'version = "$VERSION"'),
]

$CHANGELOG_FILENAME = 'ChangeLog'
$CHANGELOG_TEMPLATE = 'TEMPLATE.rst'
$CHANGELOG_NEWS = 'news'
$CHANGELOG_CATEGORIES = ('Added', 'Changed', 'Removed', 'Fixed')
$PUSH_TAG_REMOTE = 'git@github.com:flatsurf/ipyvue-flatsurf.git'

$GITHUB_ORG = 'flatsurf'
$GITHUB_REPO = 'ipyvue-flatsurf'
