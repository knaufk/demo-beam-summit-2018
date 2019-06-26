from __future__ import absolute_import

import argparse
import logging
import re

import apache_beam as beam
from apache_beam.transforms import window
from apache_beam.transforms import trigger
from apache_beam.io.external.kafka import ReadFromKafka
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions
from apache_beam.transforms.trigger import AccumulationMode


class LoggingDoFn(beam.DoFn):
    def process(self, element):
        logging.info(element)

def run(argv=None):
    parser = argparse.ArgumentParser()
    known_args, pipeline_args = parser.parse_known_args(argv)

    pipeline_options = PipelineOptions(pipeline_args)
    pipeline_options.view_as(SetupOptions).save_main_session = True
    p = beam.Pipeline(options=pipeline_options)

    (p | 'ReadFromKafka' >> ReadFromKafka(consumer_config={"bootstrap.servers": "localhost:9092"},
                                          topics=["beam-input"])
     | 'ExtractWords' >> beam.FlatMap(lambda (k,v): re.findall(r'[A-Za-z\']+', v))
     | 'Window' >> beam.WindowInto(window.GlobalWindows(), trigger=trigger.Repeatedly(trigger.AfterCount(1)), accumulation_mode=AccumulationMode.ACCUMULATING)
     | 'Count' >> beam.combiners.Count.PerElement()
     | 'Format' >> beam.Map(lambda word_count: '%s: %s' % (word_count[0], word_count[1]))
     | 'Log' >> beam.ParDo(LoggingDoFn()))

    result = p.run()
    result.wait_until_finish()

if __name__ == '__main__':
    logging.getLogger().setLevel(logging.INFO)
    run()
