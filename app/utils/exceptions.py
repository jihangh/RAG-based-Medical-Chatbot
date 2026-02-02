class AppBaseException(Exception):
    """Base class for all application-specific exceptions."""
    pass


class NetworkError(AppBaseException):
    def __init__(self, message="Network error occurred."):
        super().__init__(message)


class PDFLoadError(AppBaseException):
    def __init__(self, message="Failed to load PDF."):
        super().__init__(message)


class DataProcessingError(AppBaseException):
    def __init__(self, message="Error processing data."):
        super().__init__(message)


class DocumentFilterError(Exception):
    def __init__(self, message="Error filtering documents."):
        super().__init__(message)


class DocDenseEmbedError(AppBaseException):
    def __init__(self, message="Error generating dense document embeddings."):
        super().__init__(message)


class DocSparseEmbedError(AppBaseException):
    def __init__(self, message="Error generating sparse document embeddings."):
        super().__init__(message)


class DatabaseConnectionError(AppBaseException):
    def __init__(self, message="Failed to connect to the database."):
        super().__init__(message)


class BatchUploadError(AppBaseException):
    def __init__(self, message="Error uploading batch to the database."):
        super().__init__(message)


class RecordUploadError(AppBaseException):
    def __init__(self, message="Error uploading records to the database."):
        super().__init__(message)


class BuildKnowledgeBaseError(AppBaseException):
    def __init__(self, message="Error building the knowledge base."):
        super().__init__(message)


class QueryDenseEmbedError(AppBaseException):
    def __init__(self, message="Error generating dense query embeddings."):
        super().__init__(message)


class QuerySparseEmbedError(AppBaseException):
    def __init__(self, message="Error generating sparse query embeddings."):
        super().__init__(message)


class HybridSearchError(AppBaseException):
    def __init__(self, message="Error during hybrid search operation."):
        super().__init__(message)


class HybridRetreiverError(AppBaseException):
    def __init__(self, message="Error in Hybrid Retriever."):
        super().__init__(message)


class PromptFileNotFoundError(AppBaseException):
    def __init__(self, message="Prompt text file not found."):
        super().__init__(message)


class BuildContextPromptError(AppBaseException):
    def __init__(self, message="Error building context prompt."):
        super().__init__(message)


class RagChainError(AppBaseException):
    def __init__(self, message="Error occurred in RAG chain execution."):
        super().__init__(message)

