from app.models import Layout

layoutQwerty = Layout(name='Qwerty', mods=[
    {
        'name': 'lowercase',
        'keys': [
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
            ['q', 'w', 'e', 'r', 't', 'y', 'u', 'i', 'o', 'p', '[', ']', '\\'],
            ['a', 's', 'd', 'f', 'g', 'h', 'j', 'k', 'l', ';', '\'', Layout.KEY_ENTER],
            ['z', 'x', 'c', 'v', 'b', 'n', 'm', ', ', '.', '/', Layout.KEY_SHIFT],
            [Layout.KEY_SPACE]
        ]
    },
    {
        'name': 'uppercase',
        'keys': [
            ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'],
            ['Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '{', '}', '|'],
            ['A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ':', '"', Layout.KEY_ENTER],
            ['Z', 'X', 'C', 'V', 'B', 'N', 'M', '<', '>', '?', Layout.KEY_SHIFT],
            [Layout.KEY_SPACE]
        ]
    }
])

layoutColemak = Layout(name='Colemak', mods=[
    {
        'name': 'lowercase',
        'keys': [
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
            ['q', 'w', 'f', 'p', 'g', 'j', 'l', 'u', 'y', ';', '[', ']', '\\'],
            ['a', 'r', 's', 't', 'd', 'h', 'n', 'e', 'i', 'o', '\'',  Layout.KEY_ENTER],
            ['z', 'x', 'c', 'v', 'b', 'k', 'm', ', ', '.', '/',  Layout.KEY_SHIFT],
            [Layout.KEY_SPACE]
        ]
    },
    {
        'name': 'uppercase',
        'keys': [
            ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'],
            ['Q', 'W', 'F', 'P', 'G', 'J', 'L', 'U', 'Y', ':', '{', '}', '|'],
            ['A', 'R', 'S', 'T', 'D', 'H', 'N', 'E', 'I', 'O', '"', Layout.KEY_ENTER],
            ['Z', 'X', 'C', 'V', 'B', 'K', 'M', '<', '>', '?', Layout.KEY_SHIFT],
            [Layout.KEY_SPACE]
        ]
    }
])

layoutDworak = Layout(name='Dworak', mods=[
    {
        'name': 'lowercase',
        'keys': [
            ['`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '='],
            ['\'', ', ', '.', 'p', 'y', 'f', 'g', 'c', 'r', 'l', '/', '=', '\\'],
            ['a', 'o', 'e', 'u', 'i', 'd', 'h', 't', 'n', 's', '-', Layout.KEY_ENTER],
            [';', 'q', 'j', 'k', 'x', 'b', 'm', 'w', 'v', 'z', Layout.KEY_SHIFT],
            [Layout.KEY_SPACE]
        ]
    },
    {
        'name': 'uppercase',
        'keys': [
            ['~', '!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+'],
            ['"', '<', '>', 'P', 'Y', 'F', 'G', 'C', 'R', 'L', '?', '+', '|'],
            ['A', 'O', 'E', 'U', 'I', 'D', 'H', 'T', 'N', 'S', '_', Layout.KEY_ENTER],
            [':', 'Q', 'J', 'K', 'X', 'B', 'M', 'W', 'V', 'Z', Layout.KEY_SHIFT],
            [Layout.KEY_SPACE]
        ]
    }
])