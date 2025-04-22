class Input:
    """
    Base class for handling input operations with customizable parameters.

    Parameters
    ----------
    sleep : float, optional
        Time in seconds to wait between consecutive API requests.
        Default is 0.1 seconds.
    output_format : str, optional
        The format of the output file. Available option is 'json'.
        Default is 'json'.
    bulk : bool, optional
        If True, enables bulk processing and creates a bulk output file.
        For more details, refer to the documentation of the biodumpy package.
        Default is False.
    """

    def __init__(self,
                 sleep: float = 0.1,
                 output_format: str = "json",
                 bulk: bool = False
                 ):
        super().__init__()
        self.sleep = sleep
        self.output_format = output_format
        self.bulk = bulk

    def _download(self, **kwargs) -> list:
        raise NotImplementedError()
