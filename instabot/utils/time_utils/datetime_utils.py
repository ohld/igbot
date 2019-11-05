import datetime


class DatetimeUtils:

    SECONDS_IN_A_WEEK = 604800
    SECONDS_IN_A_DAY = 86400
    SECONDS_IN_A_HOUR = 3600
    SECONDS_IN_A_MINUTE = 60
    MINUTES_IN_A_YEAR = 525600
    MINUTES_IN_A_MONTH = 43800
    MINUTES_IN_A_WEEK = 10080
    MINUTES_IN_A_DAY = 1440
    MINUTES_IN_A_HOUR = 60

    @staticmethod
    def difference_in_seconds(a, b):
        duration = a - b
        return duration.total_seconds()

    @staticmethod
    def difference_in_minutes(a, b):
        duration_in_seconds = DatetimeUtils.difference_in_seconds(a, b)
        return divmod(duration_in_seconds, 60)

    # @staticmethod
    # def difference_in_hours(a, b):
    #     return a - b  # in seconds
    #
    # @staticmethod
    # def difference_in_days(a, b):
    #     duration, duration_in_seconds = DatetimeUtils.difference_in_seconds(a, b)
    #     duration_in_days = duration.days  # Build-in datetime function
    #     duration_in_days = divmod(duration_in_seconds, 86400)[0]  # Seconds in a day = 86400

    @staticmethod
    def days_to_seconds(quantity):
        return quantity * DatetimeUtils.SECONDS_IN_A_DAY

    @staticmethod
    def minutes_to_seconds(quantity):
        return quantity * DatetimeUtils.SECONDS_IN_A_MINUTE

    @staticmethod
    def now():
        return datetime.datetime.utcnow().replace(microsecond=0)

