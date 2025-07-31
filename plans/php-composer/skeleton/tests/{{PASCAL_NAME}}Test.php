<?php

namespace {{ VENDOR | to_pascal_case }}\{{ NAME | to_pascal_case }}\Tests;

use {{ VENDOR | to_pascal_case }}\{{ NAME | to_pascal_case }}\{{ NAME | to_pascal_case }};
use PHPUnit\Framework\TestCase;

final class {{ NAME | to_pascal_case }}Test extends TestCase
{
    public function testVersion(): void
    {
        $app = {{ NAME | to_pascal_case }}();
        $this->assertSame($app->VERSION, "{{ VERSION }}");
    }
}
