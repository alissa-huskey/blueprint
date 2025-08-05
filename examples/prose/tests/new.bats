#!/usr/bin/env bats

load 'helper'

# bats test_tags=tag:fs
@test "bp new prose [OPTIONS] NAME" {
  dest="$TEST_DIR/paper-lanterns"

  summary="A girl’s wish at a lantern festival sparks a reunion she never saw coming."

  run bp_y new prose --dest "$TEST_DIR" --summary "${summary}" "paper lanterns"

  assert_success

  assert_dir_exists "${dest}"
  assert_dir_exists "${dest}/.git"
  assert_dir_exists "${dest}/drafts"
  assert_dir_exists "${dest}/final"
  assert_dir_exists "${dest}/outline"
  assert_dir_exists "${dest}/research"

  assert_file_exists "${dest}/README.md"
  assert_file_exists "${dest}/drafts/paper-lanterns.md"
  assert_file_exists "${dest}/outline/story-outline.md"
  assert_file_exists "${dest}/research/notes.md"

  assert_file_contains "${dest}/README.md" "# Paper Lanterns"
  assert_file_contains "${dest}/drafts/paper-lanterns.md" "# Paper Lanterns"
  assert_file_contains "${dest}/outline/story-outline.md" "Working title: Paper Lanterns"
  assert_file_contains "${dest}/outline/story-outline.md" "${summary}"
}
