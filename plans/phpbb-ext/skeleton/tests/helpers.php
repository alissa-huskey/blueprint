<?php

/**
 * Test helper file.
 *
 {% include "header.php.jinja" %}
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
