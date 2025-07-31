#bash

: "${rootdir:="$( cd -P "${BATS_TEST_DIRNAME}/../.." && echo "$PWD" )"}"
bindir="${rootdir}/bin"

for lib in support assert file; do
  load $(brew --prefix bats-$lib)/lib/bats-$lib/load.bash
done

p() {
  while read -r line; do
    printf "# %s\n" "${line}" >&3
  done <<< "${@}"
}

setup() {
  BATSLIB_TEMP_PRESERVE_ON_FAILURE=1

  if [[ "${BATS_TEST_TAGS[*]}" =~ tag:fs ]]; then
    export TEST_DIR="$(temp_make)"
    cd $TEST_DIR || :
  fi
}

teardown() {
  if [[ "${BATS_TEST_TAGS[*]}" =~ tag:fs ]]; then
    temp_del ${TEST_DIR}
  fi

  if [[ "${BATS_TEST_TAGS[*]}" =~ tag:poetry ]]; then
    # needed because poetry fucks up the current venv when running this
    cd "${rootdir}" && poetry update
  fi
}

bats::on_failure() {
  if [[ "${BATS_TEST_TAGS[*]}" =~ tag:fs ]]; then
    p "TEST_DIR: ${TEST_DIR}"
  fi
}

# Run bp with <<< y
# (needed because `run bp ... <<< y` does not work as expected)
bp_y() {
  run ${rootdir}/bin/bp "$@" <<< y
}
