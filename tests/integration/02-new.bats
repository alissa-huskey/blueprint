#!/usr/bin/env bats

load 'helper'

@test "bp new --help" {
  run ${rootdir}/bin/bp new --help

  assert_success
  assert_output --partial "basic"
  assert_output --partial "python"
}

@test "bp new python-poetry --help" {
  run ${rootdir}/bin/bp new python-poetry --help

  assert_success
  assert_output --partial -- --dest
  assert_output --partial -- --summary
  assert_output --partial -- --license
  assert_output --partial -- --pyv
  assert_output --partial -- --pyv-constraint
}
