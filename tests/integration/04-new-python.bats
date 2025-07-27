#!/usr/bin/env bats

load 'helper'

skip

@test "bp new python --help" {
  run ${rootdir}/bin/bp new python --help

  assert_success
  assert_output --partial -- --dest
  assert_output --partial -- --summary
  assert_output --partial -- --license
  assert_output --partial -- --pyv
  assert_output --partial -- --pyv-constraint
}

# bats test_tags=tag:poetry, tag:fs
@test "bp new python [OPTIONS] NAME" {
  dest="$TEST_DIR/my-project"

  run bp_y new python            \
    --dest "$TEST_DIR"           \
    --summary "My new project."  \
    --pyv 3.10.2                 \
    --pyv-constraint ">=3.10.2"  \
    "my project"

  assert_success

  assert_dir_exists "${dest}"
  assert_dir_exists "${dest}/my_project"
  assert_dir_exists "${dest}/tests"

  assert_file_exists "${dest}/.env"
  assert_file_exists "${dest}/.python-version"
  assert_file_exists "${dest}/README.md"
  assert_file_exists "${dest}/pyproject.toml"
  assert_file_exists "${dest}/setup.cfg"
  assert_file_exists "${dest}/my_project/__init__.py"
  assert_file_exists "${dest}/tests/__init__.py"
  assert_file_exists "${dest}/tests/test_my_project.py"

  assert_file_contains "${dest}/pyproject.toml" '^name = "my-project"$'
  assert_file_contains "${dest}/pyproject.toml" '^version = "0.0.1"$'
  assert_file_contains "${dest}/pyproject.toml" '^description = "My new project."$'
  assert_file_contains "${dest}/pyproject.toml" '^license = "MIT"$'
  assert_file_contains "${dest}/pyproject.toml" '^python = ">=3.10.2"$'

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

  assert_file_contains "${dest}/.python-version" "3.10.2"
}
