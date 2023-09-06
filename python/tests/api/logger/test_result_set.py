from logging import getLogger

import pandas as pd

import whylogs as why
from whylogs.api.logger.result_set import SegmentedResultSet
from whylogs.core.schema import DatasetSchema
from whylogs.core.segmentation_partition import segment_on_column

TEST_LOGGER = getLogger(__name__)


def test_result_set_metadata_on_writables():
    segment_column = "col1"
    df = pd.DataFrame(data={segment_column: [1, 2]})
    results: SegmentedResultSet = why.log(df, schema=DatasetSchema(segments=segment_on_column(segment_column)))

    assert results.metadata is not None
    assert "whylabs.traceId" in results.metadata
    trace_id = results.metadata["whylabs.traceId"]
    custom_metadata_value = "Some custom metadata string"
    custom_metadata_key = "foo"
    results.metadata[custom_metadata_key] = custom_metadata_value

    for profile in results.get_writables():
        assert "whylabs.traceId" in profile.metadata
        assert profile.metadata["whylabs.traceId"] == trace_id
        assert custom_metadata_key in profile.metadata
        assert profile.metadata[custom_metadata_key] == custom_metadata_value
