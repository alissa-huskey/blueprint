#!/usr/bin/env bats

load 'helper'

@test "bp new --help" {
  run ${rootdir}/bin/bp --help

  assert_success
}
