#!/usr/bin/env bats

load 'helper'

@test "bp new phpbb-ext --help" {
  run ${rootdir}/bin/bp new phpbb-ext --help

  assert_success

  assert_output --partial -- '*  VENDOR    TEXT  [required]'
  assert_output --partial -- '*  NAME      TEXT  [required]'

  assert_output --partial -- --dest
  assert_output --partial -- --summary
  assert_output --partial -- --license

  assert_output --partial -- --phpv
  assert_output --partial -- --php-constraint
}

# bats test_tags=tag:fs
@test "bp new phpbb-ext [OPTIONS] NAME" {
  dest="$TEST_DIR/phpbb-my-project"

  run bp_y new phpbb-ext     \
    --dest "$TEST_DIR"           \
    --summary "My new project."  \
    "acme" "my project"

  assert_success

  assert_dir_exists "${dest}"
  assert_dir_exists "${dest}/core"
  assert_dir_exists "${dest}/tests"
  assert_dir_exists "${dest}/phpcs-rules"
  # assert_dir_exists "${dest}/vendor"

  assert_file_exists "${dest}/.ackrc"
  assert_file_exists "${dest}/.editorconfig"
  assert_file_exists "${dest}/.gitignore"
  assert_file_exists "${dest}/composer.json"
  assert_file_exists "${dest}/phpunit.xml"
  assert_file_exists "${dest}/phpcs-rules/ruleset.xml"
  assert_file_exists "${dest}/README.md"
  assert_file_exists "${dest}/core/compat.php"
  # assert_file_exists "${dest}/vendor/squizlabs/php_codesniffer/CodeSniffer.conf"

  assert_file_contains "${dest}/composer.json" '"name": "acme/myproject",'
  assert_file_contains "${dest}/composer.json" '"description": "My new project.",'
  assert_file_contains "${dest}/composer.json" '"version": "0.1.0",'
  assert_file_contains "${dest}/composer.json" '"type": "phpbb-extension",'
  assert_file_contains "${dest}/composer.json" '"authors": \[ { "name": "" } \],'
  assert_file_contains "${dest}/composer.json" '"php": ">=7.3",'
  # assert_file_contains "${dest}/composer.json" '"acme\\\\myproject\\\\": "./src/",'
  # assert_file_contains "${dest}/composer.json" '"acme\\\\myproject\\\\tests\\\\": "./tests/",'

  assert_file_contains "${dest}/core/compat.php" 'PHP version >=7.3'
  assert_file_contains "${dest}/core/compat.php" '@package [ ]*PhpBB_Acme_MyProject'
  # assert_file_contains "${dest}/core/compat.php" '@author [ ]*{{ AUTHOR }}'
  assert_file_contains "${dest}/core/compat.php" '@license [ ]*http://opensource.org/licenses/gpl-2.0.php GNU General Public License v2'

  # assert_file_contains "${dest}/tests/TestMyProject.php" 'namespace Acme\MyProject\Tests;'
  # assert_file_contains "${dest}/tests/TestMyProject.php" 'use Acme\MyProject\MyProject;'
  # assert_file_contains "${dest}/tests/TestMyProject.php" 'final class TestMyProject extends TestCase'
  # assert_file_contains "${dest}/tests/TestMyProject.php" '$app = {{ PASCAL_NAME }}();'
  # assert_file_contains "${dest}/tests/TestMyProject.php" '$this->assertSame($app->VERSION, "0.1.0");'
}
