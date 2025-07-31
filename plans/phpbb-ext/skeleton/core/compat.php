<?php

/**
 * PHP 7-to-8 Compatibility
 *
 * PHP version {{ PHP_CONSTRAINT }}
 *
 * @category Phpbb
 * @package  PhpBB_{{ VENDOR | to_pascal_case }}_{{ NAME | to_pascal_case }}
 * @author   {{ AUTHOR }}
 * @license  http://opensource.org/licenses/gpl-2.0.php GNU General Public License v2
 */

if (!function_exists("str_contains")) {
    /**
     * Determine if a string contains a given substring.
     *
     * @param string $haystack String to search in
     * @param string $needle   Substring to search for
     *
     * @return bool
     */
    function str_contains(string $haystack, string $needle): bool
    {
        return $needle !== '' && mb_strpos($haystack, $needle) !== false;
    }
}
/**
 * Check if all array_elements satisfy a callback function.
 *
 * @param array    $array    Array to check
 * @param callback $callback Callback to check with, signature must be:
 *                           callback(mixed $value, mixed $key): bool
 *
 * @return bool
 */
if (!function_exists("array_all")) {
    function array_all(array $array, callable $callback): bool
    {
        foreach ($array as $key => $value) {
            if (!$callback($value, $key)) {
                return false;
            }
        }
        return true;
    }
}
