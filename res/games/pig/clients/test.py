#!/usr/bin/env python
# -*- coding: utf-8 -*-

basic_console = """
{% macro display_one(player) %}
    {% for entry in varargs %}
        {% set result = player %}
        {% for field in entry %}
            {% set result = result[field] %}
        {% endfor %}
        {{ result }}
    {% endfor %}
{% endmacro %}

{% macro display_all() %}
    {% for player in data.players.list %}
        {{ display_one(player, *varargs) }}
    {% endfor %}
{% endmacro %}

{% macro display_current() %}
    {{ display_one(data.players.current, *varargs) }}
{% endmacro %}
"""

import jinja2

test = """
{{ diceroll(name, roll) }}
"""

jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('.'),
        extensions=['jinja2.ext.i18n'])
jinja_env.install_null_translations()
with open('basic_console.jinja2') as f:
    content = f.read()
#game = jinja_env.get_template('basic_console.jinja2')
#rules = jinja_env.from_string(basic_console)
a = jinja_env.from_string(basic_console + content + test)
result = a.render(name="Wezegege", roll=5)
result = '\n'.join([entry for entry in result.split('\n') if entry])
print(result)
