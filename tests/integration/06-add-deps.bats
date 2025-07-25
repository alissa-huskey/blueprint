#!/usr/bin/env bats

load 'helper'

@test "bp add python deps --help" {
  run ${rootdir}/bin/bp add python deps --help

  assert_success

  assert_output --partial "dest"
}

# bats test_tags=tag:poetry, tag:fs
@test "bp add python deps" {
  poetry new my-project

  dest="${TEST_DIR}/my-project"

  run ${rootdir}/bin/bp add python deps "${dest}"

  assert_success

  assert_file_contains "${dest}/pyproject.toml" '^black = "[*]"$'
  assert_file_contains "${dest}/pyproject.toml" '^flake8 = "[*]"$'
  assert_file_contains "${dest}/pyproject.toml" '^flake8-black = "[*]"$'
  assert_file_contains "${dest}/pyproject.toml" '^flake8-docstrings = "[*]"$'
  assert_file_contains "${dest}/pyproject.toml" '^flake8-isort = "[*]"$'
  assert_file_contains "${dest}/pyproject.toml" '^ipython = "[*]"$'
  assert_file_contains "${dest}/pyproject.toml" '^isort = "[*]"$'
  assert_file_contains "${dest}/pyproject.toml" '^pdbpp = "[*]"$'
  assert_file_contains "${dest}/pyproject.toml" '^pycodestyle = "[*]"$'
  assert_file_contains "${dest}/pyproject.toml" '^pylama = "[*]"$'
  assert_file_contains "${dest}/pyproject.toml" '^pynvim = "[*]"$'
  assert_file_contains "${dest}/pyproject.toml" '^pylint = "[*]"$'
}
