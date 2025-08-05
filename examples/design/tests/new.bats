#!/usr/bin/env bats

load 'helper'

@test "bp new design --help" {
  run ${rootdir}/bin/bp new design --help

  assert_success
  assert_output --partial -- --dest
  assert_output --partial -- --summary
  assert_output --partial -- --license
  assert_output --partial -- --author
}

# bats test_tags=tag:fs
@test "bp new design [OPTIONS] NAME" {
  dest="$TEST_DIR/my-project"
  run bp_y new design --dest "$TEST_DIR" --summary "My new project." "my project"

  assert_success

  assert_dir_exists "${dest}"
  assert_dir_exists "${dest}/.git"
  assert_dir_exists "${dest}/.todo"
  assert_dir_exists "${dest}/assets"
  assert_dir_exists "${dest}/designs"
  assert_dir_exists "${dest}/docs"

  assert_file_exists "${dest}/README.md"
  assert_file_exists "${dest}/docs/requirements.md"
}
