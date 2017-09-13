from expects import expect
from icdiff_expects import equal

from unittest import mock
import striemann.metrics


class Test:

    def test_in_memory(self):
        transport = striemann.metrics.InMemoryTransport()
        metrics = striemann.metrics.Metrics(transport, source='test')
        metrics.recordGauge('service_name', 2., tags=['spam'], ham='eggs')
        metrics.recordGauge('service_name', 4., tags=['spam'], ham='eggs')
        metrics.incrementCounter(
            'service_name', value=5, tags=['foo'], bar='baz'
        )
        metrics.flush()
        expect(transport.last_batch).to(equal([
            {'attributes': {'ham': 'eggs', 'source': 'test'},
             'metric_f': 2.0,
             'service': 'service_name.min',
             'tags': ['spam']},
            {'attributes': {'ham': 'eggs', 'source': 'test'},
             'metric_f': 4.0,
             'service': 'service_name.max',
             'tags': ['spam']},
            {'attributes': {'ham': 'eggs', 'source': 'test'},
             'metric_f': 3.0,
             'service': 'service_name.mean',
             'tags': ['spam']},
            {'attributes': {'ham': 'eggs', 'source': 'test'},
             'metric_f': 2,
             'service': 'service_name.count',
             'tags': ['spam']},
            {'attributes': {'bar': 'baz', 'source': 'test'},
             'metric_f': 5,
             'service': 'service_name',
             'tags': ['foo']}
        ]))

    def test_ttl(self):
        transport = striemann.metrics.InMemoryTransport()
        metrics = striemann.metrics.Metrics(transport)

        metrics.incrementCounter('heartbeat', ttl=7)
        metrics.flush()

        expect(transport.last_batch).to(equal([
            {
                'service': 'heartbeat',
                'ttl': 7.0,
                'metric_f': 1,
                'tags': [],
                'attributes': {}
            }
        ]))


    @mock.patch('timeit.default_timer', side_effect=[0, 1, 0, 3])
    def test_timers(self, timer):

        transport = striemann.metrics.InMemoryTransport()
        metrics = striemann.metrics.Metrics(transport)

        with metrics.time('time'):
            pass

        with metrics.time('time'):
            pass

        metrics.flush()
        expect(transport.last_batch[0]).to(equal(
            {
                'service': 'time.min',
                'metric_f': 1,
                'tags': [],
                'attributes': {}
            }))
        expect(transport.last_batch[1]).to(equal(
            {
                'service': 'time.max',
                'metric_f': 3,
                'tags': [],
                'attributes': {}
            }))
        expect(transport.last_batch[2]).to(equal(
            {
                'service': 'time.mean',
                'metric_f': 2,
                'tags': [],
                'attributes': {}
            }))
        expect(transport.last_batch[3]).to(equal(
            {
                'service': 'time.count',
                'metric_f': 2,
                'tags': [],
                'attributes': {}
            }))
