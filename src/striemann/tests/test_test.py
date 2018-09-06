from expects import expect
from striemann.test import fakes
from striemann.test.expectsmatcher import contain_metric


class TestExpectsMatcher:
    def test(self):
        metrics = fakes.FakeMetrics()
        metrics.incrementCounter("Burgers sold")
        metrics.recordGauge("Hunger level", 10)
        expect(metrics).to(contain_metric("Hunger level"))
