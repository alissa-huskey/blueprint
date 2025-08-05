#!/usr/bin/env bats

load 'helper'

@test "bp new php-composer --help" {
  run ${rootdir}/bin/bp new php-composer --help

  assert_success

  assert_output --partial -- '*  VENDOR    TEXT  [required]'
  assert_output --partial -- '*  NAME      TEXT  [required]'

  assert_output --partial -- --dest
  assert_output --partial -- --summary
  assert_output --partial -- --license
  assert_output --partial -- --author
  assert_output --partial -- --phpv
  assert_output --partial -- --php-constraint
  assert_output --partial -- --project-type
}

# bats test_tags=tag:fs
@test "bp new php-composer [OPTIONS] NAME" {
  dest="$TEST_DIR/my-project"

  run bp_y new php-composer      \
    --dest "$TEST_DIR"           \
    --summary "My new project."  \
    --author "Jane Doe"          \
    "acme" "my project"

  assert_success

  assert_dir_exists "${dest}"
  assert_dir_exists "${dest}/src"
  assert_dir_exists "${dest}/tests"
  assert_dir_exists "${dest}/phpcs-rules"
  assert_dir_exists "${dest}/vendor"

  assert_file_exists "${dest}/.env"
  assert_file_exists "${dest}/.ackrc"
  assert_file_exists "${dest}/.editorconfig"
  assert_file_exists "${dest}/.gitignore"
  assert_file_exists "${dest}/composer.json"
  assert_file_exists "${dest}/phpunit.xml"
  assert_file_exists "${dest}/phpcs-rules/ruleset.xml"
  assert_file_exists "${dest}/README.md"
  assert_file_exists "${dest}/src/MyProject.php"
  assert_file_exists "${dest}/tests/MyProjectTest.php"
  assert_file_exists "${dest}/vendor/squizlabs/php_codesniffer/CodeSniffer.conf"

  assert_file_contains "${dest}/.env" 'export PATH="./vendor/bin:${PATH}"'

  assert_file_contains "${dest}/composer.json" '"name": "acme/my-project",'
  assert_file_contains "${dest}/composer.json" '"description": "My new project.",'
  assert_file_contains "${dest}/composer.json" '"version": "0.1.0",'
  assert_file_contains "${dest}/composer.json" '"type": "project",'
  assert_file_contains "${dest}/composer.json" '"license": "MIT",'
  assert_file_contains "${dest}/composer.json" \
    '"authors": \[ { "name": "Jane Doe" } \],'
  assert_file_contains "${dest}/composer.json" '"php": ">=7.3",'
  # assert_file_contains "${dest}/composer.json" '"Acme\\\\MyProject\\\\": "./src/",'
  # assert_file_contains "${dest}/composer.json" '"Acme\\\\MyProject\\\\Tests\\\\": "./tests/",'

  assert_file_contains "${dest}/src/MyProject.php" 'PHP version >=7.3'
  assert_file_contains "${dest}/src/MyProject.php" '@package  Acme_MyProject'
  assert_file_contains "${dest}/src/MyProject.php" '@author   Jane Doe'
  assert_file_contains "${dest}/src/MyProject.php" '@license  MIT'
  assert_file_contains "${dest}/src/MyProject.php" 'namespace Acme\\MyProject;'
  assert_file_contains "${dest}/src/MyProject.php" 'final class MyProject'
  assert_file_contains "${dest}/src/MyProject.php" 'public const VERSION = "0.1.0";'

  assert_file_contains "${dest}/tests/MyProjectTest.php" 'namespace Acme\\MyProject\\Tests;'
  assert_file_contains "${dest}/tests/MyProjectTest.php" 'use Acme\\MyProject\\MyProject;'
  assert_file_contains "${dest}/tests/MyProjectTest.php" 'final class MyProjectTest extends TestCase'
  assert_file_contains "${dest}/tests/MyProjectTest.php" '$app = MyProject();'
  assert_file_contains "${dest}/tests/MyProjectTest.php" '$this->assertSame($app->VERSION, "0.1.0");'
}
