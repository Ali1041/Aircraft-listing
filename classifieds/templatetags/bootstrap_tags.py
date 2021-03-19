from django import template
register = template.Library()


@register.filter
def add_class(modelform_input, css_class):
    return modelform_input.as_widget(attrs={'class': css_class})


@register.simple_tag
def replace_tags(params, new_param, new_value):
    if new_param not in params:
        return "?%s=%s&%s" % (new_param, new_value, params)
    else:
        new_param += "="
        start_index = params.find(new_param) + len(new_param)
        end_index = params.find("&", start_index)

        if end_index == -1:
            old_val = params[start_index:]
        else:
            old_val = params[start_index:end_index]

        params = params.replace(old_val, new_value)

        return "?" + params