def impl(*traits):
    def decorator(child_class):
        child_class = type(
            child_class.__name__,
            tuple(traits),
            dict(child_class.__dict__)
        )
        return child_class
    return decorator
