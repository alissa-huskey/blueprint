#!/usr/bin/env bats

load 'helper'

@test "[error: missing args] scripts/setup-art-dir" {
  run ${rootdir}/plans/design/scripts/setup-art-dir

  assert_failure
}

@test "[error: invalid sw arg] scripts/setup-art-dir PATH SOFTWARE" {
  run ${rootdir}/plans/design/scripts/setup-art-dir "${TEST_DIR}" xxx

  assert_failure
}

# bats test_tags=tag:fs
@test "[error: base path is not a dir] scripts/setup-art-dir PATH SOFTWARE" {
  run ${rootdir}/plans/design/scripts/setup-art-dir xxx illustrator

  assert_failure
}

# bats test_tags=tag:fs
@test "[error: dir already exists] scripts/setup-art-dir PATH SOFTWARE" {
  mkdir "${TEST_DIR}/models"

  run ${rootdir}/plans/design/scripts/setup-art-dir ${TEST_DIR} sketchup

  assert_failure
}

# bats test_tags=tag:fs
@test "[success] scripts/setup-art-dir PATH SOFTWARE" {
  run ${rootdir}/plans/design/scripts/setup-art-dir "${TEST_DIR}" sketchup

  assert_success
  assert_dir_exists "$TEST_DIR/models"
}
