<?php

/**
 * Test bootstrap file.
 *
 {% include "header.php.jinja" %}
 */

// ignore deprecation warnings from vendor code
error_reporting(E_ALL & ~E_DEPRECATED);

const TEST_ROOT = __DIR__;

require_once(TEST_ROOT . DIRECTORY_SEPERATOR . "helpers.php");
