class Sensor:
    __slots__ = (
        "_lock",
        "_registry",
        "_name",
        "_parents",
        "_metrics",
        "_stats",
        "_config",
        "_inactive_sensor_expiration_time_ms",
        "_last_record_time",
    )
    def __init__(self, registry, name, parents, config, inactive_sensor_expiration_time_seconds) -> None: ...
    @property
    def name(self):
        """
        The name this sensor is registered with.
        This name will be unique among all registered sensors.
        """
        ...
    @property
    def metrics(self): ...
    def record(self, value: float = 1.0, time_ms=None) -> None:
        """
        Record a value at a known time.
        Arguments:
            value (double): The value we are recording
            time_ms (int): A POSIX timestamp in milliseconds.
                Default: The time when record() is evaluated (now)

        Raises:
            QuotaViolationException: if recording this value moves a
                metric beyond its configured maximum or minimum bound
        """
        ...
    def add_compound(self, compound_stat, config=None) -> None:
        """
        Register a compound statistic with this sensor which
        yields multiple measurable quantities (like a histogram)

        Arguments:
            stat (AbstractCompoundStat): The stat to register
            config (MetricConfig): The configuration for this stat.
                If None then the stat will use the default configuration
                for this sensor.
        """
        ...
    def add(self, metric_name, stat, config=None) -> None:
        """
        Register a metric with this sensor

        Arguments:
            metric_name (MetricName): The name of the metric
            stat (AbstractMeasurableStat): The statistic to keep
            config (MetricConfig): A special configuration for this metric.
                If None use the sensor default configuration.
        """
        ...
    def has_expired(self):
        """Return True if the Sensor is eligible for removal due to inactivity."""
        ...
