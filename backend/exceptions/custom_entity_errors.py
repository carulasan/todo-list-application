from exceptions.custom_errors import DeletionForbiddenError

class BrandDeletionWithStoreError(DeletionForbiddenError):
    """Brand Deletion with associated Store Error."""
    parent_entity = "brand"
    child_entity = "store"

    def __init__(self, error_code):
        super().__init__(error_code, self.parent_entity, self.child_entity)

class SupercardPrefixDeletionWithSupercardBatchError(DeletionForbiddenError):
    """SupercardPrefix Deletion with associated SupercardBatch Error."""
    parent_entity = "supercard_prefix" 
    child_entity = "supercard_batch"

    def __init__(self, error_code):
        super().__init__(error_code, self.parent_entity, self.child_entity)


class CountryDeletionWithStoreError(DeletionForbiddenError):
    """Country Deletion with associated Store Error."""
    parent_entity = "country"
    child_entity = "store"

    def __init__(self, error_code):
        super().__init__(error_code, self.parent_entity, self.child_entity)
        
        
class NotificationOptOutDeletionWithStoreError(DeletionForbiddenError):
    """Brand Deletion with associated Store Error."""
    parent_entity = "brand"
    child_entity = "store"

    def __init__(self, error_code):
        super().__init__(error_code, self.parent_entity, self.child_entity)

