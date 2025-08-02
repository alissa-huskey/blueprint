#!/usr/bin/env bats

load 'helper'

@test "bp new basic --help" {
  run ${rootdir}/bin/bp new basic --help

  assert_success
  assert_output --partial -- --dest
  assert_output --partial -- --summary
  assert_output --partial -- --license
}

# bats test_tags=tag:fs
@test "bp new basic [OPTIONS] NAME" {
  dest="$TEST_DIR/my-project"
  run bp_y new basic --dest "$TEST_DIR" --summary "My new project." "my project"

  assert_success

  assert_dir_exists "${dest}"
  assert_dir_exists "${dest}/.git"
  assert_dir_exists "${dest}/.todo"

  assert_file_exists "${dest}/README.md"
  assert_file_exists "${dest}/CHANGELOG.md"
  assert_file_exists "${dest}/.git/description"

  assert_file_contains "${dest}/README.md" "^# My Project$"
  assert_file_contains "${dest}/README.md" "^> My new project.$"
  assert_file_contains "${dest}/.git/description" "My Project: My new project."
}
