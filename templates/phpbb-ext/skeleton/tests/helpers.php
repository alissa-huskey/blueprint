<?php

/**
 * Test helper file.
 *
 * PHP version ${PHP_CONSTRAINT}
 *
 * @category Phpbb
 * @package  PhpBB_${VENDOR}_${PASCAL_NAME}_Tests
 * @author   ${AUTHOR}
 * @license  http://opensource.org/licenses/gpl-2.0.php GNU General Public License v2
 */

/**
 * Print a horizontal line to stdout.
 *
 * @return null
 */
function hr(): void
{
    print "\n=======================================\n";
}

/**
 * Print a message to stdout.
 */
function out(...$msg): void
{
    $text = join(" ", $msg);
    print "\n[logger] $text\n\n";
}

/**
 * Print a message to stderr.
 */
function err(...$msg): void
{
    $text = join(" ", $msg);
    fwrite(STDERR, "\n[logger] ERROR $text\n\n");
}
