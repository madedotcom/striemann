## [0.6] - 2018-05-31
Added documentation on Read the Docs.
### Deprecated
 - FakeMetrics is now a list. Fakemetrics.metrics will be removed in 1.0
   release.

## [0.5] - 2018-04-27
### Breaking changes
 - Gauges no longer record min/mean/max/count
   Once we actually started using the library in anger, it became apparent that
   for most gauges, the min/max/mean params aren't helpful.

   We've decided to drop that feature from `recordGauge` replacing it with a 
   new `recordSummary` method. The `time` method has been rewritten to use a
   Summary rather than a Gauge.
 - Made the "counters", and "gauges" properties of the Metrics class private.
 - Made the state of Counter, and Gauge private.


## [0.4] - 2017-11-14
### Fixes
-  Fix issue where we get stuck always 'Failed to flush metrics to riemann'

### Deprecated
- RiemannTransport.is_connected() should no longer be needed

## [0.3.1]
### Fixes
- We now reconnect if there is an exception raised during `flush`

## [0.3]
### Fixes
- Added missing TTL parameter to `time` method.

## [0.2]
### Fixes
- TTL attributes are no longer coerced to strings


[0.6]: https://github.com/madedotcom/striemann/compare/v0.5...v0.6
[0.5]: https://github.com/madedotcom/striemann/compare/v0.4.0...v0.5
[0.4]: https://github.com/madedotcom/striemann/compare/v0.3.0...v0.4.0
