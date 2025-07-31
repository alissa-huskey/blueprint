<?php

/**
 * Test bootstrap file.
 *
 * PHP version {{ PHP_CONSTRAINT }}
 *
 * @category Phpbb
 * @package  PhpBB_{{ VENDOR | to_pascal_case }}_{{ NAME | to_pascal_case }}_Tests
 * @author   {{ AUTHOR }}
 * @license  http://opensource.org/licenses/gpl-2.0.php GNU General Public License v2
 */

// ignore deprecation warnings from vendor code
error_reporting(E_ALL & ~E_DEPRECATED);

const TEST_ROOT = __DIR__;

require_once(TEST_ROOT . DIRECTORY_SEPERATOR . "helpers.php");
