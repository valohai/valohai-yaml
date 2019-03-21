def lint_iterables(lint_result, context, iterables):
    for iterable in iterables:
        if isinstance(iterable, dict):
            iterable = iterable.values()
        for item in iterable:
            if hasattr(item, 'lint'):
                item.lint(lint_result, context)
