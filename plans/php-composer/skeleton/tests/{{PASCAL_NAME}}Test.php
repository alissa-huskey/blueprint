<?php

namespace {{ VENDOR | to_pascal_case }}\{{ NAME | to_pascal_case }}\Tests;

use {{ VENDOR | to_pascal_case }}\{{ NAME | to_pascal_case }}\{{ NAME | to_pascal_case }};
use PHPUnit\Framework\TestCase;

final class Test{{ NAME | to_pascal_case }} extends TestCase
{
    public function testVersion(): void
    {
        $app = {{ NAME | to_pascal_case }}();
        $this->assertSame($app->VERSION, "{{ VERSION }}");
    }
}
