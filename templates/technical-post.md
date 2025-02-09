---
layout: post
title: {{ title }}
date: {{ date }}
author: {{ author }}
categories: [{{ tags|join(", ") }}]
---

{{ description }}

{% if introduction %}
## Introduction
{{ introduction }}
{% endif %}

{% if code_example %}
## Code Example
```{{ language }}
{{ code_example }}
```
{% endif %}

{% if explanation %}
## Understanding the Code
{{ explanation }}
{% endif %}

{% if conclusion %}
## Conclusion
{{ conclusion }}
{% endif %}

---
*Written by {{ author }}*