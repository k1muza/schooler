class BaseValidator: 
    def validate(self, request, *args, **kwargs):
        raise NotImplementedError('Subclasses must implement this method')
