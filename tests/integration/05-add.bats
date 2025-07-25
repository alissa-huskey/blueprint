#!/usr/bin/env bats

load 'helper'

@test "bp add --help" {
  run ${rootdir}/bin/bp add --help

  assert_success

  assert_output --partial "python"
}

@test "bp add python --help" {
  run ${rootdir}/bin/bp add python --help

  assert_success

  assert_output --partial "deps"
}
